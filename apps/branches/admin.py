from django.contrib import admin
from apps.branches.models import Branch, Country, State, City

# Register your models here.
admin.site.register(Branch)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)