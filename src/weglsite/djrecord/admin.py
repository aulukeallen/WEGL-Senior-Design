from django.contrib import admin
from djrecord import forms
from .forms import OnAirShowForm
from .models import DJ, OnAirShow

        
# Register your models here.
@admin.register(DJ)
class DJAdmin(admin.ModelAdmin):
    list_display = ('firstName', 'lastName', 'email', 'joinDate')
    ordering = ('lastName', 'firstName')
    search_fields = ('firstName', 'lastName', 'email')

@admin.register(OnAirShow)
class OnAirShowAdmin(admin.ModelAdmin):
    list_display = ('name', 'day', 'startTime')
    ordering = ('name',)
    search_fields = ('name',)
    form = OnAirShowForm