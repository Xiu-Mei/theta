from django.db import models

from devices.models import Url, Contractor
from location.models import Office


class Index(models.Model):
    index = models.CharField(max_length=512, unique=True)

    def __str__(self):
        return str(self.index)


class KindOfSpare(models.Model):
    name = models.CharField(max_length=512, unique=True)

    def __str__(self):
        return str(self.name)


class Spare(models.Model):
    indexes = models.ManyToManyField(Index)
    printers = models.ManyToManyField('printers.Printer')
    kind_of_spare = models.ForeignKey(KindOfSpare, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='images/spares', default='spare.png')
    urls = models.ManyToManyField(Url, blank=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.indexes.all()[0], self.kind_of_spare, self.printers.all()[0])


class SpareItem(models.Model):
    spare = models.ForeignKey(Spare, on_delete=models.PROTECT)
    office = models.ForeignKey(Office, on_delete=models.PROTECT)
    contractors = models.ManyToManyField(Contractor, blank=True)
    in_stock = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} {} {} pieces'.format(self.spare.printers.all()[0], self.spare.kind_of_spare, self.in_stock)


COLOR_CHOICES = (
    ('black', 'black'),
    ('cyan', 'cyan'),
    ('magenta', 'magenta'),
    ('yellow', 'yellow'),
    ('multicolor', 'multicolor'),
)


class Cartridge(models.Model):
    name = models.CharField(max_length=512, unique=True)
    printers = models.ManyToManyField('printers.Printer')
    image = models.ImageField(upload_to='images/cartridges', default='cartridge.png')
    capacity = models.IntegerField(default=0)
    urls = models.ManyToManyField(Url, blank=True)
    comment = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=32, choices=COLOR_CHOICES, default='black')

    def __str__(self):
        return str(self.name)


class CartridgeItem(models.Model):
    cartridge = models.ForeignKey(Cartridge, on_delete=models.PROTECT)
    office = models.ForeignKey(Office, on_delete=models.PROTECT)
    contractors = models.ManyToManyField(Contractor, blank=True)
    in_stock = models.IntegerField(default=0)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.cartridge)
