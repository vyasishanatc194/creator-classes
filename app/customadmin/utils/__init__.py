from .core import update_order
from .core import get_upload_to_uuid, get_deleted_objects, admin_urlname
from .core import filter_perms, filter_superadmin, filter_admin, filter_vendor
from .api import get_status, modify_api_response

from six import string_types
from importlib import import_module

from .stripe import MyStripe
from .order import create_charge_object, create_card_object, create_bank_object, create_customer_id
from .emails import Emails
from .exception import CustomValidation

from django.utils.module_loading import import_string
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.conf import settings
import functools
from rest_framework import status



def import_callable(path_or_callable):
    if hasattr(path_or_callable, '__call__'):
        return path_or_callable
    else:
        assert isinstance(path_or_callable, string_types)
        package, attr = path_or_callable.rsplit('.', 1)
        return getattr(import_module(package), attr)


def default_create_token(token_model, user, serializer):
    token, _ = token_model.objects.get_or_create(user=user)
    return token


def jwt_encode(user):
    try:
        from rest_framework_jwt.settings import api_settings
    except ImportError:
        raise ImportError("djangorestframework_jwt needs to be installed")

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


@functools.lru_cache(maxsize=None)
def get_default_password_validators():
    return get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)


def get_password_validators(validator_config):
    validators = []
    for validator in validator_config:
        try:
            klass = import_string(validator['NAME'])
        except ImportError:
            msg = "The module in NAME could not be imported: %s. Check your AUTH_PASSWORD_VALIDATORS setting."
            raise ImproperlyConfigured(msg % validator['NAME'])
        validators.append(klass(**validator.get('OPTIONS', {})))

    return validators

def validate_password(password, user=None, password_validators=None):
    """
    Validate whether the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.append(error)
    if errors:
        print("*************************************************************")
        print(errors)
        # raise ValidationError(errors)
        raise CustomValidation("This password is too short. OR It must contain at least 8 characters. OR This password is too common. OR This password is entirely numeric.", status_code=status.HTTP_200_OK)
