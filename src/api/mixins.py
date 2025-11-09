from importlib import import_module
from typing import TYPE_CHECKING, Sequence, Type

from django.conf import settings
from django.contrib import auth
from rest_framework.authentication import BaseAuthentication, SessionAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated

# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions


def get_auth_header(headers):
    value = headers.get("Authorization")

    if not value:
        return None

    auth_type, auth_value = value.split()[:2]

    return auth_type, auth_value


def enforce_csrf(request):
    """
    Enforce CSRF validation.
    """
    check = CSRFCheck(lambda: ())
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    if reason:
        # CSRF failed, bail with explicit error message
        raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)


class CustomAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT["JWT_AUTH_COOKIE"]) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        # enforce_csrf(request)
        return self.get_user(validated_token), validated_token


class SessionAsHeaderAuthentication(BaseAuthentication):
    """
    In case we are dealing with issues like Safari not supporting SameSite=None,
    And the client passes the session as Authorization header:

    Authorization: Session 7wvz4sxcp3chm9quyw015n6ryre29b3u

    Run the standard Django auth & try obtaining user.
    """

    def authenticate(self, request):
        auth_header = get_auth_header(request.headers)

        if auth_header is None:
            return None

        auth_type, auth_value = auth_header

        if auth_type != "Session":
            return None

        engine = import_module(settings.SESSION_ENGINE)
        SessionStore = engine.SessionStore
        session_key = auth_value

        request.session = SessionStore(session_key)
        user = auth.get_user(request)

        return user, None


class CsrfExemptedSessionAuthentication(SessionAuthentication):
    """
    DRF SessionAuthentication is enforcing CSRF, which may be problematic.
    That's why we want to make sure we are exempting any kind of CSRF checks for APIs.
    """

    def enforce_csrf(self, request):
        return


if TYPE_CHECKING:
    # This is going to be resolved in the stub library
    # https://github.com/typeddjango/djangorestframework-stubs/
    from rest_framework.permissions import _PermissionClass

    PermissionClassesType = Sequence[_PermissionClass]
else:
    PermissionClassesType = Sequence[Type[BasePermission]]


class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        CsrfExemptedSessionAuthentication,
        SessionAsHeaderAuthentication,
        CustomAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated,)
