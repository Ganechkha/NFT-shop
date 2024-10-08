import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nft_shop.settings")

app = Celery("nft_shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = "redis://localhost:6379/0"
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()
