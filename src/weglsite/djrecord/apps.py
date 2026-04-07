import sys
from django.apps import AppConfig


class DjrecordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djrecord'
    
    def ready(self):
        # Only start scheduler if not running a management command that shouldn't start it
        if 'runserver' in sys.argv:
            from weglsite.apscheduler import start
            start()
