from config.env import env

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://127.0.0.1:6380/0")
CELERY_RESULT_BACKEND = "django-db"
CELERY_TIMEZONE = env("CELERY_TIMEZONE", default='Africa/Cairo')


CELERY_TASK_SOFT_TIME_LIMIT = 20  # seconds
CELERY_TASK_TIME_LIMIT = 30  # seconds
CELERY_TASK_MAX_RETRIES = 3