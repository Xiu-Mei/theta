import json

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse

from theta.users.validation import OfficeAdminValidationMixin
from location.models import Building, Floor, Place, Room
from utility.validation import text_validator


class LocationTemplateView(OfficeAdminValidationMixin, TemplateView):
    template_name = 'pages/location/locations.html'

    def __init__(self):
        self.office = None
        self.redirect = None

    def get(self, request, *args, **kwargs):
        self.is_office_admin()
        if self.redirect:
            redirect(self.redirect)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(LocationTemplateView, self).get_context_data(**kwargs)
        tree_view = list()
        buildings = Building.objects.filter(office=self.office).values_list(
            'id', 'name').order_by('name')
        for building in buildings:
            building_dict = dict()
            building_dict['text'] = building[1]
            building_dict['selectable'] = False
            floors = Floor.objects.filter(building=building[0]).values_list('id', 'name').order_by('name')
            if floors:
                building_dict['nodes'] = list()
            for floor in floors:
                floor_dict = dict()
                floor_dict['text'] = floor[1]
                floor_dict['href'] = 'building/{}/floor/{}'.format(building[0], floor[0])
                # rooms = Room.objects.filter(floor=floor[0]).values_list('id', 'name').order_by('name')
                # if rooms:
                #     floor_dict['nodes'] = list()
                # for room in rooms:
                #     room_dict = dict()
                #     room_dict['text'] = room[1]
                #     room_dict['href'] = 'devices/room/{}'.format(room[0])
                #     floor_dict['nodes'].append(room_dict)
                building_dict['nodes'].append(floor_dict)
            tree_view.append(building_dict)
        context['tree_view'] = json.dumps(tree_view)
        context['menu'] = 'location'
        return context


class FloorTemplateView(OfficeAdminValidationMixin, TemplateView):
    template_name = 'pages/location/floor.html'

    def __init__(self):
        self.office = None
        self.floor_id = None
        self.building_id = None
        self.redirect = None
        self.floor = None

    def get(self, request, *args, **kwargs):
        self.is_office_admin()
        self.validate_location()
        if self.redirect:
            return redirect(self.redirect)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(FloorTemplateView, self).get_context_data(**kwargs)
        context['menu'] = 'location'
        context['floor'] = self.floor
        context['places'] = Place.objects.filter(floor=self.floor_id)
        return context

    def post(self, request, *args, **kwargs):
        self.is_office_admin()
        self.validate_location()
        if self.redirect:
            return redirect(self.redirect)
        if request.is_ajax():
            post_params = self.validate_post_params()
            if post_params:
                print('id={}, left={}, top={}, text={}, action={}'.format(*post_params))
                return JsonResponse(self.change_place(*post_params))
        else:
            return redirect('location')

    def change_place(self, place_id, left, top, text, action):
        if action == 'save':
            if place_id:
                place = Place.objects.filter(floor_id=self.floor_id, id=place_id).update(left=left, top=top, name=text)
            else:
                place = Place.objects.create(floor_id=self.floor_id, left=left, top=top, name=text)
                place_id = place.id

            if place_id and place:
                response = {'id': place_id}
            else:
                response = {'id': 0}
            return response
        elif action == 'delete':
            Place.objects.filter(floor_id=self.floor_id, id=place_id).delete()
            return {'id': 0}
        return {}

    def validate_post_params(self):
        try:
            place_id = int(self.request.POST['id']) if 'id' in self.request.POST.keys() else 0
            left = int(self.request.POST['left'].split('px')[0])
            top = int(self.request.POST['top'].split('px')[0])
            text = text_validator(self.request.POST['text'], 'd, en, ru', allowed='_-', remove_tags=True,
                                  return_sentence=True)
            action = text_validator(self.request.POST['action'], 'en', remove_tags=True)
        except (KeyError, ValueError):
            return {}

        return [place_id, left, top, text, action]

    def validate_location(self):
        self.floor_id = self.kwargs['floor_id']
        self.building_id = self.kwargs['building_id']
        try:
            Building.objects.get(
                office=self.office,
                id=self.building_id,
            )
            self.floor = Floor.objects.get(
                building=self.building_id,
                id=self.floor_id,
            )
        except (Building.DoesNotExist, Floor.DoesNotExist):
            self.redirect = 'location'
            return
