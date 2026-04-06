from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

# Signal for AttendanceRecord creation
from django.db.models.signals import post_save
from django.dispatch import receiver

# Represents a WEGL 91.1 DJ.
# - Many-to-many relationship with DJs -
class DJ(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="dj_profile")
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=25, unique=True)
    joinDate = models.DateField("date dj joined wegl")

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


# Create AttendanceRecord when a DJ is created
@receiver(post_save, sender=DJ)
def create_attendance_record_for_dj(sender, instance, created, **kwargs):
    if created:
        AttendanceRecord.objects.create(dj=instance)

# Represents an on-air show on WEGL 91.1 (WHAT a show is). 
# - Many-to-many relationship with DJ -
# - One-to-many relationship with Timeslot -

# Through model for DJ-OnAirShow relationship with attendance boolean
class OnAirShowDJ(models.Model):
    onairshow = models.ForeignKey('OnAirShow', on_delete=models.CASCADE)
    dj = models.ForeignKey('DJ', on_delete=models.CASCADE)
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('onairshow', 'dj')

    def __str__(self):
        return f"{self.dj} in {self.onairshow} - Present: {self.present}"


class OnAirShow(models.Model):
    name = models.CharField(max_length=200)
    DAYS = [
        (0, "Sunday"),
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday")
    ]
    day = models.IntegerField(choices=DAYS, null=True, blank=True)
    startTime = models.TimeField(null=True, blank=True)
    djs = models.ManyToManyField(DJ, through='OnAirShowDJ', related_name="shows", blank=True)

    def __str__(self):
        return self.name

class AttendanceRecord(models.Model):
    dj = models.ForeignKey(DJ, on_delete=models.CASCADE, related_name="attendance_records")
    absenceCount = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.dj} - Absences: {self.absenceCount}"

# Represents a timeslot for an on-air show (WHEN a show is).
# - Many-to-one relationship with Show -
class Timeslot(models.Model):
    DAYS = [
        (0, "Sunday"),
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday")
    ]

    show = models.ForeignKey(OnAirShow, on_delete=models.CASCADE, related_name="timeslots")
    day = models.IntegerField(choices=DAYS)
    startTime = models.TimeField()
    duration = models.DurationField()

    # Inner config class: specifies that (show, weekday, start_time) must be unique.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["show", "day", "startTime"],
                name="uniqueShowTimeslot"
            )
        ]

    def __str__(self):
        return f"{self.show.name} - {self.get_day_display()} @ {self.startTime}"