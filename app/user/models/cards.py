from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Card(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    card_id = CharField(_("Card Id"), max_length=255, blank=True)
    customer_id = CharField(_("Customer Id"), max_length=255, blank=True)
    last4 = CharField(_("Last 4 digits"), max_length=255, blank=True)
    brand = CharField(_("Brand of card"), max_length=255, blank=True)
    exp_month = CharField(_("Exp. month"), max_length=255, blank=True)
    exp_year = CharField(_("Exp. year"), max_length=255, blank=True)
    name = CharField(_("Card holder name"), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"

    def __str__(self):
        return "{0}".format(self.user)
