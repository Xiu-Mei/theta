from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from devices.models import InventoryNumberPrefix, Manufacturer
from printers.models import Printer, PrinterItem, PrinterChangeCartridgeJob
from printer_spares.models import Cartridge, Spare, SpareItem, CartridgeItem
from location.models import Building, Floor, Place, Room
from utility.validation import validation, mask_validation
from theta.users.validation import OfficeAdminValidationMixin
from history.models import SpareItemHistory


class PrintersListView(OfficeAdminValidationMixin, TemplateView):
    number_per_page = 16
    template_name = 'pages/printers/printers.html'

    def __init__(self):
        super(PrintersListView, self).__init__()
        self.get_params = dict()
        self.validation_params = dict()
        self.post_params = dict()
        self.context = dict()
        self.params = dict()

    def get(self, request, *args, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')

        self.get_params['inv_num'] = self.request.GET.get('inv_num')
        self.validation_params['inv_num'] = {
            'symbol_set': 'en, ru, d',
            'allowed': '-',
        }
        self.get_params['variety'] = self.request.GET.get('variety')
        self.validation_params['variety'] = {
            'symbol_set': 'en, ru, d',
            'allowed': '-',
        }
        self.get_params['manufacturer'] = self.request.GET.get('manufacturer')
        self.validation_params['manufacturer'] = {'symbol_set': 'en, ru, d',
                                                  'allowed': '',
                                                  'return_sentence': True}
        self.get_params['page'] = self.request.GET.get('page', '1')
        self.validation_params['page'] = {'symbol_set': 'int'}
        if validation(self.get_params, self.validation_params) is False:
            redirect('printers')
        self.get_context_data()
        return self.render_to_response(self.context)

    def get_context_data(self, **kwargs):
        self.context.update(super(PrintersListView, self).get_context_data(**kwargs))
        self._fetch_list_of_printers()
        self.context['page'] = self.get_params['page']
        self.context['variety'] = self.get_params['variety'] if self.get_params['variety'] else ''
        self.context['manufacturer'] = self.get_params['manufacturer'] if self.get_params['manufacturer'] else ''

        self.context['paginator'] = Paginator(self.context['list_of_printers'], PrintersListView.number_per_page)
        self.context['printers'] = self.context['paginator'].get_page(self.context['page'])
        self.context['menu'] = 'printers'

    def _fetch_list_of_printers(self):
        filters = dict()
        filters['name__icontains'] = self.get_params['variety']
        filters['manufacturer__name__icontains'] = self.get_params['manufacturer']
        filters = {k: v for k, v in filters.items() if v is not None}
        self.context['list_of_printers'] = Printer.objects.filter(**filters)
        self.context['manufacturers'] = [manufacturer.name for manufacturer in Manufacturer.objects.all()
                                         if self.context['list_of_printers'].filter(manufacturer=manufacturer).exists()]


class PrinterView(OfficeAdminValidationMixin, TemplateView):
    template_name = 'pages/printers/printer.html'

    def __init__(self):
        super(PrinterView, self).__init__()
        self.get_params = dict()
        self.post_params = dict()
        self.context = dict()
        self.params = dict()
        self.action = ''

    def get(self, request, *args, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')

        self.params['printer_id'] = self.kwargs['printer_id']

        if not self.get_context_data():
            return redirect('printers')
        return self.render_to_response(self.context)

    def get_context_data(self, **kwargs):
        self.context.update(super(PrinterView, self).get_context_data(**kwargs))
        try:
            self.context['printer'] = Printer.objects.get(id=self.params['printer_id'])
        except Printer.DoesNotExist:
            return False
        self.context['printer_items'] = PrinterItem.objects.filter(
            office=self.office,
            printer=self.params['printer_id'],
        ).values('id', 'inventory_number').order_by('inventory_number')
        self.context['cartridges'] = Cartridge.objects.filter(printers__id=self.params['printer_id'])
        cartridge_items = dict()
        for cartridge in self.context['cartridges']:
            i = CartridgeItem.objects.filter(
                office=self.office,
                cartridge__id=cartridge.id,
            ).values_list('in_stock', flat=True)
            cartridge_items[cartridge.name] = i[0] if i else i
        self.context['cartridge_items'] = cartridge_items
        self.context['spares'] = Spare.objects.filter(printers__id=self.params['printer_id'])
        spare_items = dict()
        for spare in self.context['spares']:
            i = SpareItem.objects.filter(
                office=self.office,
                spare__id=spare.id,
            ).values_list('in_stock', flat=True)
            spare_items[spare.id] = i[0] if i else i
        self.context['spare_items'] = spare_items
        self.context['inv_prefix_masks'] = self.collect_prefixes()
        self.context['buildings'] = Building.objects.filter(office=self.office)
        self.context['menu'] = 'printers'
        return True

    def post(self, request, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')
        self.params['printer_id'] = kwargs['printer_id']
        if not request.is_ajax():
            return redirect('printer', printer_id=self.params['printer_id'])

        self.get_post_params() and self.get_post_context()

        if 'error' not in self.context.keys():
            return JsonResponse(self.context)
        else:
            return JsonResponse({'error': self.context['error']})

    def get_post_params(self):
        actions = dict()
        validation_params = dict()

        actions['addPrinterItem'] = ('mask', 'inv_number', 'note', 'building', 'floor', 'room', 'place')
        actions['addSpareItem'] = (('spare_id', 'spareId'), 'amount')
        actions['getFloors'] = ('building', )
        actions['getRooms'] = ('building', 'floor')
        actions['getPlaces'] = ('building', 'floor', 'room')

        validation_params['mask'] = {
            'symbol_set': 'w',
            'allowed': '-',
            'required': True,
        }
        validation_params['inv_number'] = {
            'symbol_set': 'w',
            'allowed': '-',
            'required': True,
        }
        validation_params['note'] = {
            'symbol_set': 'w',
            'allowed': '_-,.!?\n',
            'return_sentence': True,
        }
        validation_params['spare_id'] = {
            'symbol_set': 'int',
            'required': True,
        }
        validation_params['amount'] = {
            'symbol_set': 'int',
            'required': True,
        }
        validation_params['building'] = {
            'symbol_set': 'w',
            'allowed': '-_/*()',
            'return_sentence': True,
            'required': True,
        }
        validation_params['floor'] = {
            'symbol_set': 'w',
            'allowed': '-_/*()',
            'return_sentence': True,
            'required': True,
        }
        validation_params['room'] = {
            'symbol_set': 'w',
            'allowed': '-_/*()',
            'return_sentence': True,
        }
        validation_params['place'] = {
            'symbol_set': 'w',
            'allowed': '-_/*()',
            'return_sentence': True,
            'required': True,
        }
        self.action = self.request.POST.get('action')
        validation_params['action'] = {
            'symbol_set': 'en',
            'allowed_values': tuple(key for key in actions.keys()),
            'required': True,
        }
        if not validation({'action': self.action}, validation_params):
            return False

        for item in actions[self.action]:
            if type(item) is not tuple:
                self.post_params[item] = self.request.POST.get(item)
            else:
                self.post_params[item[0]] = self.request.POST.get(item[1])
        return validation(self.post_params, validation_params)

    def fetch_add_printer_params(self):
        get_printer_masks = InventoryNumberPrefix.objects.filter(devices__in=[1, ])
        self.params['prefix'] = None
        for mask in get_printer_masks:
            if str(mask) == self.post_params['mask']:
                self.params['prefix'] = mask
                break
        if self.params['prefix'] is None:
            self.context['error'] = 'There isn\'t such prefix and mask'
            return False

        self.params['inv_number'] = mask_validation(self.params['prefix'].inventory_number_mask,
                                                    self.post_params['inv_number'])
        if self.params['inv_number'] is None:
            self.context['error'] = 'Entered inventory number doesn\'t fit with mask.'
            return False
        self.get_place()
        if self.params['place'] is None:
            self.context['error'] = 'There is not such place.'
            return False

    def change_printer(self):
        if self.fetch_add_printer_params() is False:
            return False
        try:
            PrinterItem.objects.get(printer_id=self.params['printer_id'],
                                    office=self.office,
                                    prefix=self.params['prefix'],
                                    inventory_number=self.params['inv_number'],
                                    )
            self.context['error'] = 'Printer with this inventory number already exist.'
            return False
        except PrinterItem.DoesNotExist:
            printer_item = PrinterItem.objects.create(printer_id=self.params['printer_id'],
                                                      office=self.office,
                                                      place=self.params['place'],
                                                      prefix=self.params['prefix'],
                                                      inventory_number=self.params['inv_number'],
                                                      notes=self.post_params['note'],
                                                      )
            if printer_item:
                self.context['success'] = 'Printer has been created.'
                return True
            else:
                self.context['error'] = 'Cannot create printer.'
                return False
        return True

    def collect_prefixes(self):
        latest_printer_item = PrinterItem.objects.filter(office=self.office,
                                                         printer=self.params['printer_id'],
                                                         ).order_by('-id')
        all_prefixes = InventoryNumberPrefix.objects.filter(devices__in=[1, ])
        result = [str(prefix) for prefix in all_prefixes]
        if latest_printer_item:
            latest_printer_item = latest_printer_item[0]
            try:
                result.insert(0, result.pop(result.index(str(latest_printer_item.prefix))))
            except ValueError:
                return result
        return result

    def fetch_add_spare_params(self):
        try:
            self.params['spare'] = Spare.objects.get(id=self.post_params['spare_id'])
        except Spare.DoesNotExist:
            self.context['error'] = 'A spare with this id doesn\'t exists.'
            return False

    def change_spare(self):
        if self.fetch_add_spare_params() is False:
            return False
        if self.post_params['amount'] == 0:
            self.context['error'] = 'Number of spares is zero'
            return False

        spare_item, created = SpareItem.objects.get_or_create(spare=self.params['spare'],
                                                              office=self.office,
                                                              )
        if created:
            self.create_spare_item_history([spare_item, 'create', 'The first creation of spare item.'])
        spare_item.in_stock += self.post_params['amount']
        if spare_item.in_stock < 0:
            spare_item.in_stock = 0
        spare_item.save()
        action = 'income' if self.post_params['amount'] > 0 else 'consumption'
        message = '{} {}'.format(
            self.post_params['amount'],
            spare_item.in_stock,
        )
        self.create_spare_item_history([spare_item, action, message])

        if spare_item:
            self.context['success'] = 'Spare is changed.'
            self.context['instock'] = spare_item.in_stock
            return True
        else:
            self.context['error'] = 'Cannot change the spare.'
            return False

    def create_spare_item_history(self, params):
        """
        :param params: [spare_item, action, message]
        :return: True or False
        """
        SpareItemHistory.objects.create(
            user=self.request.user,
            office=self.office,
            spare_item=params[0],
            action=params[1],
            message=params[2],
        )

    def get_building(self):
        try:
            self.params['building'] = Building.objects.get(office=self.office, name=self.post_params['building'])
        except Building.DoesNotExist:
            self.params['building'] = None

    def get_floors(self):
        self.get_building()
        self.params['floors'] = Floor.objects.filter(building=self.params['building'])

    def get_rooms(self):
        self.get_floors()
        self.params['floor'] = [floor for floor in self.params['floors']
                                if floor.name == self.post_params['floor']]

        self.params['floor'] = self.params['floor'][0] if self.params['floor'] else None
        self.params['rooms'] = Room.objects.filter(floor=self.params['floor'])

    def get_places(self):
        self.get_rooms()
        if 'room' not in self.post_params.keys() or self.post_params['room'] == '':
            self.params['places'] = Place.objects.filter(floor=self.params['floor'])
        else:
            self.params['room'] = [room for room in self.params['rooms'] if room.name == self.post_params['room']]
            self.params['room'] = self.params['room'][0] if self.params['room'] else None
            self.params['places'] = Place.objects.filter(floor=self.params['floor'],
                                                         room=self.params['room']
                                                         )

    def get_place(self):
        self.get_places()
        # TODO: receive place id, that will allow have same name place on floor
        self.params['place'] = [place for place in self.params['places'] if place.name == self.post_params['place']]
        self.params['place'] = self.params['place'][0] if self.params['place'] else None

    def get_floors_context(self):
        self.get_floors()
        self.context['floors'] = [floor.name for floor in self.params['floors']]

    def get_rooms_and_places_context(self):
        self.get_places()
        self.context['rooms'] = [room.name for room in self.params['rooms']]
        self.context['places'] = [place.name for place in self.params['places']]

    def get_places_for_room_context(self):
        self.get_places()
        self.context['places'] = [place.name for place in self.params['places']]

    def get_post_context(self):
        if self.action == 'addPrinterItem':
            self.change_printer()
        elif self.action == 'addSpareItem':
            self.change_spare()
        elif self.action == 'getFloors':
            self.get_floors_context()
        elif self.action == 'getRooms':
            self.get_rooms_and_places_context()
        elif self.action == 'getPlaces':
            self.get_places_for_room_context()


class PrinterItemView(OfficeAdminValidationMixin, TemplateView):
    template_name = 'pages/printers/printer_item.html'

    def __init__(self):
        super(PrinterItemView, self).__init__()
        self.get_params = dict()
        self.post_params = dict()
        self.context = dict()
        self.params = dict()
        self.action = ''

    def get(self, request, *args, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')

        self.params['printer_item_id'] = self.kwargs['printer_item_id']

        if not self.get_context_data():
            return redirect('printers')
        return self.render_to_response(self.context)

    def get_context_data(self, **kwargs):
        self.context.update(super(PrinterItemView, self).get_context_data(**kwargs))
        try:
            self.context['printer_item'] = PrinterItem.objects.get(
                office=self.office,
                id=self.params['printer_item_id']
            )
            self.context['printer'] = self.context['printer_item'].printer
        except ObjectDoesNotExist:
            return False

        cartridges = Cartridge.objects.filter(printers__id=self.context['printer'].id)
        self.context['cartridges'] = list()
        for cartridge in cartridges:
            try:
                cartridge_item = CartridgeItem.objects.get(
                    office=self.office,
                    cartridge=cartridge,
                )
                self.context['cartridges'].append((cartridge, cartridge_item))
            except ObjectDoesNotExist:
                self.context['cartridges'].append((cartridge, 0))
                continue
        self.context['spares'] = Spare.objects.filter(printers__id=self.context['printer'].id)
        spare_items = dict()
        for spare in self.context['spares']:
            i = SpareItem.objects.filter(
                office=self.office,
                spare__id=spare.id,
            ).values_list('in_stock', flat=True)
            spare_items[spare.id] = i[0] if i else i
        self.context['spare_items'] = spare_items

        self.context['place'] = self.context['printer_item'].place
        try:
            if self.context['printer_item'].place.room_id:
                self.context['room'] = Room.objects.get(id=self.context['printer_item'].place.room_id)
            self.context['floor'] = Floor.objects.get(id=self.context['printer_item'].place.floor_id)
            self.context['building'] = Building.objects.get(office=self.office,
                                                            floor__id=self.context['floor'].id
                                                            )
        except ObjectDoesNotExist as e:
            print(e)
        self.context['menu'] = 'printers'
        return True

    def post(self, request, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')
        if not request.is_ajax():
            return redirect('printer_item', printer_item_id=self.params['printer_item_id'])
        self.params['printer_item_id'] = self.kwargs['printer_item_id']

        self.get_post_params() and self.get_post_context()

        if 'error' not in self.context.keys():
            return JsonResponse(self.context)
        else:
            return JsonResponse({'error': self.context['error']})

    def get_post_params(self):
        actions = dict()
        validation_params = dict()

        actions['savePrinterItem'] = ('condition', 'notes',)
        actions['cartridgeIssue'] = ('cartridge_id',)

        validation_params['condition'] = {
            'symbol_set': 'en',
            'allowed_values': tuple(i2 for i1, i2 in PrinterItem._meta.get_field('working_condition').choices),
        }
        validation_params['notes'] = {
            'symbol_set': 'w',
            'allowed': '-_/*().,!?\n',
            'return_sentence': True,
        }
        validation_params['cartridge_id'] = {
            'symbol_set': 'int',
            'required': True,
        }

        self.action = self.request.POST.get('action')
        validation_params['action'] = {
            'symbol_set': 'en',
            'allowed_values': tuple(key for key in actions.keys()),
            'required': True,
        }
        if not validation({'action': self.action}, validation_params):
            return False

        for item in actions[self.action]:
            if type(item) is not tuple:
                self.post_params[item] = self.request.POST.get(item)
            else:
                self.post_params[item[0]] = self.request.POST.get(item[1])
        return validation(self.post_params, validation_params)

    def change_printer_item(self):
        printer_item_changed = False
        try:
            printer_item = PrinterItem.objects.get(office=self.office,
                                                   id=self.params['printer_item_id'],
                                                   )
            if self.post_params['condition']:
                printer_item.working_condition = self.post_params['condition']
                printer_item_changed = True
            if self.post_params['notes'] and printer_item.notes != self.post_params['notes']:
                printer_item.notes = self.post_params['notes']
                printer_item_changed = True
            elif not self.post_params['notes'] and printer_item.notes:
                printer_item.notes = ''
                printer_item_changed = True
        except ObjectDoesNotExist:
            self.context['error'] = 'Printer doesn\'t exist'
            return
        if printer_item_changed:
            printer_item.save()
            self.context['success'] = 'Printer updated.'

    def cartridge_issue(self):
        try:
            cartridge_item = CartridgeItem.objects.get(
                office=self.office,
                id=self.post_params['cartridge_id'],
            )
        except ObjectDoesNotExist:
            self.context['error'] = 'Wrong cartridge.'
            return False
        if cartridge_item.in_stock < 1:
            self.context['error'] = 'Not enough cartridges.'
            return False
        cartridge_item.in_stock -= 1
        cartridge_item.save()

        PrinterChangeCartridgeJob.objects.create(printer_item_id=self.params['printer_item_id'])
        self.context['instock'] = cartridge_item.in_stock
        self.context['cartridge_item_id'] = cartridge_item.id
        self.context['success'] = 'The cartridge is issued.'
        return True

    def get_post_context(self):
        if self.action == 'savePrinterItem':
            self.change_printer_item()
        elif self.action == 'cartridgeIssue':
            self.cartridge_issue()


