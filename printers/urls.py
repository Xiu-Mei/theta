from django.conf.urls import url
from printers.views import PrintersListView, PrinterView


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
]
