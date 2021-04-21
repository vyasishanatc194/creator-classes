from django.db import models
from creator_class.models import ActivityTracking
from django.utils.translation import gettext as _


class Notification(ActivityTracking):
    TYPES_CHOICES = (
        ("OTHER", _("OTHER")),
        ("BOOKING", _("BOOKING")),
    )
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default="",
        help_text=_("Notification Title"),
        verbose_name=_("Title"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Notification Description"),
        verbose_name=_("Description"),
    )
    stream = models.ForeignKey("creator.Stream", on_delete=models.CASCADE, null=True, blank=True, related_name="notification_stream")
    user = models.ForeignKey(
        "User", related_name="user_notification", on_delete=models.CASCADE
    )
    is_read = models.BooleanField(
        default=False,
        help_text=_("Is Notification Read?"),
        verbose_name=_("Is Notification Read?"),
    )
    notification_type = models.CharField(
        max_length=255,
        choices=TYPES_CHOICES,
        null=True,
        blank=True,
        help_text=_("Notification Title"),
        verbose_name=_("Title"),
    )
    profile_image = models.ImageField(upload_to="profile_image", default="sample.jpg", null=True,  blank=True, verbose_name=_("Profile Image"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ["-created_at"]