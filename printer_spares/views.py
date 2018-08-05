from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import JsonResponse

from theta.users.validation import OfficeAdminValidationMixin
from utility.validation import text_validator
from printer_spares.models import Cartridge, CartridgeItem
from history.models import CartridgeItemHistory


class AddCartridgeTemplateView(OfficeAdminValidationMixin, TemplateView):
    template_name = 'pages/printer_spares/add_cartridge.html'

    def __init__(self):
        super(AddCartridgeTemplateView, self).__init__()
        self.office = None
        self.redirect = None

    def get(self, request, *args, **kwargs):
        self.is_office_admin()
        if self.redirect:
            redirect(self.redirect)
        get_params = dict()
        get_params['cartridge_name'] = self.request.GET.get('cartridgeName', '')
        get_params['number_of_cartridges'] = self.request.GET.get('numberOfCartridges', '')
        context = self.get_context_data()
        if self.validate_get_params(get_params):
            self.add_cartridge_item(get_params)
            return redirect('add_cartridge')
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(AddCartridgeTemplateView, self).get_context_data(**kwargs)
        context['cartridges'] = Cartridge.objects.all()
        context['history'] = CartridgeItemHistory.objects.filter(
            action__in=['income', 'consumption', 'delivery']
        ).order_by('-id')[:10]
        context['menu'] = 'storage'
        return context

    @staticmethod
    def validate_get_params(get_params):
        if not get_params['cartridge_name'] or not get_params['number_of_cartridges']:
            return None
        try:
            get_params['cartridge_name'] = text_validator(
                get_params['cartridge_name'],
                'en, ru, d',
                remove_tags=True,
                allowed='/|()-_',
                return_sentence=True,
            )
            get_params['number_of_cartridges'] = int(get_params['number_of_cartridges'])
            if get_params['number_of_cartridges'] == 0:
                raise ValueError
        except ValueError:
            return None
        return True

    def add_cartridge_item(self, get_params):
        try:
            cartridge = Cartridge.objects.get(name=get_params['cartridge_name'])
        except Cartridge.DoesNotExist:
            return
        cartridge_item, created = CartridgeItem.objects.get_or_create(
            cartridge=cartridge,
            office=self.office,
        )
        cartridge_item.in_stock += get_params['number_of_cartridges']
        if created:
            self.cartridge_item_history_create([cartridge_item, 'create', 'The first creation of printer item.'])
        if cartridge_item.in_stock < 0:
            cartridge_item.in_stock = 0
        cartridge_item.save()

        action = 'income' if get_params['number_of_cartridges'] > 0 else 'consumption'
        message = '{} {}'.format(
            get_params['number_of_cartridges'],
            cartridge_item.in_stock,
        )
        self.cartridge_item_history_create([cartridge_item, action, message])

    def cartridge_item_history_create(self, params):
        """
        :param params: [cartridge_item, action, message]
        :return: True or False
        """
        CartridgeItemHistory.objects.create(
            user=self.request.user,
            office=self.office,
            cartridge_item=params[0],
            action=params[1],
            message=params[2],
        )

    def post(self, request, *args, **kwargs):
        self.is_office_admin()
        if self.redirect:
            return redirect(self.redirect)
        if request.is_ajax():
            ajax_params = self.validate_ajax_params()
            if 'error' not in ajax_params.keys():
                return JsonResponse(self.get_ajax_response(**ajax_params))
            else:
                return JsonResponse({'error': ajax_params['error']})
        else:
            return redirect('add_cartridge')

    def validate_ajax_params(self):
        try:
            cartridge_name = text_validator(
                self.request.POST['cartridgeName'],
                'en, ru, d',
                remove_tags=True,
                allowed='/|()-_',
                return_sentence=True,
            )
        except ValueError:
            return {'error': 'Wrong cartridge name'}
        return {'cartridge_name': cartridge_name}

    def get_ajax_response(self, **params):
        try:
            cartridge_item = CartridgeItem.objects.get(
                cartridge__name=params['cartridge_name'],
                office=self.office,
            )
        except CartridgeItem.DoesNotExist:
            return {'inStock': 'None'}
        return {'inStock': cartridge_item.in_stock}
