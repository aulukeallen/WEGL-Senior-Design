

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import DJ, AttendanceRecord
from .models import OnAirShowDJ
from .forms import DjInfoForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required

show_dict = {
    0 : "Monday",
    1 : "Tuesday",
    2 : "Wednesday",
    3 : "Thursday",
    4 : "Friday",
    5 : "Saturday",
    6 : "Sunday"
}

@login_required
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

@login_required
def attendance(request):
    records = AttendanceRecord.objects.all()
    search_query = request.GET.get('search', '').strip()
    sort_order = request.GET.get('sort', 'desc')

    if search_query:
        records = records.filter(dj__firstName__icontains=search_query) | records.filter(dj__lastName__icontains=search_query)

    if sort_order == 'asc':
        records = records.order_by('absenceCount')
    else:
        records = records.order_by('-absenceCount')

    print(records)
    return render(request, "djrecord/attendance.html", {"data": records})

@login_required
def clock_in(request):
    # Get the DJ associated with the current user
    try:
        dj = request.user.dj_profile
    except DJ.DoesNotExist:
        return HttpResponse("No DJ profile associated with this user.", status=403)

    # Get current time and weekday
    import datetime
    now = datetime.datetime.now()
    current_time = now.time()
    current_weekday = (now.weekday() + 1) % 7

    # Find shows for this DJ within ±15 minutes of now
    from .models import OnAirShow
    time_window_start = (datetime.datetime.combine(now.date(), current_time) - datetime.timedelta(minutes=15)).time()
    time_window_end = (datetime.datetime.combine(now.date(), current_time) + datetime.timedelta(minutes=15)).time()

    for show in OnAirShow.objects.filter(djs=dj):
        print(current_weekday)
        print(f"Show: {show.name}, Day: {show.day}, Start Time: {show.startTime}")
    # Get shows for today (by weekday) and within the time window
    show = OnAirShow.objects.filter(
        djs=dj,
        day=current_weekday,
        startTime__gte=time_window_start,
        startTime__lte=time_window_end
    ).first()

    if show:
        print(show.name, show.startTime)

    # Set present=True for each OnAirShowDJ record for these shows
    
    if show:
        print(show.name)
        onairshowdj = OnAirShowDJ.objects.filter(onairshow=show, dj=dj).first()
        if onairshowdj:
            onairshowdj.present = True
            onairshowdj.save()

    return render(request, "djrecord/clockin.html", {"dj": dj, "show": show, "now": now, "clocked_in": True if show else False})