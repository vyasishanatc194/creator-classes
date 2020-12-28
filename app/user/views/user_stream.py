from rest_framework.views import APIView
from ..serializers import StreamDetailSerializer, StreamListingSerializer
from creator_class.helpers import custom_response, serialized_response
from rest_framework import status
from creator.models import Stream, StreamKeyword
from datetime import datetime

STREAMS_FETCHED_MESSAGE = "Streams fetched Successfully!"

class StreamDetailView(APIView):
    """
    Stream detail view
    """
    serializer_class = StreamDetailSerializer
    permission_classes = ()

    def get(self, request, pk):
        stream = Stream.objects.filter(active=True, pk=pk)
        if not stream:
            message = "Stream not found"
            return custom_response(True, status.HTTP_400_BAD_REQUEST, message)
        serializer = self.serializer_class(stream[0],context={"request": request})
        message = "Stream fetched Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, serializer.data)


class StreamSearchAPIView(APIView):
    """
    Stream Search API
    """
    serializer_class = StreamListingSerializer
    permission_classes = ()

    def get(self, request):
        search = request.GET.get('search', None)
        stream_keyword = request.GET.get('keyword', None)

        streams = Stream.objects.filter(active=True, stream_datetime__gte=datetime.today())
        if search:
            streams = streams.filter(title__icontains=search)

        if stream_keyword:
            stream_keyword = stream_keyword.split(',')
            keyword_streams = []
            streams_keywords= StreamKeyword.objects.filter(keyword__in=stream_keyword)

            for stream in streams_keywords:
                if stream.stream in streams and stream.stream not in keyword_streams:
                    keyword_streams.append(stream.stream)
            serializer = self.serializer_class(keyword_streams, many=True, context={"request": request})
            return custom_response(True, status.HTTP_200_OK, STREAMS_FETCHED_MESSAGE, serializer.data) 


        serializer = self.serializer_class(streams, many=True, context={"request": request})
        return custom_response(True, status.HTTP_200_OK, STREAMS_FETCHED_MESSAGE, serializer.data)