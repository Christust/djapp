from django.db import models
from apps.base.models import Base


# Create your models here.
class Country(Base):
    name = models.CharField("Name", max_length=50, blank=False, null=False)

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class State(Base):
    name = models.CharField("Name", max_length=50, blank=False, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=False, null=False)

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"

class City(Base):
    name = models.CharField("Name", max_length=50, blank=False, null=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=False, null=False)

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

class Branch(Base):
    name = models.CharField("Name", max_length=50, blank=False, null=False)

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, blank=False, null=False
    )

    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=False, null=False)

    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False, null=False)

    def natural_key(self):
        return self.name

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
