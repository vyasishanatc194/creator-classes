from django.db import models
from creator_class.models import ActivityTracking


class CreatorReview(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="review_by_user")
    creator = models.ForeignKey("creator.Creator", on_delete=models.CASCADE, related_name="review_for_creator")
    review = models.CharField(max_length=255, blank=True, null=True, default='')
    rating = models.FloatField(blank=True, null=True, default=0)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Creator Review"
        verbose_name_plural = "Creator reviews"
        ordering = ["-created_at"]


class ClassReview(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="class_review_by_user")
    creator_class = models.ForeignKey("creator.CreatorClass", on_delete=models.CASCADE, related_name="review_for_class")
    review = models.CharField(max_length=255, blank=True, null=True, default='')
    rating = models.FloatField(blank=True, null=True, default=1)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Class Review"
        verbose_name_plural = "Class reviews"
        ordering = ["-created_at"]