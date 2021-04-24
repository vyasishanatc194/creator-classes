from rest_framework.views import APIView
from ..serializers import (
    CountryListSerializer,
)
from ..models import CountryField
from creator_class.helpers import custom_response
from rest_framework import status, parsers, renderers



class CountryListAPIView(APIView):
    serializer_class = CountryListSerializer

    def get(self, request):
        countries = CountryField.objects.filter(active=True)
        if 'country' in request.GET:
            countries = countries.filter(country_name=request.GET['country'])
        serializer = self.serializer_class(countries,many=True,context={'request': request})
        message = "Country Details fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


