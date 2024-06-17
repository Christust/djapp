from django.db import models
from apps.base.models import Base
from apps.branches.models import Branch
from apps.users.models import User


# Create your models here.
class Store(Base):
    name = models.CharField("Name", max_length=50, blank=False, null=False)
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, blank=False, null=False
    )

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"


class Item(Base):
    class Units(models.TextChoices):
        UNITS = "units"
        METERS = "meters"
        LITERS = "liters"

    name = models.CharField("Name", max_length=50, blank=False, null=False)
    description = models.CharField(
        "Description", max_length=50, blank=False, null=False
    )
    brand = models.CharField("Brand", max_length=50, blank=False, null=False)
    barcode = models.CharField("Barcode", max_length=50, blank=False, null=False)
    consumable = models.BooleanField("Consumable", default=False)
    units = models.CharField(
        "Units", max_length=20, choices=Units.choices, blank=False, null=False
    )

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"


class Stock(Base):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=False, null=False)
    amount = models.IntegerField("Amount", blank=False, null=False)

    def natural_key(self):
        return self.item

    def __str__(self):
        return f"{self.store} - {self.item}"

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

        # Unico item por store
        unique_together = ('store', 'item')


class MaterialRequest(Base):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, blank=False, null=False, default=1
    )
    finished = models.BooleanField("Finished", default=False)

    def natural_key(self):
        return self.store

    def __str__(self):
        return f"{self.store}"

    class Meta:
        verbose_name = "Material Request"
        verbose_name_plural = "Material Requests"


class MaterialRequirement(Base):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, blank=False, null=False, default=1
    )
    finished = models.BooleanField("Finished", default=False)

    def natural_key(self):
        return self.store

    def __str__(self):
        return f"{self.store}"

    class Meta:
        verbose_name = "Material Requirement"
        verbose_name_plural = "Material Requirements"


class ItemRequest(Base):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)
    material_request = models.ForeignKey(
        MaterialRequest, on_delete=models.CASCADE, blank=False, null=False
    )
    amount = models.IntegerField("Amount", blank=False, null=False)
    amount_returned = models.IntegerField(
        "Amount returned", blank=False, null=False, default=0
    )

    def natural_key(self):
        return self.item

    def __str__(self):
        return f"{self.item}"

    class Meta:
        verbose_name = "Item Request"
        verbose_name_plural = "Item Requests"


class ItemRequirement(Base):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=False, null=False)
    material_requirement = models.ForeignKey(
        MaterialRequirement, on_delete=models.CASCADE, blank=False, null=False
    )
    amount = models.IntegerField("Amount", blank=False, null=False)

    def natural_key(self):
        return self.item

    def __str__(self):
        return f"{self.item}"

    class Meta:
        verbose_name = "Item Requirement"
        verbose_name_plural = "Item Requirements"
