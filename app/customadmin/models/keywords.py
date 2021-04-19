from django.db import models
from creator_class.models import ActivityTracking


class AdminKeyword(ActivityTracking):
    keyword = models.CharField(max_length=55, blank=False, null=False, default='')
    image = models.ImageField(upload_to='keyword/', blank=True, null=True)

    def __str__(self):
        return f"{self.keyword}"

    class Meta:
        verbose_name = "Admin Keyword"
        verbose_name_plural = "Admin Keywords"
        ordering = ["-created_at"]


class AvailableTimezone(ActivityTracking):
    tz = models.CharField(max_length=10, blank=False, null=False, default='')

    def __str__(self):
        return f"{self.tz}"

    class Meta:
        verbose_name = "Timezone"
        verbose_name_plural = "Timezones"
        ordering = ["-created_at"]
