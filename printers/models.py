from django.db import models

from devices.models import Device, Manufacturer, Contractor, InventoryNumberPrefix
from location.models import Office, Place
from printer_spares.models import Spare


TYPE_CHOICES = (
    ('laser', 'laser'),
    ('ink', 'ink'),
)


class Printer(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT, default=1)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)

    name = models.CharField(max_length=512, unique=True, verbose_name='Name')  # like LaserJet 2014
    image = models.ImageField(upload_to='images/printers', default='/images/printers/printer.png')
    mfp = models.BooleanField(default=False)
    duplex = models.BooleanField(default=False)
    usb = models.BooleanField(default=True)
    ethernet = models.BooleanField(default=False)
    wireless = models.BooleanField(default=False)
    color = models.BooleanField(default=False)
    type = models.CharField(max_length=32, choices=TYPE_CHOICES, default='laser')
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '{} {}'.format(self.manufacturer, self.name)


class PrinterItem(models.Model):
    printer = models.ForeignKey(Printer, on_delete=models.PROTECT)
    office = models.ForeignKey(Office, on_delete=models.PROTECT)
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    prefix = models.ForeignKey(InventoryNumberPrefix, on_delete=models.PROTECT, blank=True, null=True)
    inventory_number = models.CharField(verbose_name='inventory number', max_length=32)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} {}{}'.format(self.printer.name, self.prefix.prefix, self.inventory_number)

# JOBS


RESULT_CHOICES = (
    ('success', 'success'),
    ('fail', 'fail'),
    ('partial', 'partial'),
)


class PrinterRepairJob(models.Model):
    printer_item = models.ForeignKey(PrinterItem, on_delete=models.PROTECT)
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT)
    date_time = models.DateTimeField()
    total_printed_sheets = models.IntegerField(verbose_name='total printed sheets')
    result = models.CharField(max_length=32, choices=RESULT_CHOICES, default='success')
    spares = models.ManyToManyField(Spare)
    comment = models.TextField(blank=True, null=True)


class PrinterChangeCartridgeJob(models.Model):
    printer_item = models.ForeignKey(PrinterItem, on_delete=models.PROTECT)
    date_time = models.DateTimeField()
    printed_sheets = models.IntegerField(blank=True, null=True, verbose_name='printed sheets')
