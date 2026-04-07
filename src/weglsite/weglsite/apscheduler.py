from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
import logging
import sys

from djrecord.tasks import check_absences

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(
        check_absences,
        'cron',
        minute='15',
        id='check_absences_job',
        replace_existing=True,
    )
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass