from django.conf.urls import url
from printers.views import PrintersListView, PrinterView, PrinterItemView


urlpatterns = [
    url(
        regex=r'^$',
        view=PrintersListView.as_view(),
        name='printers'
    ),
    url(
        regex=r'^(?P<printer_id>\d{1,10})$',
        view=PrinterView.as_view(),
        name='printer'
    ),
    url(
        regex=r'^printer_item/(?P<printer_item_id>\d{1,10})$',
        view=PrinterItemView.as_view(),
        name='printer_item'
    ),
]
