from django.db import models


class Office(models.Model):
    name = models.CharField(max_length=512, unique=True)  # Moscow office
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Building(models.Model):
    office = models.ForeignKey(Office, on_delete=models.PROTECT)
    name = models.CharField(max_length=512, unique=True)  # Angar
    comment = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/buildings',
                              default='images/buildings/default_building.png')

    def __str__(self):
        return '{} {} {}'.format(self.office, self.id, self.name)


class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.PROTECT, default=1)
    name = models.CharField(max_length=512, unique=True)  # first floor
    comment = models.TextField(blank=True, null=True)
    plan = models.ImageField(upload_to='images/plans',
                             default='images/plans/default_plan.png')

    def __str__(self):
        return '{} {} {comment}'.format(self.building, self.name, comment=self.comment[:12])


class Room(models.Model):
    office = models.ForeignKey(Office, on_delete=models.PROTECT)
    name = models.CharField(max_length=512, unique=True)  # room: 402a
    additional_name = models.CharField(max_length=512, blank=True, null=True)
    image = models.ImageField(upload_to='images/rooms',
                              default='images/rooms/default_room.png')

    def __str__(self):
        return '{} {} {}'.format(self.office, self.name, self.additional_name)


class Place(models.Model):
    floor = models.ForeignKey(Floor, blank=True, null=True, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=512)  # Ivanov or place 4a
    left = models.IntegerField(verbose_name='coordinate left', default=0)
    top = models.IntegerField(verbose_name='coordinate top', default=0)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.floor, self.name)
