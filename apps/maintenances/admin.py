from django.contrib import admin
from apps.maintenances.models import MaintenanceReport, MaintenanceRequest, MaintenanceType

# Register your models here.
admin.site.register(MaintenanceType)
admin.site.register(MaintenanceReport)
admin.site.register(MaintenanceRequest)