from django.db import models
from creator_class.models import ActivityTracking
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from django.db import models
from creator_class.utils import MyStripe


class Plan(ActivityTracking):
    name = models.CharField(max_length=200, blank=True, null=True, default='')
    plan_amount = models.FloatField(blank=True, null=True, default=1)
    discount_amount = models.FloatField(blank=True, null=True)
    duration_in_months = models.IntegerField(blank=True, null=True, default=1)
    stripe_plan_id = models.CharField(max_length=200, blank=True, null=True, default='')
    stripe_product_id = models.CharField(max_length=222 ,blank=True, null=True)
    paypal_plan_id = models.CharField(max_length=200, blank=True, null=True, default='')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["-created_at"]


@receiver(pre_delete, sender=Plan)
def delete_img_pre_delete_post(sender, instance, *args, **kwargs):
    exist = Plan.objects.filter(stripe_plan_id=instance.id).exists()
    if not exist:
        stripe = MyStripe()
        if instance.stripe_plan_id:
            stripe.deletePlan(instance.stripe_plan_id)
            stripe.deleteProduct(instance.stripe_product_id)
            return


@receiver(post_save, sender=Plan)
def create_plan(sender, instance, created, **kwargs):
    print('signal started')
    stripe = MyStripe()
    if created:
        plan_duration = instance.duration_in_months
        product_obj = stripe.createProduct(instance.name)
        if (plan_duration < 6):
            plan_id = stripe.createPlan(
                int(instance.plan_amount) * 100, "month", product_obj["id"]
            )
        if (plan_duration == 6):
            plan_id = stripe.createPlan(
                int(instance.plan_amount) * 100, "month", product_obj["id"], 6
            )
        if (plan_duration > 6):
            plan_id = stripe.createPlan(
                int(instance.plan_amount) * 100, "month", product_obj["id"], 12
            )
        instance.stripe_plan_id = plan_id["id"]
        instance.stripe_product_id = product_obj["id"]
        instance.save()
        return


@receiver(post_save, sender=Plan)
def update_plan(sender, instance, created, **kwargs):
    stripe = MyStripe()
    if not created and instance.stripe_product_id:
        stripe.modifyProduct(instance.stripe_product_id, instance.name)
        return


class PlanCover(ActivityTracking):
    covers = models.CharField(max_length=255, blank=True, null=True, default='')
    plan = models.ForeignKey("Plan", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.plan.name}"

    class Meta:
        verbose_name = "Plan Cover"
        verbose_name_plural = "Plan Covers"
        ordering = ["-created_at"]
