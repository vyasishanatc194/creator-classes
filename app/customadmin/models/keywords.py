from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking


class AdminKeyword(ActivityTracking):
    keyword = models.CharField(max_length=55, blank=False, null=False, default='')

    def __str__(self):
        return f"{self.keyword}"

    class Meta:
        verbose_name = "Admin Keyword"
        verbose_name_plural = "Admin Keywords"
        ordering = ["-created_at"]
