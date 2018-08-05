from django.conf.urls import url
from printer_spares.views import AddCartridgeTemplateView

urlpatterns = [
    url(
        regex=r'^add_cartridge$',
        view=AddCartridgeTemplateView.as_view(),
        name='add_cartridge'
    ),
]
