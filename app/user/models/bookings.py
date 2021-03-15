from django.db import models
from django.utils.translation import gettext as _
from creator_class.models import ActivityTracking


class SessionBooking(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="booking_by")
    creator = models.ForeignKey("creator.Creator", on_delete=models.CASCADE, related_name="booking_with")
    time_slot = models.ForeignKey("creator.TimeSlot", on_delete=models.CASCADE, related_name="booking_slot")
    card_id = models.CharField(null=True, blank=True, max_length=255)
    transaction_detail = models.ForeignKey("user.TransactionDetail", on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=255)
    agora_token = models.CharField(null=True, blank=True, max_length=255)
    completed = models.BooleanField(default=False)
    agora_uid = models.CharField(null=True, blank=True, max_length=255)
    channel_name = models.CharField(null=True, blank=True, max_length=255)


    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Session booking"
        verbose_name_plural = "Session bookings"
        ordering = ["-created_at"]


class BookedSessionKeywords(ActivityTracking):
    session = models.ForeignKey(SessionBooking, on_delete=models.CASCADE, related_name="booking_slot")
    keyword = models.ForeignKey("customadmin.AdminKeyword", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.session.pk}"

    class Meta:
        verbose_name = "Session booking keyword"
        verbose_name_plural = "Session booking keywords"
        ordering = ["-created_at"]



class StreamBooking(ActivityTracking):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="stream_booking_by")
    stream = models.ForeignKey("creator.Stream", on_delete=models.CASCADE, related_name="booked_stream")
    card_id = models.CharField(null=True, blank=True, max_length=255)
    transaction_detail = models.ForeignKey("user.TransactionDetail", on_delete=models.CASCADE, null=True, blank=True)
    agora_token = models.CharField(null=True, blank=True, max_length=255)
    completed = models.BooleanField(default=False)
    agora_uid = models.CharField(null=True, blank=True, max_length=255)
    channel_name = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        verbose_name = "Stream booking"
        verbose_name_plural = "Stream bookings"
        ordering = ["-created_at"]
