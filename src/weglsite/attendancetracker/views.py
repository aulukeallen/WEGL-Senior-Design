from django.shortcuts import render
from django.http import HttpResponse
from .models import AttendanceRecord

# Create your views here.
def index(request):
    data = AttendanceRecord.objects.all()
    print(data)
    return render(request, "attendancetracker/index.html", {"data": data})