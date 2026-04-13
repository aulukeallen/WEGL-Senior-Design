from django.db import models

# Create your models here.
class MediaRecord(models.Model):
    artist = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    MEDIA_CHOICES = {
        "Vinyl": "Vinyl",
        "CD": "CD",
        "Cassette": "Cassette",
        "Hard Drive": "Hard Drive",
        "Other": "Other"
    }
    medium = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    weglSticker = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.artist} on {self.medium}"