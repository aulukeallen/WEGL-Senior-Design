from django.contrib import admin
from .models import DJ

# Register your models here.
@admin.register(DJ)
class DJAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'email', 'joinDate')
    ordering = ('lastName', 'firstName')
    search_fields = ('firstName', 'lastName', 'email')