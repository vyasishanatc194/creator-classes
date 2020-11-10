from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking
from . import Creator

class OneToOneSession(ActivityTracking):
    creator = models.ForeignKey("Creator", on_delete=models.CASCADE, related_name="sessioncreator")
    amount = models.FloatField(blank=True, null=True, default=50)

    def __str__(self):
        return f"{self.creator.email}"

    class Meta:
        verbose_name = "Creator OneToOne Session"
        verbose_name_plural = "Creator OneToOne Sessions"
        ordering = ["-created_at"]

class TimeSlot(ActivityTracking):
    session = models.ForeignKey("OneToOneSession", on_delete=models.CASCADE, related_name="sessiontimeslot")
    slot_datetime = models.DateTimeField(auto_now_add=False)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.session.creator.email} | {self.slot_datetime}"

    class Meta:
        verbose_name = "OneToOne Session Time Slot"
        verbose_name_plural = "OneToOne Session Time Slots"
        ordering = ["-created_at"]
