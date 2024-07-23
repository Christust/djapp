from django.contrib import admin
from apps.stores.models import Store, Stock, Item, MaterialRequest, StockRequest, MaterialRequirement, StockRequirement

# Register your models here.
admin.site.register(Store)
admin.site.register(Stock)
admin.site.register(Item)
admin.site.register(MaterialRequest)
admin.site.register(StockRequest)
admin.site.register(MaterialRequirement)
admin.site.register(StockRequirement)