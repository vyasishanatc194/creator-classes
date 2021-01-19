from django.db import models
from creator_class.models import ActivityTracking


class CreatorClassCommission(ActivityTracking):
    affiliation_deduction =  models.PositiveIntegerField(default=10, blank=True, null=True)
    creator_class_deduction =  models.PositiveIntegerField(default=10, blank=True, null=True)

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Creator Classes Commission"
        verbose_name_plural = "Creator Classes Commission"
        ordering = ["-created_at"]