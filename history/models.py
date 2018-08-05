from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

from location.models import Office
from printer_spares.models import CartridgeItem

ACTION_CHOICES = (
    ('create', 'create'),
    ('income', 'income'),
    ('delivery', 'delivery'),
    ('consumption', 'consumption'),
)


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class CartridgeItemHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    cartridge_item = models.ForeignKey(CartridgeItem, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    action = models.CharField(max_length=32, choices=ACTION_CHOICES, default='create')
    message = models.CharField(max_length=32, blank=True)

    def message_as_list(self):
        return self.message.split(' ')
