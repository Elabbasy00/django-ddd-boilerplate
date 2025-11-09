from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.serializers import as_serializer_error
from rest_framework.views import exception_handler

from src.application.shared.exceptions import (
    ApplicationError,
    ValidationError as AppValidationError,
    NotFoundError,
    ConflictError,
    UnauthorizedError,
)
from src.domain.shared.exceptions import DomainException


def drf_custom_exception_handler(exc, ctx):
    """
    {
        "message": "Error message",
        "extra": {}
    }
    """
    if isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(as_serializer_error(exc))

    if isinstance(exc, Http404):
        exc = exceptions.NotFound()

    if isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = exception_handler(exc, ctx)

    # If unexpected error occurs (server error, etc.)
    if response is None:
        # Handle ApplicationError and its subclasses
        if isinstance(exc, ApplicationError):
            status_code = 400  # Default
            if isinstance(exc, NotFoundError):
                status_code = 404
            elif isinstance(exc, ConflictError):
                status_code = 409
            elif isinstance(exc, UnauthorizedError):
                status_code = 401
            elif isinstance(exc, AppValidationError):
                status_code = 400

            data = {"message": exc.message, "extra": exc.extra}
            return Response(data, status=status_code)

        # Handle DomainException (should be caught and converted, but handle just in case)
        if isinstance(exc, DomainException):
            data = {"message": exc.message, "extra": exc.details}
            return Response(data, status=400)

        return response

    if isinstance(exc.detail, (list, dict)):
        response.data = {"detail": response.data}

    if isinstance(exc, exceptions.ValidationError):
        response.data["message"] = "Validation error"
        response.data["extra"] = {"fields": response.data["detail"]}
    else:
        response.data["message"] = response.data["detail"]
        response.data["extra"] = {}

    del response.data["detail"]

    return response
