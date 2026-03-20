from django.shortcuts import render
from django.http import HttpResponse
from .models import MediaRecord

# Create your views here.
def index(request):

    entries = MediaRecord.objects.order_by('artist')

    return render(request, "physicalmedia/index.html", {"entries": entries})