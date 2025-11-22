from celery import Celery
import sys, os
from infrastructure.tasks.notifications import send_email

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Celery("noconflict_backend")
app.config_from_object("settings.vars", namespace="CELERY")
app.autodiscover_tasks(["infrastructure.tasks"])