from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import CSVUploadForm
from .models import CSVUpload, AsplayEntry
from .utils import parse_csv
from django.middleware.csrf import get_token

# Create your views here.
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

    uploads = CSVUpload.objects.order_by('-uploadDate')
    entries = AsplayEntry.objects.select_related('upload').order_by('-playDate', 'startTime')
    return render(request, 'dadreports/index.html', {'uploads': uploads, 'form': form, 'entries': entries})