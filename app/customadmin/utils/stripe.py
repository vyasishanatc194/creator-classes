import stripe
from django.conf import settings

class MyStripe():

    def __init__(self):
        stripe.api_key = settings.API_KEY

    def createCustomer(self,user):

        # description
        # email
        # metadata
        # name
        # payment_method
        # phone
        # shipping    

        return stripe.Customer.create(email=user.email,name=user.name,phone=user.mobile)
        
    def updateCustomer(self,customerId,user):

        # description
        # email
        # metadata
        # name
        # payment_method
        # phone
        # shipping    

        return stripe.Customer.modify(customerId,
            metadata={"email": user.email,"name": user.name,"phone": user.mobile},
        )

    def deleteCustomer(self,customerId):

        return stripe.Customer.delete(customerId)

    def createCard(self,customerId, data):
        return stripe.Customer.create_source(customerId, source=data["source"])

    def deleteCard(self, customerId, cardId):
        return stripe.Customer.delete_source(customerId, cardId)

    def createBank(self, customerId, bank_data):
        return stripe.Customer.create_source(customerId, source=bank_data)

    def retrieveBank(self, customerId, bankId):
        return stripe.Customer.retrieve_source(customerId, bankId)

    def updateBank(self, customerId, bankId, order):
        return stripe.Customer.modify_source(customerId, bankId, metadata={"order_id": order.id})

    def verifyBnak(self, customerId, bankId):
        bank_account = stripe.Customer.retrieve_source(customerId, bankId)
        return bank_account.verify(amounts=[32, 45])

    def deleteBank(self, customerId, bankId):
        return stripe.Customer.delete_source(customerId, bankId)

    def createCharge(self, data, card, customerId):
        return stripe.Charge.create(amount=int(data["final_price"])*100, currency=settings.CURRENCY, source=card, customer=customerId)

    def retrieveCharge(self, chargeId):
        return stripe.Charge.retrieve(chargeId)

    def updateCharge(self, chargeId, order):
        return stripe.Charge.modify(chargeId, metadata={"order_id": order.id})

    def captureCharge(self, chargeId):
        return stripe.Charge.capture(chargeId)
