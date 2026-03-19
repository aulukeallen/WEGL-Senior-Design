from django.shortcuts import render
from django.http import HttpResponse
from .models import DJ

# Create your views here.
def index(request):
    data = DJ.objects.all()
    print(data)
    return render(request, "djrecord/index.html", {"data": data})