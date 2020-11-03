from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking


class CreatorReview(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="review_by_user")
    creator = models.ForeignKey("creator.Creator", on_delete=models.CASCADE, related_name="review_for_creator")
    review = models.CharField(max_length=255, blank=True, null=True, default='')
    rating = models.FloatField(blank=True, null=True, default=1)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Creator Review"
        verbose_name_plural = "Creator reviews"
        ordering = ["-created_at"]