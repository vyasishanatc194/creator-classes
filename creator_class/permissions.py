from rest_framework import permissions, status, authentication
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination


# Pagination
PAGINATOR = PageNumberPagination()
PAGINATOR.page_size = 10
PAGINATOR_PAGE_SIZE = PAGINATOR.page_size


class GenericAPIException(APIException):
    """
    raises API exceptions with custom messages and custom status codes
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "error"

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class IsAccountOwner(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        raise GenericAPIException(
            {
                "status": False,
                "code": 400,
                "message": "User not authenticated!",
                "result": status.HTTP_400_BAD_REQUEST,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class IsUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if not request.user.is_creator:
            return True
        raise GenericAPIException(
            {
                "status": False,
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "You don't have permisson to access this view!",
                "result": status.HTTP_400_BAD_REQUEST,
            }
        )


class IsCreator(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_creator:
            return True
        raise GenericAPIException(
            {
                "status": False,
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "You don't have permisson to access this view!",
                "result": status.HTTP_400_BAD_REQUEST,
            }
        )


def get_pagination_response(model_class, request, serializer_class, context):
    result = {}
    model_response = PAGINATOR.paginate_queryset(model_class, request)
    serializer = serializer_class(model_response, many=True, context=context)
    result.update({'data':serializer.data})
    current = PAGINATOR.page.number
    next_page = 0 if PAGINATOR.get_next_link() is None else current + 1
    previous_page = 0 if PAGINATOR.get_previous_link() is None else current - 1
    result.update({'links': {
        'current': current,
        'next': next_page,
        'previous': previous_page,
        'total': PAGINATOR.page.paginator.count,
        'last' : PAGINATOR.page.paginator.num_pages,
    }})
    return result