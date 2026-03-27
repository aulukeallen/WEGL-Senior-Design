from django.contrib import admin
from .models import MediaRecord

# Register your models here.
@admin.register(MediaRecord)
class MediaRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'medium', 'weglSticker')
    ordering = ('artist', 'title')
    search_fields = ('title', 'artist', 'weglSticker')