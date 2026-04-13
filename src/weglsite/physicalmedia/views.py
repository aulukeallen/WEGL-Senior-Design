from django.shortcuts import render
from django.http import HttpResponse
from .models import MediaRecord
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

@login_required
def index(request):
    search = request.GET.get("search", "")
    filterMedium = request.GET.get("medium", "")

    queryset = MediaRecord.objects.order_by('artist')

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(artist__icontains=search)
        )
    if filterMedium:
        queryset = queryset.filter(medium=filterMedium)

    paginator = Paginator(queryset, 25)
    pageNumber = request.GET.get("page")
    pageObj = paginator.get_page(pageNumber)

    context = {
        "page_obj": pageObj,
        "search": search,
        "filterMedium": filterMedium,
        "mediums": MediaRecord.objects.values_list("medium", flat=True).distinct()
    }
    return render(request, "physicalmedia/index.html", context)