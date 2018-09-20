from django import forms
from django.contrib import admin
from devices.models import Device, Manufacturer, Contractor, Url, InventoryNumberPrefix


class InventoryNumberPrefixForm(forms.ModelForm):
    class Meta:
        model = InventoryNumberPrefix
        fields = '__all__'

    def clean(self):
        allowed = ['w', 'd', '-']
        error_message = "Inventory number mask can contain only 'w', 'd' or '-' letters. For Example: wwdddd"
        inventory_number_mask = self.cleaned_data.get('inventory_number_mask')
        for i in allowed:
            inventory_number_mask = inventory_number_mask.replace(i, '')
        if inventory_number_mask:
            self.add_error('inventory_number_mask', error_message)


class InventoryNumberPrefixAdmin(admin.ModelAdmin):
    form = InventoryNumberPrefixForm
    list_display = ('for_item', 'prefix', 'inventory_number_mask')


class ManufacturerAdminForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        widgets = {
            'image': forms.FileInput(
                                attrs={
                                    'accept': "image/*",
                                })
        }
        fields = '__all__'


class ManufacturerAdmin(admin.ModelAdmin):
    form = ManufacturerAdminForm


admin.site.register(Device)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Contractor)
admin.site.register(Url)
admin.site.register(InventoryNumberPrefix, InventoryNumberPrefixAdmin)
