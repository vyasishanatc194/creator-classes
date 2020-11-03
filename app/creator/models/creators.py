from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking
from user.models import User


class Creator(User):
    key_skill = models.CharField(max_length=40, blank=True, null=True, default='')
    instagram_url = models.CharField(max_length=40, blank=True, null=True, default='')
    linkedin_url = models.CharField(max_length=40, blank=True, null=True, default='')
    twitter_url = models.CharField(max_length=40, blank=True, null=True, default='')
    google_url = models.CharField(max_length=40, blank=True, null=True, default='')
    facebook_url = models.CharField(max_length=40, blank=True, null=True, default='')

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
