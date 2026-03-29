from django.contrib import admin
from .models import AttendanceRecord

# Register your models here.
@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('djName', 'absenceCount')
    ordering = ('-djName',)
    search_fields = ('djName',)
