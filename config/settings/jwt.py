import datetime

from config.env import env

# For more settings
# Read everything from here - https://styria-digital.github.io/django-rest-framework-jwt/#additional-settings

# Default to 7 days
JWT_EXPIRATION_DELTA_SECONDS = env("JWT_EXPIRATION_DELTA_SECONDS", default=60 * 60 * 24 * 360)
JWT_AUTH_COOKIE = env("JWT_AUTH_COOKIE", default="jwt")
JWT_AUTH_COOKIE_SAMESITE = env("JWT_AUTH_COOKIE_SAMESITE", default="Lax")
JWT_AUTH_HEADER_PREFIX = env("JWT_AUTH_HEADER_PREFIX", default="Bearer")
JWT_SIGNING_KEY = env("JWT_SIGNING_KEY", default="django-insecure-&(5h58d6647w8nk7mb^a_b-")


# JWT_AUTH = {
#     "JWT_GET_USER_SECRET_KEY": "src.authentication.services.auth_user_get_jwt_secret_key",
#     "JWT_RESPONSE_PAYLOAD_HANDLER": "src.authentication.services.auth_jwt_response_payload_handler",
#     "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=JWT_EXPIRATION_DELTA_SECONDS),
#     "JWT_ALLOW_REFRESH": False,
#     "JWT_AUTH_COOKIE": JWT_AUTH_COOKIE,
#     "JWT_AUTH_COOKIE_SECURE": True,
#     "JWT_AUTH_COOKIE_SAMESITE": JWT_AUTH_COOKIE_SAMESITE,
#     "JWT_AUTH_HEADER_PREFIX": JWT_AUTH_HEADER_PREFIX,
# }


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(seconds=JWT_EXPIRATION_DELTA_SECONDS),
    # "REFRESH_TOKEN_LIFETIME": None,
    # "ROTATE_REFRESH_TOKENS": False,
    # "BLACKLIST_AFTER_ROTATION": False,
    "JWT_AUTH_COOKIE_DOMAIN": None,  # A string like "example.com", or None for standard domain cookie.
    "JWT_AUTH_COOKIE_SECURE": False,  # Whether the auth cookies should be secure (https:// only).
    "JWT_AUTH_COOKIE_HTTP_ONLY": True,  # Http only cookie flag.It's not fetch by javascript.
    "JWT_AUTH_COOKIE_PATH": "/",  # The path of the auth cookie.
    "JWT_AUTH_COOKIE_SAMESITE": JWT_AUTH_COOKIE_SAMESITE,
    "JWT_AUTH_COOKIE": JWT_AUTH_COOKIE,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SIGNING_KEY,
    "AUTH_HEADER_TYPES": (JWT_AUTH_HEADER_PREFIX,),
    "JWT_AUTH_COOKIE_SECURE": True,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
