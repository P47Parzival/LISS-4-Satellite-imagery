# backend/celery_config.py

from celery import Celery
from celery.schedules import crontab
import os

# Use Redis as the message broker
# The broker URL points to your running Redis instance.
BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Create a Celery instance
celery_app = Celery(
    "tasks",
    broker=BROKER_URL,
    backend=RESULT_BACKEND,
    include=["tasks_gee"]  # IMPORTANT: Tell Celery where to find tasks
)

# --- Define the Scheduled Task ---
# This is the "monitoring" part of your system.
celery_app.conf.beat_schedule = {
    'check-all-aois-daily': {
        'task': 'tasks_gee.schedule_all_aoi_checks', # Points to the task function
        'schedule': crontab("*"),  # Run every day at 1:30 AM
        # Use crontab(minute='*/30') for every 30 mins for testing
    },
}

celery_app.conf.timezone = 'UTC'