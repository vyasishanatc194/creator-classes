import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from rest_framework.pagination import PageNumberPagination

from rest_framework import status
from rest_framework.response import Response
from django.core.mail import EmailMultiAlternatives
import os
from user.models import User
import sendgrid
from .settings import SENDGRID_API_KEY
from sendgrid.helpers.mail import Email, Substitution, Mail, Personalization
from python_http_client import exceptions

# Pagination
PAGINATOR = PageNumberPagination()
PAGINATOR.page_size = 10
PAGINATOR_PAGE_SIZE = PAGINATOR.page_size


def get_object(model ,pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None

def custom_response(status_value, code, message, result={}):
    return Response({
                    'status': status_value,
                    'code': code,
                    'message': message,
                    'data': result
                }, status=status.HTTP_200_OK)


def dict_obj_list_to_str(data):
    for key, value in data.items():
        data[key] = "".join(value)
    return data


def send_email(user, subject, text_content):
    from_email= settings.EMAIL_HOST_USER
    to= user.email
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
    return "Mail with link has been sent successfully"


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


def serialized_response(serializer, message):
    if serializer.is_valid():
        serializer.save()
        result = serializer.data
        response_status = True
    else:
        result = dict_obj_list_to_str(serializer.errors)
        response_status = False
        message = "Please resolve error(s) OR fill Missing field(s)!"
    return response_status, result, message

def delete_media(path):
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if(os.path.exists(os.path.join(media_root, str(path))) and path):
        os.remove(os.path.join(media_root, str(path)))
    return True


def send_templated_email(to_email, email_temlpate_id, dynamic_data_for_template):
    sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
    personalization = Personalization()
    personalization.add_to(Email(to_email))
    mail = Mail()
    mail.from_email = Email("aaradhana.citrusbug@gmail.com")
    mail.template_id = email_temlpate_id
    personalization.dynamic_template_data = dynamic_data_for_template
    mail.add_personalization(personalization)
    try:
        sg.client.mail.send.post(request_body=mail.get())
        return
    except exceptions.BadRequestsError as e:
        exit()