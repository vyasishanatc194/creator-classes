from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking


class SessionBooking(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="booking_by")
    creator = models.ForeignKey("creator.Creator", on_delete=models.CASCADE, related_name="booking_with")
    time_slot = models.ForeignKey("creator.TimeSlot", on_delete=models.CASCADE, related_name="booking_slot")

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Session booking"
        verbose_name_plural = "Session bookings"
        ordering = ["-created_at"]


class StreamBooking(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="stream_booking_by")
    stream = models.ForeignKey("creator.Stream", on_delete=models.CASCADE, related_name="booked_stream")

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Stream booking"
        verbose_name_plural = "Stream bookings"
        ordering = ["-created_at"]