from django.db import models
from django.utils import timezone

# Represents a WEGL 91.1 DJ.
# - Many-to-many relationship with DJs -
class DJ(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=25, unique=True)
    joinDate = models.DateField("date dj joined wegl")

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

# Represents an on-air show on WEGL 91.1 (WHAT a show is). 
# - Many-to-many relationship with DJ -
# - One-to-many relationship with Timeslot -
class OnAirShow(models.Model):
    name = models.CharField(max_length=200)
    djs = models.ManyToManyField(DJ, related_name="shows", blank=True)

    def __str__(self):
        return self.name

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