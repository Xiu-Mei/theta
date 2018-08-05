from django.contrib import admin
from printer_spares.models import Index, Spare, Cartridge, KindOfSpare, SpareItem

admin.site.register(Index)
admin.site.register(KindOfSpare)
admin.site.register(Spare)
admin.site.register(SpareItem)
admin.site.register(Cartridge)
# admin.site.register(CartridgeItem)
