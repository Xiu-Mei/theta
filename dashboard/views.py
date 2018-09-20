from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.urls import reverse

from theta.users.validation import OfficeAdminValidationMixin
from printers.models import PrinterItem
from devices.models import InventoryNumberPrefix
from utility.validation import validation, mask_validation
from utility.list_with_titles import ListWithTitles


class MainAdminView(OfficeAdminValidationMixin, TemplateView):
    template_name = 'pages/dashboard/main.html'

    def __init__(self):
        super(MainAdminView, self).__init__()
        self.get_params = dict()
        self.post_params = dict()
        self.context = dict()
        self.params = dict()
        self.allowed_actions = ('search_by_inv_num', 'search_by_place')
        self.action = ''

    def get(self, request, *args, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')

        if not self.get_context_data():
            return redirect('main_admin')
        return self.render_to_response(self.context)

    def get_context_data(self, **kwargs):
        translations = ('Printer inv.num:', 'Place name:')
        self.context['search_actions'] = [(action, translation)
                                          for action, translation in zip(self.allowed_actions, translations)]
        return True

    def post(self, request, **kwargs):
        if self.is_office_admin() is False:
            return redirect('account_login')
        if not request.is_ajax():
            return redirect('main_admin')
        self.get_post_params() and self.get_post_context()
        html = render_to_string('pages/grid_with_pagination.html', self.context)
        return HttpResponse(html)

    def get_post_params(self):
        actions = dict()
        validation_params = dict()

        actions['search_by_inv_num'] = ('search_str', 'page')
        actions['search_by_place'] = ('search_str', 'page')

        self.action = self.request.POST.get('action')
        validation_params['action'] = {
            'symbol_set': 'en',
            'allowed': '_',
            'allowed_values': tuple(key for key in actions.keys()),
            'required': True,
        }
        if not validation({'action': self.action}, validation_params):
            return False
        if self.action == 'search_by_inv_num':
            validation_params['search_str'] = {
                'symbol_set': 'd',
                # 'allowed': '-ПФ',
                'required': True,
            }
        elif self.action == 'search_by_place':
            validation_params['search_str'] = {
                'symbol_set': 'w',
                'allowed': '-_*()',
                'required': True,
            }
        validation_params['page'] = {
            'symbol_set': 'd',
            'allowed': '',
            'default_value': 1,
        }

        for item in actions[self.action]:
            if type(item) is not tuple:
                self.post_params[item] = self.request.POST.get(item)
            else:
                self.post_params[item[0]] = self.request.POST.get(item[1])
        return validation(self.post_params, validation_params)

    def search_by_inv_num(self):
        self.context['items'] = []
        for prefix in InventoryNumberPrefix.objects.filter(for_item='Printers'):
            fixed_number = mask_validation(prefix.inventory_number_mask, self.post_params['search_str'])
            try:
                printer = PrinterItem.objects.get(
                    office=self.office,
                    prefix=prefix,
                    inventory_number=fixed_number
                )
                self.context['items'].append(printer)
            except ObjectDoesNotExist:
                continue
        if len(self.context['items']) == 1:
            self.context['redirect'] = reverse('printer_item', kwargs={'printer_item_id': self.context['items'][0].id})

    def search_by_place(self):
        pass
        # self.context['paginator'], self.context['items'] = self.get_pagination(printers_list,
        #                                                                        self.post_params['page'], 6)

    def get_post_context(self):
        if self.action == 'search_by_inv_num':
            self.search_by_inv_num()
        elif self.action == 'search_by_place':
            self.search_by_place()

    @staticmethod
    def get_pagination(list_of_items, active_page, num_per_page):
        paginator = Paginator(list_of_items, num_per_page)
        page = paginator.get_page(active_page)
        return paginator, page




