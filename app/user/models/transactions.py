"""This is a model module to store Charge data in to the database"""

from django.db.models import CharField, FloatField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from creator_class.models import ActivityTracking
import uuid

# ----------------------------------------------------------------------
# Charge Model
# ----------------------------------------------------------------------


class TransactionDetail(ActivityTracking):

    """This model stores the data into Charge table in db"""

    transaction_id = models.UUIDField(null=True, blank=True, default=uuid.uuid4)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    card_id = CharField(_("Card Id"), max_length=255, blank=True)
    customer_id = CharField(_("Customer Id"), max_length=255, blank=True)
    charge_id = CharField(_("Charge Id"), max_length=255, blank=True)
    charge_object = CharField(_("Object"), max_length=255, blank=True, null=True)
    amount = FloatField(_("Amount"), max_length=255, blank=True, null=True)
    amount_refunded = CharField(_("Amount refunded"), max_length=255, blank=True, null=True)
    application = CharField(_("Application"), max_length=255, blank=True, null=True)
    application_fee = CharField(_("Application fee"), max_length=255, blank=True, null=True)
    application_fee_amount = CharField(_("Application fee amount"), max_length=255, blank=True, null=True)
    balance_transaction = CharField(_("Balance transaction"), max_length=255, blank=True)
    address = CharField(_("Address"), max_length=255, blank=True, null=True)
    email = CharField(_("Email"), max_length=255, blank=True, null=True)
    name = CharField(_("Name"), max_length=255, blank=True, null=True)
    phone = CharField(_("Phone"), max_length=255, blank=True, null=True)
    calculated_statement_descriptor = CharField(_("Calculated statement descriptor"), max_length=255, blank=True, null=True)
    captured = models.BooleanField()
    created = CharField(_("Created"), max_length=255, blank=True, null=True)
    currency = CharField(_("Currency"), max_length=255, blank=True, null=True)
    customer = CharField(_("Customer"), max_length=255, blank=True, null=True)
    description = CharField(_("Description"), max_length=255, blank=True, null=True)
    disputed = models.BooleanField()
    failure_code = CharField(_("Failure code"), max_length=255, blank=True, null=True)
    failure_message = CharField(_("Failure message"), max_length=255, blank=True, null=True)
    fraud_details = CharField(_("Fraud details"), max_length=255, blank=True, null=True)
    invoice = CharField(_("Invoice"), max_length=255, blank=True, null=True)
    livemode = models.BooleanField()
    metadata = CharField(_("Metadata"), max_length=255, blank=True, null=True)
    on_behalf_of = CharField(_("On behalf of"), max_length=255, blank=True, null=True)
    order = CharField(_("Order"), max_length=255, blank=True, null=True)
    outcome = CharField(_("Outcome"), max_length=255, blank=True, null=True)
    paid = models.BooleanField()
    payment_intent = CharField(_("Payment intent"), max_length=255, blank=True, null=True)
    payment_method = CharField(_("Card Id"), max_length=255, blank=True)
    brand = CharField(_("Brand"), max_length=255, blank=True, null=True)
    address_line1_check = CharField(_("Address line1 check"), max_length=255, blank=True, null=True)
    address_postal_code_check = CharField(_("Address postal code check"), max_length=255, blank=True, null=True)
    cvc_check = CharField(_("CVC check"), max_length=255, blank=True, null=True)
    country = CharField(_("Country"), max_length=255, blank=True, null=True)
    exp_month = CharField(_("Exp month"), max_length=255, blank=True, null=True)
    exp_year = CharField(_("Exp year"), max_length=255, blank=True, null=True)
    fingerprint = CharField(_("Fingerprint"), max_length=255, blank=True, null=True)
    funding = CharField(_("Funding"), max_length=255, blank=True, null=True)
    installments = CharField(_("Installments"), max_length=255, blank=True, null=True)
    last4 = CharField(_("Last4 digit"), max_length=255, blank=True, null=True)
    network = CharField(_("Network"), max_length=255, blank=True, null=True)
    three_d_secure = CharField(_("3D secure"), max_length=255, blank=True, null=True)
    wallet = CharField(_("Wallet"), max_length=255, blank=True, null=True)
    charge_type = CharField(_("Type"), max_length=255, blank=True, null=True)
    receipt_email = CharField(_("Receipt email"), max_length=255, blank=True, null=True)
    receipt_number = CharField(_("Receipt number"), max_length=255, blank=True, null=True)
    receipt_url = CharField(_("Receipt URL"), max_length=255, blank=True, null=True)
    refunded = models.BooleanField()
    refunds_object = CharField(_("Refunds object"), max_length=255, blank=True, null=True)
    refunds_data = CharField(_("Refunds data"), max_length=255, blank=True, null=True)
    refunds_has_more = models.BooleanField()
    refunds_url = CharField(_("Refunds URL"), max_length=255, blank=True, null=True)
    review = CharField(_("Review"), max_length=255, blank=True, null=True)
    shipping = CharField(_("Shipping"), max_length=255, blank=True, null=True)
    source_transfer = CharField(_("Source transfer"), max_length=255, blank=True, null=True)
    statement_descriptor = CharField(_("Statement descriptor"), max_length=255, blank=True, null=True)
    statement_descriptor_suffix = CharField(_("Statement descriptor suffix"), max_length=255, blank=True, null=True)
    status = CharField(_("Status"), max_length=255, blank=True, null=True)
    transfer_data = CharField(_("Transfer data"), max_length=255, blank=True, null=True)
    transfer_group = CharField(_("Transfer group"), max_length=255, blank=True, null=True)
    source = CharField(_("Source"), max_length=1000, blank=True, null=True)

    class Meta:
        """Provide some extra information here"""

        verbose_name = "Transaction Detail"
        verbose_name_plural = "Transaction Details"

    def __str__(self):
        return "{0}".format(self.user)
