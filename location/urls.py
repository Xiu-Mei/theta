from django.conf.urls import url
from location.views import LocationTemplateView, FloorTemplateView

urlpatterns = [
    url(
        regex=r'^$',
        view=LocationTemplateView.as_view(),
        name='location',
    ),
    url(
        regex=r'^building/(?P<building_id>\d{1,10})/floor/(?P<floor_id>\d{1,10})$',
        view=FloorTemplateView.as_view(),
        name='floor',
    ),
]
