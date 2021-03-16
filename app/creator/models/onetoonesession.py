from django.db import models
from creator_class.models import ActivityTracking

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
    tz = models.ForeignKey("customadmin.AvailableTimezone", on_delete=models.CASCADE, related_name="selected_timezones", blank=True, null=True)
    is_booked = models.BooleanField(default=False)
    agora_token = models.CharField(null=True, blank=True, max_length=255)
    completed = models.BooleanField(default=False)
    agora_uid = models.CharField(null=True, blank=True, max_length=255)
    channel_name = models.CharField(null=True, blank=True, max_length=255)
    token_created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.session.creator.email} | {self.slot_datetime}"

    class Meta:
        verbose_name = "OneToOne Session Time Slot"
        verbose_name_plural = "OneToOne Session Time Slots"
        ordering = ["-created_at"]
