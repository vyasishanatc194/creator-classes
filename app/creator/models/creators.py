from django.db import models
from creator_class.models import ActivityTracking
from django.utils.translation import gettext as _
from user.models import User

STATUS_CHOICE = (
    ('REJECT', "Rejected"),
    ('PENDING', "Pending"),
    ('ACCEPT', "Accepted")
)
class Creator(User):
    status = models.CharField(max_length=7,choices=STATUS_CHOICE, default='PENDING')
    key_skill = models.CharField(max_length=40, blank=True, null=True, default='')
    instagram_url = models.CharField(max_length=40, blank=True, null=True, default='')
    linkedin_url = models.CharField(max_length=40, blank=True, null=True, default='')
    twitter_url = models.CharField(max_length=40, blank=True, null=True, default='')
    google_url = models.CharField(max_length=40, blank=True, null=True, default='')
    facebook_url = models.CharField(max_length=40, blank=True, null=True, default='')
    creator_website_url = models.CharField(max_length=40, blank=True, null=True, default='')
    affiliation_link = models.CharField(max_length=255, blank=True, null=True, default='')


    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Creator"
        verbose_name_plural = "Creators"
        ordering = ["-created_at"]


class CreatorSkill(ActivityTracking):
    skill = models.CharField(max_length=40, blank=True, null=True, default='')
    creator = models.ForeignKey("Creator", on_delete=models.CASCADE, related_name="creator")

    def __str__(self):
        return f"{self.creator.email}"

    class Meta:
        verbose_name = "Creator skill"
        verbose_name_plural = "Creator skills"
        ordering = ["-created_at"]


class CreatorAffiliation(ActivityTracking):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="affiliated_user")
    plan_id = models.ForeignKey("customadmin.Plan", on_delete=models.CASCADE, related_name="user")
    amount = models.FloatField(blank=True, null=True)
    transfer_amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    commission_amount = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Creator Affiliation"
        verbose_name_plural = "Creator Affiliation"
        ordering = ["-created_at"]


class PayoutErrorLog(ActivityTracking):
    error_text = models.TextField(blank=True, null=True, default='')
    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Payout Error Log"
        verbose_name_plural = "Payout Error Logs"
        ordering = ["-created_at"]