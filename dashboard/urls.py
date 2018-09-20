from django.conf.urls import url
from dashboard.views import MainAdminView

urlpatterns = [
    url(
        regex=r'^$',
        view=MainAdminView.as_view(),
        name='main_admin'
    ),
]
