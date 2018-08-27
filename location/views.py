import json

from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import JsonResponse

from theta.users.validation import OfficeAdminValidationMixin
from location.models import Building, Floor, Place
from utility.validation import validation


class LocationTemplateView(OfficeAdminValidationMixin, TemplateView):
    template_name = 'pages/location/locations.html'

    def __init__(self):
        super(LocationTemplateView, self).__init__()
        self.context = dict()

    def get(self, request, *args, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')

        self.get_context_data()
        return self.render_to_response(self.context)

    def get_context_data(self, **kwargs):
        self.context.update(super(LocationTemplateView, self).get_context_data(**kwargs))
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
        self.context['tree_view'] = json.dumps(tree_view)
        self.context['menu'] = 'location'


class FloorTemplateView(OfficeAdminValidationMixin, TemplateView):
    template_name = 'pages/location/floor.html'

    def __init__(self):
        super(FloorTemplateView, self).__init__()
        self.params = dict()
        self.context = dict()
        self.post_params = dict()
        self.validation_params = dict()

    def get(self, request, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')

        self.params['building_id'] = kwargs['building_id']
        self.params['floor_id'] = kwargs['floor_id']
        if self.get_floor() is False:
            return redirect('location')

        self.get_context_data()
        return self.render_to_response(self.context)

    def get_context_data(self, **kwargs):
        self.context.update(super(FloorTemplateView, self).get_context_data(**kwargs))
        self.context['menu'] = 'location'
        self.context['floor'] = self.params['floor']
        self.context['places'] = Place.objects.filter(floor=self.params['floor_id'])

    def post(self, request, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')

        self.params['building_id'] = kwargs['building_id']
        self.params['floor_id'] = kwargs['floor_id']
        if self.get_floor() is False:
            return redirect('location')

        self.post_params['place_id'] = self.request.POST.get('id')
        self.validation_params['place_id'] = {
            'symbol_set': 'int',
        }
        self.post_params['left'] = self.request.POST.get('left')
        if self.post_params['left'].endswith('px'):
            self.post_params['left'] = self.post_params['left'][:-2]
        self.validation_params['left'] = {
            'symbol_set': 'int',
            'required': True,
        }
        self.post_params['top'] = self.request.POST.get('top')
        if self.post_params['top'].endswith('px'):
            self.post_params['top'] = self.post_params['top'][:-2]
        self.validation_params['top'] = {
            'symbol_set': 'int',
            'required': True,
        }
        self.post_params['text'] = self.request.POST.get('text')
        self.validation_params['text'] = {
            'symbol_set': 'd, en, ru',
            'allowed': '_-',
            'return_sentence': True,
        }
        self.post_params['action'] = self.request.POST.get('action')
        self.validation_params['action'] = {
            'symbol_set': 'en_sm',
            'allowed_values': ('save', 'delete', ),
            'required': True,
        }
        if request.is_ajax():
            if validation(self.post_params, self.validation_params) is False:
                return JsonResponse({'error': self.post_params['error']})

            self.change_place()
            print(self.context['id'])
            return JsonResponse(self.context)
        else:
            return redirect('location')

    def change_place(self):
        if self.post_params['action'] == 'save':
            if self.post_params['place_id']:
                place = Place.objects.filter(floor_id=self.params['floor'], id=self.post_params['place_id']).\
                    update(
                    left=self.post_params['left'],
                    top=self.post_params['top'],
                    name=self.post_params['text']
                )
                self.context['id'] = self.post_params['place_id'] if place else 0
            else:
                place = Place.objects.create(
                    floor_id=self.params['floor_id'],
                    left=self.post_params['left'],
                    top=self.post_params['top'],
                    name=self.post_params['text']
                )
                self.context['id'] = place.id if place else 0

        elif self.post_params['action'] == 'delete':
            Place.objects.filter(floor_id=self.params['floor'], id=self.post_params['place_id']).delete()
            self.context['id'] = 0

    def get_floor(self):
        try:
            Building.objects.get(
                office=self.office,
                id=self.params['building_id'],
            )
            self.params['floor'] = Floor.objects.get(
                building=self.params['building_id'],
                id=self.params['floor_id'],
            )
        except (Building.DoesNotExist, Floor.DoesNotExist):
            self.params['error'] = 'Building or Floor doesn\'t  exitst'
            return False
