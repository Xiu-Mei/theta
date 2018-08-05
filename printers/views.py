from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import JsonResponse

from devices.models import InventoryNumberPrefix
from printers.models import Printer, PrinterItem
from printer_spares.models import Cartridge, Spare, SpareItem, CartridgeItem
from location.models import Place, Room
from utility.validation import text_validator, mask_validation


class PrintersListView(TemplateView):
    #  TODO: validate get parameters
    number_per_page = 16
    template_name = 'pages/printers/printers.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account_login')
        get_params = dict()
        get_params['variety'] = self.request.GET.get('variety', '')
        get_params['manufacturer'] = self.request.GET.get('manufacturer', '')
        get_params['page'] = self.request.GET.get('page', '1')
        context = self.get_context_data(**get_params)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(PrintersListView, self).get_context_data(**kwargs)
        self._fetch_list_of_printers(context)
        context['paginator'] = Paginator(context['list_of_printers'], PrintersListView.number_per_page)
        context['printers'] = context['paginator'].get_page(context['page'])
        context['menu'] = 'printers'
        return context

    @staticmethod
    def _fetch_list_of_printers(context):
        filters = dict()
        filters['name__icontains'] = context['variety'] if context['variety'] else None
        filters['manufacturer__name__icontains'] = context['manufacturer'] if context['manufacturer'] else None
        filters = {k: v for k, v in filters.items() if v is not None}
        context['list_of_printers'] = Printer.objects.filter(**filters)


class PrinterView(TemplateView):
    template_name = 'pages/printers/printer.html'

    def __init__(self):
        self.redirect = None
        self.office = None
        self.printer_id = None
        self.default_storage = None

    def get(self, request, *args, **kwargs):
        self.validation()
        if self.redirect:
            return redirect(self.redirect)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        printer_id = self.kwargs['printer_id']
        context = super(PrinterView, self).get_context_data(**kwargs)
        context['printer'] = Printer.objects.get(id=printer_id)
        context['printer_items'] = PrinterItem.objects.filter(
            office=self.office,
            printer=printer_id,
        ).values('inventory_number').order_by('inventory_number')
        context['cartridges'] = Cartridge.objects.filter(printers__id=printer_id)
        cartridge_items = dict()
        for cartridge in context['cartridges']:
            i = CartridgeItem.objects.filter(
                office=self.office,
                cartridge__id=cartridge.id,
            ).values_list('in_stock', flat=True)
            cartridge_items[cartridge.name] = i[0] if i else i
        context['cartridge_items'] = cartridge_items
        context['spares'] = Spare.objects.filter(printers__id=printer_id)
        spare_items = dict()
        for spare in context['spares']:
            i = SpareItem.objects.filter(
                office=self.office,
                spare__id=spare.id,
            ).values_list('in_stock', flat=True)
            spare_items[spare.id] = i[0] if i else i
        context['spare_items'] = spare_items
        context['inv_prefix_masks'] = self.collect_prefixes()
        context['menu'] = 'printers'
        return context

    def post(self, request, *args, **kwargs):
        self.validation()
        if self.redirect:
            return redirect(self.redirect)
        if request.is_ajax():
            post_params = self.validate_post_params()
            if 'error' not in post_params.keys():
                return JsonResponse(self.change_printer(**post_params))
            else:
                return JsonResponse({'error': post_params['error']})
        else:
            return redirect('location')

    def validation(self):
        if not self.request.user.is_authenticated:
            self.redirect = 'account_login'
            return
        self.office = self.request.user.office
        self.printer_id = self.kwargs['printer_id']

    def validate_post_params(self):
        allowed_actions = ['create', ]
        try:
            default_storage = Room.objects.get(office=self.office, name='###storage')
            default_storage_place = Place.objects.get(room=default_storage, name='###printers')
        except ValueError:
            return {'error': 'There isn\'t a default virtual storage: ###storage or place: ###printers'}
        try:
            prefix_and_inventory_number = text_validator(self.request.POST['mask'],
                                                         'w, d',
                                                         allowed='-',
                                                         remove_tags=True
                                                         )
            get_printer_masks = InventoryNumberPrefix.objects.filter(devices__in=[1, ])
            current_mask = None
            for mask in get_printer_masks:
                if str(mask) == prefix_and_inventory_number:
                    current_mask = mask
                    break
            if current_mask is None:
                return {'error': 'There isn\'t such prefix and mask'}

            inventory_number = text_validator(self.request.POST['inv_number'],
                                              'w, d',
                                              allowed='-',
                                              remove_tags=True
                                              )
            if 'note' in self.request.POST.keys() and self.request.POST['note']:
                notes = text_validator(self.request.POST['note'],
                                       'd, en, ru',
                                       allowed='_-',
                                       remove_tags=True,
                                       return_sentence=True
                                       )
            else:
                notes = ''
            action = text_validator(self.request.POST['action'], 'w', remove_tags=True)
            if action not in allowed_actions:
                return {'error': 'Unknown action.'}
        except (KeyError, ValueError):
            return {'error': ' Please, assign all values.'}
        inventory_number = mask_validation(current_mask.inventory_number_mask, inventory_number)
        if inventory_number:
            return {'inventory_number': inventory_number,
                    'place': default_storage_place,
                    'prefix': current_mask,
                    'notes': notes,
                    'action': action,
                    }
        else:
            return {'error': 'Entered inventory number doesn\'t fit with mask.'}

    def change_printer(self, **params):
        if params['action'] == 'create':
            try:
                PrinterItem.objects.get(printer_id=self.printer_id,
                                        office=self.office,
                                        prefix=params['prefix'],
                                        inventory_number=params['inventory_number'],
                                        )
                return {'error': 'Printer with this inventory number already exist.'}
            except PrinterItem.DoesNotExist:
                printer_item = PrinterItem.objects.create(printer_id=self.printer_id,
                                                          office=self.office,
                                                          place=params['place'],
                                                          prefix=params['prefix'],
                                                          inventory_number=params['inventory_number'],
                                                          notes=params['notes'],
                                                          )
                if printer_item:
                    return {'success': 'Printer has been created.'}
                else:
                    return {'error': 'Cannot create printer.'}

    def collect_prefixes(self):
        latest_printer_item = PrinterItem.objects.filter(office=self.office,
                                                         printer=self.printer_id,
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
