from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import DJ
from .forms import DjInfoForm

# Create your views here.
def index(request):
    data = DJ.objects.all()
    print(data)
    return render(request, "djrecord/index.html", {"data": data})

# CREATE
def create_dj(request):
    print('create_dj view called')
    data = DJ.objects.all()
    if request.method == 'POST':
        form = DjInfoForm(request.POST)
        if form.is_valid():
            form.save()
            print('success creating DJ')
            return redirect('djrecord:index')
        else:
            print('form errors:', form.errors)
            return render(request, "djrecord/index.html", {'form': form, 'data': data})
    # For GET, redirect to index (no separate create page)
    return redirect('djrecord:index')

# EDIT
def edit_dj(request, pk):
    print('edit_dj view called with pk:', pk)
    item = get_object_or_404(DJ, pk=pk)
    data = DJ.objects.all()
    if request.method == 'POST':
        form = DjInfoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('djrecord:index')
        else:
            return render(request, "djrecord/index.html", {'form': form, 'data': data})
    # For GET, redirect to index (no separate edit page)
    return redirect('djrecord:index')

# DELETE
def delete_dj(request, pk):
    print('delete_dj view called with pk:', pk)
    item = get_object_or_404(DJ, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('djrecord:index')
    # For GET, redirect to index (no separate delete page)
    return redirect('djrecord:index')