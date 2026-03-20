from django.db import models

# Create your models here.

class CSVUpload(models.Model):
    fileName = models.CharField(max_length=100)
    uploadDate = models.DateTimeField(auto_now_add=True)
    rowCount = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"{self.fileName} ({self.uploadDate:%y-%m-%d %H:%M})"

class AsplayEntry(models.Model):
    upload = models.ForeignKey(CSVUpload, on_delete=models.CASCADE, related_name='entries')
    cutID = models.CharField(max_length=5)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, blank=True)
    group = models.CharField(max_length=20)
    startTime = models.TimeField()
    durationSeconds = models.DurationField()
    playDate = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['playDate']),
            models.Index(fields=['artist']),
            models.Index(fields=['cutID'])
        ]

    def __str__(self):
        return f"{self.title} - {self.artist} - {self.playDate} at {self.startTime}"