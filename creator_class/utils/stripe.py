"""
Define Stripe payment gateway related stuff here.
"""
from django.conf import settings
import stripe


class MyStripe():
    """
    This is a common Stripe class which includes different methods
    like createCustomer, createCard, createBank, createCharge etc.
    """

    def __init__(self):
        stripe.api_key = settings.STRIPE_API_KEY

    def create_customer(self, user):
        """Using this method you can register a new customer"""

        # description
        # email
        # metadata
        # name
        # payment_method
        # phone
        # shipping

        return stripe.Customer.create(email=user.email, name=f"{user.first_name} {user.last_name}")

    def update_customer(self, customer_id, user):
        """Using this method you can update an existing customer"""

        # description
        # email
        # metadata
        # name
        # payment_method
        # phone
        # shipping

        return stripe.Customer.modify(customer_id, metadata={"email": user.email, "name": f"{user.first_name} {user.last_name}"})

    def delete_customer(self, customer_id):
        """Using this method you can delete already registered customer"""
        return stripe.Customer.delete(customer_id)

    def create_card(self, customer_id, card):
        """Using this method you can create a new card of existing customer"""
        return stripe.Customer.create_source(customer_id, source=card['card_id'])

    def delete_card(self, customer_id, card_id):
        """Using this method you can delete a card of existing customer"""
        return stripe.Customer.delete_source(customer_id, card_id)

    def create_charge(self, data, card, customer_id):
        """Using this method you can create a new charge of existing customer"""
        return stripe.Charge.create(amount=int(data["final_price"])*100, currency=settings.CURRENCY, source=card, customer=customer_id)

    def retrieve_charge(self, charge_id):
        """Using this method you can fetch a charge of existing customer"""
        return stripe.Charge.retrieve(charge_id)

    def update_carge(self, charge_id, order):
        """Using this method you can update a charge of existing customer"""
        return stripe.Charge.modify(charge_id, metadata={"order_id": order.id})

    def capture_charge(self, charge_id):
        """Using this method you can capture a charge of existing customer"""
        return stripe.Charge.capture(charge_id)

    def create_token(self, data):
        """Using this method you can create a new token of credit/debit card"""
        return stripe.Token.create(card=data)


def create_card_object(newcard, request):
    """This method is used to create a response object of a card"""
    data = {
        "card_id": newcard.id,
        "customer_id": request.user.customer_id,
        "user": request.user.id,
        "brand": newcard.brand,
        "exp_month": newcard.exp_month,
        "exp_year": newcard.exp_year,
        "last4": newcard.last4,
        "name": newcard.name,
    }
    return data