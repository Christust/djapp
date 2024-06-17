from django.db import models


# Create your models here.
class Base(models.Model):
    id = models.AutoField(primary_key=True)
    is_active = models.BooleanField("Status", default=True)
    created_at = models.DateField("Creation date", auto_now_add=True)
    modified_at = models.DateField("Modification date", auto_now=True)
    deleted_at = models.DateField("Deletion date", null=True, blank=True)

    class Meta:
        abstract = True
        verbose_name = "Base Model"
        verbose_name_plural = "Base Models"