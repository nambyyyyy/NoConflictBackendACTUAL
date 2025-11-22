import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "NoConflict_Backend"
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = ALGORITHM = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

SITE_URL = os.getenv("SITE_URL", "http://localhost:8000")
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "nambyyyyy@yandex.ru")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "1234")
MAIL_FROM = os.getenv("MAIL_FROM", "nambyyyyy@yandex.ru")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.yandex.ru")
MAIL_SSL = bool(os.getenv("MAIL_SSL", False))


CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

CELERY_RESULT_BACKEND = None
CELERY_TASK_IGNORE_RESULT = True

CELERY_TIMEZONE = "UTC"
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]

CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

API_VERSION = "v1"
AUTH_PREFIX = f"/api/{API_VERSION}/auth"