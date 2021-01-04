from rest_framework.views import APIView
from ..models import Creator
from creator_class.permissions import IsAccountOwner, IsCreator
from django.conf import settings
import stripe
from rest_framework import status
from creator_class.helpers import custom_response


stripe.api_key = settings.STRIPE_API_KEY

class StripeAccountConnectAPI(APIView):

    permission_classes = (IsAccountOwner, IsCreator,)

    def post(self, request):
        if request.user.is_authenticated:
            try:
                if not request.user.stripe_account_id:
                    account = stripe.Account.create(
                            type='express',
                            settings = {
                                "payouts":{"schedule":{"interval":"weekly", "weekly_anchor":"sunday"}}
                                },
                        )   

                    ob=Creator.objects.filter(pk=request.user.pk).first()
                    ob.stripe_account_id = account.id
                    ob.save()

                    account_links = stripe.AccountLink.create(
                        account=account.id,
                        refresh_url='http://localhost:3002/creator-transfer-funds',
                        return_url='http://localhost:3002/creator-transfer-funds',
                        type='account_onboarding',
                    )

                    message = "Successfully connected stripe account"
                    return custom_response(True, status.HTTP_201_CREATED, message, account_links)
                else:

                    message = "You are already connected with stripe"
                    return custom_response(False, status.HTTP_400_BAD_REQUEST, message)

           
            except Exception as e:
                message = str(e)
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        else:
            message = "Unauthorised User"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)


class StripeAccountDiscoonectAPI(APIView):

    permission_classes = (IsAccountOwner, IsCreator,)

    def post(self, request):
        if request.user.is_authenticated:

            try:
                if request.user.stripe_account_id:
                    stripe.Account.delete(request.user.stripe_account_id)
                    ob=Creator.objects.filter(id=request.user.id).first()
                    ob.stripe_account_id = ""
                    ob.save()    
                    message = "Successfully removed stripe account"
                    return custom_response(True, status.HTTP_200_OK, message)
                message = "Successfully removed stripe account"
                return custom_response(True, status.HTTP_200_OK, message)
            except Exception as e:
                message = str(e)
                return custom_response(True, status.HTTP_400_BAD_REQUEST, message)
        else:
            message = "Unauthorised User"
            return custom_response(True, status.HTTP_400_BAD_REQUEST, message)


class CheckStripeConnectAPIView(APIView):

    permission_classes = (IsAccountOwner, IsCreator,)

    def get(self, request):
        if request.user.is_authenticated:
            try:
                if not request.user.stripe_account_id:
                    message = "You are not connected with stripe account"
                    return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
                else:
                    message = "You are already connected with stripe"
                    return custom_response(False, status.HTTP_200_OK, message)           
            except Exception as e:
                message = str(e)
                return custom_response(False, status.HTTP_400_BAD_REQUEST, message)
        else:
            message = "Unauthorised User"
            return custom_response(False, status.HTTP_400_BAD_REQUEST, message)