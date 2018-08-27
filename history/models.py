from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

from location.models import Office
from printer_spares.models import CartridgeItem, SpareItem

ACTION_CHOICES = (
    ('create', 'create'),
    ('income', 'income'),
    ('delivery', 'delivery'),
    ('consumption', 'consumption'),
)


class ItemHistoryMixin():

    def message_as_list(self):
        return self.message.split(' ')


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class CartridgeItemHistory(ItemHistoryMixin, models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True)
    cartridge_item = models.ForeignKey(CartridgeItem, on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    action = models.CharField(max_length=32, choices=ACTION_CHOICES, default='create')
    message = models.CharField(max_length=512, blank=True)


class SpareItemHistory(ItemHistoryMixin, models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True)
    spare_item = models.ForeignKey(SpareItem, on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(auto_now_add=True, blank=True)
    action = models.CharField(max_length=32, choices=ACTION_CHOICES, default='create')
    message = models.CharField(max_length=512, blank=True)
