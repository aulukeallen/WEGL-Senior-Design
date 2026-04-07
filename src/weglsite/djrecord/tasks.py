from django.core.management.base import BaseCommand
from django.utils import timezone
from djrecord.models import OnAirShow, OnAirShowDJ, AttendanceRecord
import datetime


def check_absences():
    now = timezone.localtime()
    current_weekday = (now.weekday() + 1) % 7
    check_time = now.replace(minute=15, second=0, microsecond=0)
    shows = OnAirShow.objects.filter(day=current_weekday, startTime__hour=check_time.hour)
    for show in shows:
        for onairshowdj in OnAirShowDJ.objects.filter(onairshow=show):
            if not onairshowdj.present:
                attendance, _ = AttendanceRecord.objects.get_or_create(dj=onairshowdj.dj)
                attendance.absenceCount += 1
                attendance.save()
            onairshowdj.present = False
            onairshowdj.save()
