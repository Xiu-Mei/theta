from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.http import JsonResponse

from theta.users.validation import OfficeAdminValidationMixin
from utility.validation import validation
from printer_spares.models import Cartridge, CartridgeItem
from history.models import CartridgeItemHistory


class AddCartridgeTemplateView(OfficeAdminValidationMixin, TemplateView):
    template_name = 'pages/printer_spares/add_cartridge.html'

    def __init__(self):
        super(AddCartridgeTemplateView, self).__init__()
        self.get_params = dict()
        self.validation_params = dict()
        self.post_params = dict()
        self.context = dict()
        self.params = dict()

    def get(self, request, *args, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')

        self.get_params['cartridge_name'] = self.request.GET.get('cartridgeName')
        self.validation_params['cartridge_name'] = {
            'symbol_set': 'en, ru, d',
            'allowed': '/|()-_',
            'return_sentence': True,
            'required': True,
        }
        self.get_params['number_of_cartridges'] = self.request.GET.get('numberOfCartridges')
        self.validation_params['number_of_cartridges'] = {
            'symbol_set': 'int',
            'required': True,
        }
        if validation(self.get_params, self.validation_params) is False:
            redirect('add_cartridge')

        self.get_context_data()

        if self.add_cartridge_item() is False:
            redirect('add_cartridge')

        return self.render_to_response(self.context)

    def get_context_data(self, **kwargs):
        self.context.update(super(AddCartridgeTemplateView, self).get_context_data(**kwargs))
        self.context['cartridges'] = Cartridge.objects.all()
        self.context['history'] = CartridgeItemHistory.objects.filter(
            action__in=['income', 'consumption', 'delivery']
        ).order_by('-id')[:10]
        self.context['menu'] = 'storage'

    def add_cartridge_item(self):
        if self.get_params['number_of_cartridges'] == 0:
            self.params['error'] = 'Number of cartridges is zero'
            return False
        try:
            cartridge = Cartridge.objects.get(name=self.get_params['cartridge_name'])
        except Cartridge.DoesNotExist:
            self.params['error'] = 'Cartridge doesn\'t exist'
            return False
        cartridge_item, created = CartridgeItem.objects.get_or_create(
            cartridge=cartridge,
            office=self.office,
        )
        if created:
            self.create_cartridge_item_history([cartridge_item, 'create', 'The first creation of printer item.'])
        cartridge_item.in_stock += self.get_params['number_of_cartridges']
        if cartridge_item.in_stock < 0:
            cartridge_item.in_stock = 0
        cartridge_item.save()

        action = 'income' if self.get_params['number_of_cartridges'] > 0 else 'consumption'
        message = '{} {}'.format(
            self.get_params['number_of_cartridges'],
            cartridge_item.in_stock,
        )
        self.create_cartridge_item_history([cartridge_item, action, message])

    def create_cartridge_item_history(self, params):
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

    def post(self, request):
        if self.is_office_admin() is False:
            return redirect('account_login')

        if request.is_ajax():
            self.post_params['cartridge_name'] = self.request.POST.get('cartridgeName')
            self.validation_params['cartridge_name'] = {
                'symbol_set': 'en, ru, d',
                'allowed': '/|()-_',
                'return_sentence': True,
                'required': True,
            }
            if validation(self.get_params, self.validation_params) is False:
                JsonResponse(self.post_params['error'])

            if self.get_post_context() is False:
                return JsonResponse({'error': self.post_params['error']})
            return JsonResponse(self.context)
        else:
            return redirect('add_cartridge')

    def get_post_context(self):
        try:
            cartridge_item = CartridgeItem.objects.get(
                cartridge__name=self.post_params['cartridge_name'],
                office=self.office,
            )
        except CartridgeItem.DoesNotExist:
            self.context['inStock'] = 'None'
            return True
        self.context['inStock'] = cartridge_item.in_stock
        return True

