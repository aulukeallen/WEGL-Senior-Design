
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
    filter_outside_hours = request.GET.get('outside_hours', '') == '1'

    if search_query:
        djs = djs.filter(
            Q(firstName__icontains=search_query) |
            Q(lastName__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(shows__name__icontains=search_query)
        ).distinct()

    if filter_outside_hours:
        # 5pm = 17:00:00, 11pm = 23:00:00 for Mon-Fri (1-5), all hours for Sat/Sun (0,6)
        from django.db.models import OuterRef, Exists
        from .models import OnAirShow
        djs = djs.filter(
            Exists(
                OnAirShow.objects.filter(
                    djs=OuterRef('pk'),
                    startTime__isnull=False
                ).filter(
                    (
                        # Mon-Fri: show is between 17:00 and 23:00 (inclusive)
                        (Q(day__in=[1,2,3,4,5]) & Q(startTime__gte="17:00:00") & Q(startTime__lte="23:00:00"))
                        |
                        # Sat/Sun: any time
                        (Q(day__in=[0,6]))
                    )
                )
            )
        )

    djs = djs.prefetch_related('shows')
    return render(request, "djrecord/index.html", {"djs": djs, "form": form, "filter_outside_hours": filter_outside_hours})