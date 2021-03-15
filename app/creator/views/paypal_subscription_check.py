# from django.core.management.base import BaseCommand
# import requests
from user.models import User


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
    print(access_token)
    return access_token


users = User.objects.filter(paypal_subscription_id!="", is_active=True)
for user in users:
    url = paypal_subscription_chek_url + user.paypal_subscription_id
    headers = {
        "Content-Type": "application/json",
        "Authorization": create_auth_token(),
    }
    response = requests.post(url, headers=headers, data=payload)

    sub_response = response.json()
    