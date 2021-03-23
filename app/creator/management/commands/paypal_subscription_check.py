from django.core.management.base import BaseCommand
import requests
# from user.models import User


paypal_username = "Aabc-D8rlBMneFlgavVKs9R1S5qDNcD0HXwuSP76BKM_8QGp6rhk6B1khGyRy8Bc0aELuhVIOYUImeR2"
paypal_password = "EOuRkF9j0KAB2mbbWruHgQCdQpZeu5MOQEASF4fklPBwNHOGxn6YHf9IBgyy0fWQefCAFfYFugy1KuKl"
paypal_token_url = "https://api.sandbox.paypal.com/v1/oauth2/token"
paypal_subscription_chek_url = "https://api.sandbox.paypal.com/v1/billing/subscriptions/"


def create_auth_token():
    url = paypal_token_url
    payload = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, auth=(paypal_username, paypal_password), data=payload)

    auth_response = response.json()
    access_token = auth_response['access_token']
    return access_token


class Command(BaseCommand):

    help = "Check paypal subscription status"

    def handle(self, *args, **options):
        try:
            users = User.objects.filter(paypal_subscription_id!="", is_active=True)
            for user in users:
                url = paypal_subscription_chek_url + user.paypal_subscription_id
                token = create_auth_token()
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                }
                response = requests.get(url, headers=headers, data={})

                sub_response = response.json()
                if sub_response['status']!= "ACTIVE":
                    cancel_sub_url = url + user.paypal_subscription_id + "/cancel"
                    cancel_sub = requests.post(cancel_sub_url, headers=headers, data={})

                    user.paypal_subscription_id = None
                    user.plan_id=None
                    user.save()

                    # TODO Send Email- subscription is canceled
        except:
            self.stdout.write(self.style.ERROR("Error in paypal subscription check"))