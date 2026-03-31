from django.shortcuts import render
from django.http import HttpResponse
from .models import AttendanceRecord

# Create your views here.
def index(request):
    from .forms import AttendanceSearchForm
    form = AttendanceSearchForm(request.GET or None)
    data = AttendanceRecord.objects.all()
    search_query = request.GET.get('search', '').strip()
    sort_order = request.GET.get('sort', 'desc')
    if search_query:
        data = data.filter(djName__icontains=search_query)
    if sort_order == 'asc':
        data = data.order_by('absenceCount')
    else:
        data = data.order_by('-absenceCount')
    return render(request, "attendancetracker/index.html", {"data": data, "form": form})