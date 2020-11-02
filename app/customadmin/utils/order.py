import json
from .stripe import MyStripe
from user.models import User


def create_charge_object(newcharge, request):

    address_data = newcharge.billing_details.address
    str_address_data = json.dumps(address_data, indent=4)

    fraud_details_data = newcharge.fraud_details
    str_fraud_details_data = json.dumps(fraud_details_data, indent=4)

    metadata_data = newcharge.metadata
    str_metadata_data = json.dumps(metadata_data, indent=4)

    outcome_data = newcharge.outcome
    str_outcome_data = json.dumps(outcome_data, indent=4)

    refunds_data_data = newcharge.refunds.data
    str_refunds_data_data = json.dumps(refunds_data_data, indent=4)

    source_data = newcharge.source
    str_source_data = json.dumps(source_data, indent=4)

    data = {
        "user": request.user.id,
        "card_id": newcharge.payment_method,
        "customer_id": request.user.customer_id,

        "charge_id": newcharge.id,
        "charge_object": newcharge.object,
        "amount": newcharge.amount,
        "amount_refunded": newcharge.amount_refunded,
        "application": newcharge.application,
        "application_fee": newcharge.application_fee,
        "application_fee_amount": newcharge.application_fee_amount,
        "balance_transaction": newcharge.balance_transaction,
        "address": str_address_data,
        "email": newcharge.billing_details.email,
        "name": newcharge.billing_details.name,
        "phone": newcharge.billing_details.phone,
        "calculated_statement_descriptor": newcharge.calculated_statement_descriptor,
        "captured": newcharge.captured,
        "created": newcharge.created,
        "currency": newcharge.currency,
        "customer": newcharge.customer,
        "description": newcharge.description,
        "disputed": newcharge.disputed,
        "failure_code": newcharge.failure_code,
        "failure_message": newcharge.failure_message,
        "fraud_details": str_fraud_details_data,
        "invoice": newcharge.invoice,
        "livemode": newcharge.livemode,
        "metadata": str_metadata_data,
        "on_behalf_of": newcharge.on_behalf_of,
        "order": newcharge.order,
        "outcome": str_outcome_data,
        "paid": newcharge.paid,
        "payment_intent": newcharge.payment_intent,
        "payment_method": newcharge.payment_method,
        "brand": newcharge.payment_method_details.card.brand,
        "address_line1_check": newcharge.payment_method_details.card.checks.address_line1_check,
        "address_postal_code_check": newcharge.payment_method_details.card.checks.address_postal_code_check,
        "cvc_check": newcharge.payment_method_details.card.checks.cvc_check,
        "country": newcharge.payment_method_details.card.country,
        "exp_month": newcharge.payment_method_details.card.exp_month,
        "exp_year": newcharge.payment_method_details.card.exp_year,
        "fingerprint": newcharge.payment_method_details.card.fingerprint,
        "funding": newcharge.payment_method_details.card.funding,
        "installments": newcharge.payment_method_details.card.installments,
        "last4": newcharge.payment_method_details.card.last4,
        "network": newcharge.payment_method_details.card.network,
        "three_d_secure": newcharge.payment_method_details.card.three_d_secure,
        "wallet": newcharge.payment_method_details.card.wallet,
        "charge_type": newcharge.payment_method_details.type,
        "receipt_email": newcharge.receipt_email,
        "receipt_number": newcharge.receipt_number,
        "receipt_url": newcharge.receipt_url,
        "refunded": newcharge.refunded,
        "refunds_object": newcharge.refunds.object,
        "refunds_data": str_refunds_data_data,
        "refunds_has_more": newcharge.refunds.has_more,
        "refunds_url": newcharge.refunds.url,
        "review": newcharge.review,
        "shipping": newcharge.shipping,
        "source_transfer": newcharge.source_transfer,
        "statement_descriptor": newcharge.statement_descriptor,
        "statement_descriptor_suffix": newcharge.statement_descriptor_suffix,
        "status": newcharge.status,
        "transfer_data": newcharge.transfer_data,
        "transfer_group": newcharge.transfer_group,
        "source": str_source_data

    }
    return data


def create_card_object(newcard, request):
    data = {
        "card_id": newcard.id,
        "customer_id": request.user.customer_id,
        "user": request.user.id,
        "brand": newcard.brand,
        "exp_month": newcard.exp_month,
        "exp_year": newcard.exp_year,
        "last4": newcard.last4,
        "name": newcard.name
    }
    return data


def create_bank_object(newbank, request):
    metadata_data = newbank.metadata
    str_metadata_data = json.dumps(metadata_data, indent=4)

    data = {
        "user": request.user.id,
        "bank_id": newbank.id,
        "bank_object": newbank.object,
        "acc_name": newbank.account_holder_name,
        "acc_type": newbank.account_holder_type,
        "bank_name": newbank.bank_name,
        "country": newbank.country,
        "currency": newbank.currency,
        "customer": newbank.customer,
        "fingerprint": newbank.fingerprint,
        "last4": newbank.last4,
        "metadata": str_metadata_data,
        "routing_number": newbank.routing_number,
        "status": newbank.status,
    }
    return data


def create_customer_id(user):
    stripe = MyStripe()
    newcustomer = stripe.createCustomer(user)
    User.objects.filter(pk=user.id).update(customer_id=newcustomer.id)
    return newcustomer
