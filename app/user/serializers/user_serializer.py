from rest_framework import fields, serializers
from ..models import User
from rest_framework.authtoken.models import Token


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User Profile serializer
    """
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user_obj = User(**validated_data)
        user_obj.set_password(validated_data['password'])
        user_obj.save()
        Token.objects.create(user=user_obj)
        return validated_data