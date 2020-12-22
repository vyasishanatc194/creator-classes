from rest_framework.views import APIView
from rest_framework.response import Response
from creator_class.permissions import IsAccountOwner
from user.models import Card
from ..serializers import CardSerializer
from creator_class.helpers import custom_response
from rest_framework import status
from creator_class.utils import MyStripe, create_card_object


class CardAPIView(APIView):
    """API View for Card listing"""

    permission_classes = (IsAccountOwner,)
    serializer_class = CardSerializer
    queryset = Card.objects.all()

    def get(self, request, format=None):
        try:
            cards = Card.objects.filter(user_id=request.user.pk)
            if cards is not None:
                serializer = CardSerializer(cards, many=True, context={"request": request})
                message= "Successfully fetched cards"
                return custom_response(True, status.HTTP_200_OK, message, serializer.data)

        except Card.DoesNotExist:
            message= "Cards not found"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


    def post(self, request, format=None):
        try:
            stripe = MyStripe()
            newcard = stripe.create_card(request.user.customer_id, request.data)
            data = create_card_object(newcard, request)
            serializer = CardSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                message = "Successfully created card"
                return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                message="Cannot create card"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message, serializer.errors)
        except Exception as inst:
            print(inst)
            message = "Enter valid customer_id and card_id"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


    def delete(self, request, pk, format=None):
        try:
            cards = Card.objects.get(id=pk)
            stripe = MyStripe()
            stripe.delete_card(request.user.pk, cards.card_id)
            cards.delete()
            message="Successfully deleted registered card"
            return custom_response(True, status.HTTP_200_OK, message)

        except Card.DoesNotExist:
            message = "Registered Card not found"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


    def put(self, request, pk, format=None):
        try:
            cards = Card.objects.get(id=pk)
            stripe = MyStripe()
            stripe.delete_card(cards.customer_id, cards.card_id)
            cards.delete()
            
            newcard = stripe.create_card(request.user.customer_id, request.data)
            data = create_card_object(newcard, request)
            serializer = CardSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                message = "Successfully updated card"
                return custom_response(True, status.HTTP_201_CREATED, message)
            else:
                message="Cannot update card"
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message, serializer.errors)
        except Exception as inst:
            print(inst)
            message = "Enter valid customer_id and card_id"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

        except Card.DoesNotExist:
            message = "Registered Card not found"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)