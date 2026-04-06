from django.core.management.base import BaseCommand
from django.utils import timezone
from djrecord.models import OnAirShow, OnAirShowDJ, AttendanceRecord
import datetime

class Command(BaseCommand):
    help = 'Checks for absent DJs and increments their absence count if not present.'

    def handle(self, *args, **options):
        now = timezone.localtime()
        current_weekday = (now.weekday() + 1) % 7
        # Round down to the last hour, then add 15 minutes
        check_time = now.replace(minute=15, second=0, microsecond=0)
        # Find shows scheduled for today at this hour
        shows = OnAirShow.objects.filter(day=current_weekday, startTime__hour=check_time.hour)
        for show in shows:
            for onairshowdj in OnAirShowDJ.objects.filter(onairshow=show):
                if not onairshowdj.present:
                    attendance, _ = AttendanceRecord.objects.get_or_create(dj=onairshowdj.dj)
                    attendance.absenceCount += 1
                    attendance.save()
                    self.stdout.write(f"Absent: {onairshowdj.dj} for show {show.name} (Absences: {attendance.absenceCount})")
                # Reset present for next period
                onairshowdj.present = False
                onairshowdj.save()
        self.stdout.write(self.style.SUCCESS('Absence check complete.'))
