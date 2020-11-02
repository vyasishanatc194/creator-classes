
import firebase_admin
import os
from django.conf import settings


#https://github.com/firebase/firebase-admin-python/blob/f43e6876684d2c7e9acf5b0b013642b44883c63a/snippets/messaging/cloud_messaging.py#L24-L40
#https://firebase.google.com/docs/cloud-messaging/send-message#python

class Firebase(firebase_admin):

    def __init__(self):
         
        json_path = os.path.join(settings.BASE_DIR, "night-market-752c4-firebase-adminsdk-2k061-6b40f9d7bf.json")
        cred = self.credentials.Certificate(json_path)
        self.initialize_app(cred)

    def send_to_token(self, token, data, title, body):

        # [START send_to_token]
        # This registration token comes from the client FCM SDKs.
        # token = 'YOUR_REGISTRATION_TOKEN'

        # See documentation on defining a message payload.
        message = self.messaging.Message(
            notification= self.messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            token=token,
        )

        # Send a message to the device corresponding to the provided
        # registration token.
        response = self.messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        return response
        # [END send_to_token]

    def send_to_topic(self, topic, data, title, body):
        # [START send_to_topic]
        # The topic name can be optionally prefixed with "/topics/".
        # topic = 'highScores'

        # See documentation on defining a message payload.
        message = self.messaging.Message(
            notification= self.messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            topic=topic,
        )

        # Send a message to the devices subscribed to the provided topic.
        response = self.messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        return response
        # [END send_to_topic]

    def send_to_condition(self, condition, data, title, body):
        # [START send_to_condition]
        # Define a condition which will send to devices which are subscribed
        # to either the Google stock or the tech industry topics.
        # condition = "'stock-GOOG' in topics || 'industry-tech' in topics"

        # See documentation on defining a message payload.
        message = self.messaging.Message(
            notification= self.messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            condition=condition,
        )

        # Send a message to devices subscribed to the combination of topics
        # specified by the provided condition.
        response = self.messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
        return response
        # [END send_to_condition]


    def subscribe_to_topic(self, topic,token):
        # topic = 'highScores'
        # [START subscribe]
        # These registration tokens come from the client FCM SDKs.
        # registration_tokens = [
        #     'YOUR_REGISTRATION_TOKEN_1',
        #     # ...
        #     'YOUR_REGISTRATION_TOKEN_n',
        # ]

        registration_tokens = [
            token,
        ]

        # Subscribe the devices corresponding to the registration tokens to the
        # topic.
        response = self.messaging.subscribe_to_topic(registration_tokens, topic)
        # See the TopicManagementResponse reference documentation
        # for the contents of response.
        print(response.success_count, 'tokens were subscribed successfully')
        return response
        # [END subscribe]


    def unsubscribe_from_topic(self, topic,token):
        # topic = 'highScores'
        # [START unsubscribe]
        # These registration tokens come from the client FCM SDKs.
        registration_tokens = [
            token,
        ]

        # Unubscribe the devices corresponding to the registration tokens from the
        # topic.
        response = self.messaging.unsubscribe_from_topic(registration_tokens, topic)
        # See the TopicManagementResponse reference documentation
        # for the contents of response.
        print(response.success_count, 'tokens were unsubscribed successfully')
        return response
        # [END unsubscribe]