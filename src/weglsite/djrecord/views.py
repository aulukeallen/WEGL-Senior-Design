
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import DJ
from .forms import DjInfoForm
from django.db.models import Q

# Create your views here.
def index(request):
    from .forms import DjInfoForm
    from .forms_search import DJSearchForm
    form = DJSearchForm(request.GET or None)
    djs = DJ.objects.all()
    search_query = request.GET.get('search', '').strip()
    if search_query:
        djs = djs.filter(
            Q(firstName__icontains=search_query) |
            Q(lastName__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(shows__name__icontains=search_query)
        ).distinct()
    # Prefetch related shows for efficiency
    djs = djs.prefetch_related('shows')
    return render(request, "djrecord/index.html", {"djs": djs, "form": form})