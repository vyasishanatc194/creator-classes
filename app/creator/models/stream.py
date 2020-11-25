from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking


class Stream(ActivityTracking):
    creator = models.ForeignKey("Creator", on_delete=models.CASCADE, related_name="stream_by")
    title = models.CharField(max_length=200, blank=True, null=True, default='')
    thumbnail_file = models.FileField(upload_to="stream", null=True,  blank=True, verbose_name=_("Stream thumbnail"))
    sneak_peak_file = models.FileField(upload_to="stream", null=True,  blank=True, verbose_name=_("Stream sneak peak"))
    stream_datetime = models.DateTimeField(null=True, blank=True, help_text=_("Stream Datetime"), verbose_name=_("Stream Datetime"))
    stream_amount = models.FloatField(blank=True, null=True, default=10)
    total_seats = models.IntegerField(blank=True, null=True, default=10)

    def __str__(self):
        return f"{self.creator.username} | {self.title} "

    class Meta:
        verbose_name = "Creator Stream"
        verbose_name_plural = "Creator Streams"
        ordering = ["-created_at"]


class StreamKeyword(ActivityTracking):
    keyword = models.ForeignKey("customadmin.AdminKeyword", on_delete=models.CASCADE, null=True, blank=True)
    stream = models.ForeignKey("Stream", on_delete=models.CASCADE, related_name="stream_keywords")

    def __str__(self):
        return f"{self.keyword}"

    class Meta:
        verbose_name = "Stream Keyword"
        verbose_name_plural = "Stream Keywords"
        ordering = ["-created_at"]


class StreamCovers(ActivityTracking):
    covers = models.CharField(max_length=255, blank=True, null=True, default='')
    stream = models.ForeignKey("Stream", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.covers}"

    class Meta:
        verbose_name = "Stream Cover"
        verbose_name_plural = "Stream Covers"
        ordering = ["-created_at"]
