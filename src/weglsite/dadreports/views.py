from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import CSVUploadForm
from .models import CSVUpload, AsplayEntry
from .utils import parse_csv
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):

    token = get_token(request)
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['csvFile']
            try:
                upload = parse_csv(f, filename=f.name)
                messages.success(request, f"Imported {upload.rowCount} entries from '{f.name}'.")
                return redirect('dadreports:index')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = CSVUploadForm()

    
    recentPlayback = AsplayEntry.objects.order_by("-playDate").exclude(group="IDS")
    recentPlayback = recentPlayback.exclude(group='SHORTPSA')
    recentPlayback = recentPlayback.exclude(group='LONGPSA')[:20]
    uploads = CSVUpload.objects.order_by("-uploadDate")

    context = {
        "form": form,
        "recentPlayback": recentPlayback,
        "uploads": uploads
    }

    return render(request, 'dadreports/index.html', context)