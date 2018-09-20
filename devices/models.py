from django.db import models


class Device(models.Model):
    device_name = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to='images/devices', default='device.png')

    def __str__(self):
        return str(self.device_name)

    class Meta:
        verbose_name_plural = "Devices"


class Manufacturer(models.Model):
    name = models.CharField(max_length=512, unique=True)
    image = models.ImageField(upload_to='images/manufacturers',
                              default='manufacturer.png',
                              )

    def __str__(self):
        return str(self.name)


class Contractor(models.Model):
    name = models.CharField(max_length=512, unique=True)
    contact_info = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Url(models.Model):
    url = models.URLField()

    def __str__(self):
        return str(self.url)[:20]


class InventoryNumberPrefix(models.Model):
    # devices = models.ManyToManyField(Device)
    for_item = models.CharField(max_length=512, blank=True, null=True)
    prefix = models.CharField(max_length=512, blank=True, null=True)
    inventory_number_mask = models.CharField(max_length=128, default='ddd')  # wwdddd = ab0001, ab0002

    # def get_devices(self):
    #     return "\n".join([d.device_name for d in self.devices.all()])

    def __str__(self):
        return '{}{}'.format(self.prefix, self.inventory_number_mask)
