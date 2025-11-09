from django.urls import include, path

from .views import (
    UserJwtLoginApi,
    UserJwtLogoutApi,
    UserMeApi,
    UserSessionLoginApi,
    UserSessionLogoutApi,
    ChangePassword,
    CreateUser,
)

urlpatterns = [
    path(
        "session/",
        include(
            (
                [
                    path("login/", UserSessionLoginApi.as_view(), name="login"),
                    path("logout/", UserSessionLogoutApi.as_view(), name="logout"),
                ],
                "session",
            )
        ),
    ),
    path(
        "jwt/",
        include(
            (
                [
                    path("login/", UserJwtLoginApi.as_view(), name="login"),
                    path("logout/", UserJwtLogoutApi.as_view(), name="logout"),
                ],
                "jwt",
            )
        ),
    ),
    path("me/", UserMeApi.as_view(), name="me"),
    path("change_password/", ChangePassword.as_view(), name="change_password"),
    path("registration/", CreateUser.as_view(), name="registration"),
    # path("password_reset/", include("django_rest_passwordreset.urls", namespace="password_reset")),
]
