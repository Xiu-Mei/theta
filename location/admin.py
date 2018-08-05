from django.contrib import admin
from location.models import Office, Building, Floor, Place, Room


class BuildingAdmin(admin.ModelAdmin):
    fields = ('name', 'comment', 'image',)

    def save_model(self, request, obj, form, change):
        obj.office = request.user.office
        super().save_model(request, obj, form, change)


class RoomAdmin(admin.ModelAdmin):
    fields = ('name', 'additional_name', 'image',)

    def save_model(self, request, obj, form, change):
        obj.office = request.user.office
        super().save_model(request, obj, form, change)


admin.site.register(Office)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Floor)
admin.site.register(Room, RoomAdmin)
admin.site.register(Place)
