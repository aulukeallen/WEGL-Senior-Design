from django.shortcuts import render
from django.http import HttpResponse
from .models import MediaRecord
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):

    entries = MediaRecord.objects.order_by('artist')

    return render(request, "physicalmedia/index.html", {"entries": entries})