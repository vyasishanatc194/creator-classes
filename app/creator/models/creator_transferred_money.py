from django.db import models

# ----------------------------------------------------------------------
# CreatorTransferredMoney Model
# ----------------------------------------------------------------------


class CreatorTransferredMoney(models.Model):

    """This model stores the data into CreatorTransferredMoney table in db"""

    STATUS_CHOICES = [("success", "Success"), ("fail", "Fail")]
    creator = models.ForeignKey(
        "creator.Creator",
        on_delete=models.CASCADE,
        related_name="creator_user",
        null=True,
        blank=True,
    )
    creator_earnings = models.PositiveIntegerField(default=0, blank=True, null=True)
    creator_class_deduction = models.PositiveIntegerField(default=0, blank=True, null=True)
    affiliation_commission_total = models.PositiveIntegerField(default=0, blank=True, null=True)
    affiliation_deduction = models.PositiveIntegerField(default=0, blank=True, null=True)
    final_earning_amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    final_commission_amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    transferred_amount= models.PositiveIntegerField(default=0, blank=True, null=True)
    stream_amount_total = models.FloatField(default=0, blank=True, null=True)
    stream_amount_received = models.FloatField(default=0, blank=True, null=True)
    session_amount_total = models.FloatField(default=0, blank=True, null=True)
    session_amount_received = models.FloatField(default=0, blank=True, null=True)


    status = models.CharField(
        max_length=222, blank=True, null=True, choices=STATUS_CHOICES, default="fail"
    )
    transaction_id = models.CharField(
        max_length=222,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Creator Transferred Money"
        verbose_name_plural = "Creator Transferred Money"

    def __str__(self):
        return "{0}".format(self.transfer_amount)
