import os

from config.env import BASE_DIR, env

FILE_UPLOAD_STRATEGY = env.str("DJNGO_FILEI_UPLOAD_STRATEGY", default="standard")
FILE_UPLOAD_STORAGE = env.str("DJANGO_FILE_UPLOAD_STORGE", default="local")

FILE_MAX_SIZE = env.int("FILE_MAX_SIZE", default=10485760)  # 10 MiB

if FILE_UPLOAD_STORAGE == "local":
    MEDIA_ROOT_NAME = "media"
    MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
    MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"
