from django.contrib import admin
from . import models


class BranchAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "country", "state", "city"]


class StateAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "country"]


class CityAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "state"]


# Register your models here.
admin.site.register(models.Branch, BranchAdmin)
admin.site.register(models.Country)
admin.site.register(models.State, StateAdmin)
admin.site.register(models.City, CityAdmin)
