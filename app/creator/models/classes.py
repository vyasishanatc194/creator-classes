from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking
from creator.models import Creator


class CreatorClass(ActivityTracking):
    creator = models.ForeignKey("Creator", on_delete=models.CASCADE, related_name="class_by")
    title = models.CharField(max_length=200, blank=True, null=True, default='')
    thumbnail_file = models.FileField(upload_to="class_content", null=True,  blank=True, verbose_name=_("class thumbnail"))
    class_file = models.FileField(upload_to="class_content", null=True,  blank=True, verbose_name=_("Class video"))

    def __str__(self):
        return f"{self.creator.username} | {self.title} "

    class Meta:
        verbose_name = "Creator Class"
        verbose_name_plural = "Creator Classes"
        ordering = ["-created_at"]


class ClassKeyword(ActivityTracking):
    keyword = models.CharField(max_length=40, blank=True, null=True, default='')
    creator_class = models.ForeignKey("CreatorClass", on_delete=models.CASCADE, related_name="keyword_for")

    def __str__(self):
        return f"{self.creator_class.title}"

    class Meta:
        verbose_name = "Class Keyword"
        verbose_name_plural = "Class Keywords"
        ordering = ["-created_at"]


class ClassCovers(ActivityTracking):
    covers = models.CharField(max_length=255, blank=True, null=True, default='')
    creator_class = models.ForeignKey("CreatorClass", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.creator_class.title}"

    class Meta:
        verbose_name = "Class Cover"
        verbose_name_plural = "Class Covers"
        ordering = ["-created_at"]