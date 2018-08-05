from django.contrib import admin
from printers.models import Printer, PrinterItem, PrinterRepairJob, PrinterChangeCartridgeJob


class PrinterAdmin(admin.ModelAdmin):
    exclude = ('device', )


admin.site.register(Printer, PrinterAdmin)
admin.site.register(PrinterItem)
admin.site.register(PrinterRepairJob)
admin.site.register(PrinterChangeCartridgeJob)
