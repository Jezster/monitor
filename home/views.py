from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import device_addform

# Create your views here.
def homepage(request):
	return render(request, "home/home.html")

def aboutpage(request):
	return render(request, "home/about.html", {'title': 'About'})

def load_devices(request):
	if request.method == 'POST':
		form = device_addform(request.POST)
		if form.is_valid:
			form.save()
			hostname = form.cleaned_data.get('hostname')
			messages.success(request, f'Device successfully added: {hostname}')
			return redirect('load_devices')

	else:
		form = device_addform()
	return render(request, 'home/load_devices.html', {'form': form, 'title': 'Add Device'})