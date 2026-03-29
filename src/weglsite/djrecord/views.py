
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
    data = DJ.objects.all()
    search_query = request.GET.get('search', '').strip()
    if search_query:
        data = data.filter(
            Q(firstName__icontains=search_query) |
            Q(lastName__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    return render(request, "djrecord/index.html", {"data": data, "form": form})

# # CREATE
# def create_dj(request):
#     print('create_dj view called')
#     data = DJ.objects.all()
#     if request.method == 'POST':
#         form = DjInfoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print('success creating DJ')
#             return redirect('djrecord:index')
#         else:
#             print('form errors:', form.errors)
#             return render(request, "djrecord/index.html", {'form': form, 'data': data})
#     # For GET, redirect to index (no separate create page)
#     return redirect('djrecord:index')

# # EDIT
# def edit_dj(request, pk):
#     print('edit_dj view called with pk:', pk)
#     item = get_object_or_404(DJ, pk=pk)
#     data = DJ.objects.all()
#     if request.method == 'POST':
#         form = DjInfoForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('djrecord:index')
#         else:
#             return render(request, "djrecord/index.html", {'form': form, 'data': data})
#     # For GET, redirect to index (no separate edit page)
#     return redirect('djrecord:index')

# # DELETE
# def delete_dj(request, pk):
#     print('delete_dj view called with pk:', pk)
#     item = get_object_or_404(DJ, pk=pk)
#     if request.method == 'POST':
#         item.delete()
#         return redirect('djrecord:index')
#     # For GET, redirect to index (no separate delete page)
#     return redirect('djrecord:index')