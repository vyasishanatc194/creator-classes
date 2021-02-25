from django.db import models
from creator_class.models import ActivityTracking


class Plan(ActivityTracking):
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    plan_amount = models.FloatField(blank=True, null=True, default=1)
    duration_in_months = models.IntegerField(blank=True, null=True, default=1)
    stripe_plan_id = models.CharField(max_length=200, blank=True, null=True, default='')
    paypal_plan_id = models.CharField(max_length=200, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["-created_at"]


class PlanCover(ActivityTracking):
    covers = models.CharField(max_length=255, blank=True, null=True, default='')
    plan = models.ForeignKey("Plan", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plan.name}"

    class Meta:
        verbose_name = "Plan Cover"
        verbose_name_plural = "Plan Covers"
        ordering = ["-created_at"]