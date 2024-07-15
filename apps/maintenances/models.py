from django.db import models
from apps.base.models import Base
from apps.users.models import User
from apps.branches.models import Branch
from simple_history.models import HistoricalRecords


# Create your models here.
class MaintenanceType(Base):
    type = models.CharField("Type", max_length=20, null=False, blank=False)
    description = models.TextField("Description", null=True, blank=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def natural_key(self):
        return self.type

    def __str__(self):
        return f"{self.type} - {self.description}"

    class Meta:
        verbose_name = "Maintenance type"
        verbose_name_plural = "Maintenance types"


class MaintenanceRequest(Base):
    class Status(models.TextChoices):
        PENDING = "pending"
        IN_PROGRESS = "in_progress"
        FINISHED = "finished"
        CANCELED = "canceled"

    description = models.CharField(
        "Description", max_length=25, null=False, blank=False
    )
    status = models.CharField(
        "Status",
        max_length=20,
        choices=Status.choices,
        null=True,
        blank=True,
        default=Status.PENDING,
    )
    maintenance_type = models.ForeignKey(
        MaintenanceType, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    feedback = models.CharField("Feedback", max_length=30, null=True, blank=True)

    cancel_note = models.CharField("Cancel note", max_length=35, null=True, blank=True)

    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, null=False, blank=False
    )
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def natural_key(self):
        return self.description

    def __str__(self):
        return f"{self.status} - {self.description}"

    class Meta:
        verbose_name = "Maintenance request"
        verbose_name_plural = "Maintenance requests"


class MaintenanceReport(Base):
    description = models.CharField(
        "Description", max_length=25, null=False, blank=False
    )
    maintenance_request = models.ForeignKey(
        MaintenanceRequest, on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def natural_key(self):
        return self.description

    def __str__(self):
        return f"{self.description}"

    class Meta:
        verbose_name = "Maintenance report"
        verbose_name_plural = "Maintenance reports"
