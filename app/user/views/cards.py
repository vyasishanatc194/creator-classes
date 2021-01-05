from rest_framework.views import APIView
from rest_framework.response import Response
from creator_class.permissions import IsAccountOwner
from user.models import User
from ..serializers import CardSerializer
from creator_class.helpers import custom_response
from rest_framework import status
from creator_class.utils import MyStripe, create_card_object, create_customer_id


class CardAPIView(APIView):
    """API View for Card listing"""

    permission_classes = (IsAccountOwner,)
    serializer_class = CardSerializer

    def get(self, request, format=None):
        try:
            serializer = CardSerializer(request.user, context={"request": request})
            message= "Successfully fetched card"
            return custom_response(True, status.HTTP_200_OK, message, serializer.data)

        except Card.DoesNotExist:
            message= "Card not found"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


    def post(self, request, format=None):
        try:
            stripe = MyStripe()
            customer_id = request.user.customer_id
            user = User.objects.get(pk=request.user.pk)
            if not customer_id:
                newcustomer = create_customer_id(request.user)
                customer_id = newcustomer.id
            newcard = stripe.create_card(customer_id, request.data)
            data = create_card_object(newcard, request)
            serializer = CardSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                message = "Successfully created card"

                user.card_id= newcard.id
                user.last4 = request.data['last4']
                user.brand = request.data['brand']
                user.exp_month = request.data['exp_month']
                user.exp_year = request.data['exp_year']
                user.card_name = request.data['card_name']
                user.save()


                return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                message="Cannot create card"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message, serializer.errors)
        except Exception as inst:
            print(inst)
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


    def delete(self, request, format=None):
        try:
            stripe = MyStripe()
            if request.user.card_id and request.user.customer_id:
                stripe.delete_card(request.user.customer_id, request.user.card_id)
            user  = User.objects.get(pk=request.user.pk)
            user.card_id = ""
            user.last4 = ""
            user.brand= ""
            user.exp_month = ""
            user.exp_year =""
            user.card_name = ""
            user.save()
            message="Successfully deleted registered card"
            return custom_response(True, status.HTTP_200_OK, message)

        except Exception as inst:
            message = str(inst)
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


