from django.contrib import admin
from .models import CSVUpload, AsplayEntry

# Register your models here.
@admin.register(CSVUpload)
class CSVUploadAdmin(admin.ModelAdmin):
    list_display = ('fileName', 'uploadDate', 'rowCount', 'status')
    ordering = ('uploadDate',)

@admin.register(AsplayEntry)
class AsplayEntryAdmin(admin.ModelAdmin):
    list_display = ('playDate', 'startTime', 'cutID', 'title', 'artist', 'album', 'group', 'durationSeconds')
    list_filter = ('playDate', 'artist')
    search_fields = ('title', 'artist', 'album', 'group')
    ordering = ('-playDate', '-startTime')