from django.db import models
from creator_class.models import ActivityTracking


class FavouriteCreator(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="favourite_by")
    creator = models.ForeignKey("creator.Creator", on_delete=models.CASCADE, related_name="favourite_creator")

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Favourite Creator"
        verbose_name_plural = "Favourite Creators"
        ordering = ["-created_at"]


class FavouriteClass(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="favourite_by_user")
    creator_class = models.ForeignKey("creator.CreatorClass", on_delete=models.CASCADE, related_name="favourite_class")

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Favourite Class"
        verbose_name_plural = "Favourite Classes"
        ordering = ["-created_at"]