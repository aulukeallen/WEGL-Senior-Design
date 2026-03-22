from django.db import models
from django.utils import timezone

# Create your models here.
class AttendanceRecord(models.Model):
    djName = models.CharField(max_length=200)
    absenceCount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.djName} - Absences: {self.absenceCount}"