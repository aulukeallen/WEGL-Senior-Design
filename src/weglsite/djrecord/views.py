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
    if request.method == 'POST':
        form = DjInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dj-list')
    else:
        form = DjInfoForm()
    return render(request, "djrecord/index.html", {'form': form})

# EDIT
def edit_dj(request, pk):
    print('edit_dj view called with pk:', pk)
    item = get_object_or_404(DJ, pk=pk)
    if request.method == 'POST':
        form = DjInfoForm(request.POST, instance=item)  # instance = existing obj
        if form.is_valid():
            form.save()
            return redirect('dj-list')
    else:
        form = DjInfoForm(instance=item)
    return render(request, "djrecord/index.html", {'form': form})

# DELETE
def delete_dj(request, pk):
    print('delete_dj view called with pk:', pk)
    item = get_object_or_404(DJ, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dj-list')
    return render(request, "djrecord/index.html", {'item': item})