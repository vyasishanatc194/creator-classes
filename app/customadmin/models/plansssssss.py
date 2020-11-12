from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking


class Plan(ActivityTracking):
    plan_title = models.CharField(max_length=55, blank=False, null=False, default='')
    plan_price = models.FloatField()

    def __str__(self):
        return f"{self.plan_title}"

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["-created_at"]

class PlanBenefit(ActivityTracking):
    plan = models.ForeignKey("Plan", on_delete=models.CASCADE)
    benefit_title = models.CharField(max_length=55, blank=False, null=False, default='')

    def __str__(self):
        return f"{self.plan}"

    class Meta:
        verbose_name = "Plan Benefit"
        verbose_name_plural = "Plan Benefits"
        ordering = ["-created_at"]
