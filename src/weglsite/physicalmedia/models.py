from django.db import models

# Create your models here.
class MediaRecord(models.Model):
    artist = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    MEDIA_CHOICES = {
        "vinyl": "Vinyl",
        "cd": "CD",
        "cassette": "Cassette",
        "hard drive": "Hard Drive",
        "other": "Other"
    }
    medium = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    weglSticker = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.artist} on {self.medium}"