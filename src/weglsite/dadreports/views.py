from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import CSVUploadForm
from .models import CSVUpload, AsplayEntry
from .utils import parse_csv
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

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

    
    allPlayback = AsplayEntry.objects.order_by("-playDate")

    recentPlayback = allPlayback.exclude(group="IDS").exclude(group='SHORTPSA').exclude(group='LONGPSA')

    search = request.GET.get("search", "")
    filterGroup = request.GET.get("group", "")
    filterDate = request.GET.get("date", "")

    if search:
        queryset = allPlayback.filter(
            Q(title__icontains=search) |
            Q(artist__icontains=search) |
            Q(album__icontains=search)
        )
    else:
        queryset = recentPlayback

    if filterGroup:
        queryset = queryset.filter(group=filterGroup)
    if filterDate:
        queryset = queryset.filter(playDate=filterDate)

    paginator = Paginator(queryset, 50)
    pageNumber = request.GET.get("page")
    pageObj = paginator.get_page(pageNumber)

    uploads = CSVUpload.objects.order_by("-uploadDate")

    context = {
        "form": form,
        "page_obj": pageObj,
        "uploads": uploads,
        "search": search,
        "filterGroup": filterGroup,
        "filterDate": filterDate,
        "groups": AsplayEntry.objects.values_list("group", flat=True).distinct()
    }

    return render(request, 'dadreports/index.html', context)