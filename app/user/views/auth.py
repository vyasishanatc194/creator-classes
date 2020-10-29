from rest_framework.views import APIView
from serializers import UserProfileSerializer
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status



class SignUpApiView(APIView):
    """
    User Sign up view
    """
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        email_check = User.objects.filter(email=request.data['email']).distinct()
        if email_check.exists():
            message = "Email already exists!"
            return custom_response(True, status.HTTP_200_OK, message)
        
        if not request.data['username']:
            request.data['username']=request.data['email'].split('@')[0]
        
        username_check = User.objects.filter(username=request.data['username']).distinct()
        if username_check.exists():
            message = "Username already exists!"
            return custom_response(True, status.HTTP_200_OK, message)

        message = "Account created successfully!"
        serializer = self.serializer_class(data=request.data)
        response_status, result, message = serialized_response(serializer, message)
        status_code = status.HTTP_201 if response_status else status.HTTP_400_BAD_REQUEST
        return custom_response(response_status, status_code, message, result)