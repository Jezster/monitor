from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import device_addform, device_editform
from .models import MonitoredDevice
from requests.auth import HTTPBasicAuth
from django.core.validators import ip_address_validators
from django.core.exceptions import ValidationError
import requests
import urllib3
import json

# Create your views here.

def dnac_login(host, username, password):
    url = "https://{}/api/system/v1/auth/token".format(host)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {
        'content-type': "application/json",
        'x-auth-token': ""
    }
    response = requests.request("POST", url, auth=HTTPBasicAuth(username, password), headers=headers, verify=False)
    return response.json()["Token"]

def network_device_list(host, token):
    url = "https://{}/api/v1/network-device".format(host)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {
        'content-type': "application/json",
        'x-auth-token': token
    }
    response = requests.get(url, headers=headers, verify=False)
    data = response.json()
    return data

def monitor_device(request):
    device_name = request.GET.get('device')
    device = MonitoredDevice.objects.filter(hostname=device_name).first()
    ipaddress = device.ipaddress
    username = device.username
    password = device.password

    try:
        login = dnac_login(ipaddress, username, password)
        system_status = network_device_list(ipaddress, login)
        args = {
            "dnacname": device_name,
			"title": "DNAC Server Monitor",
            "system": system_status
        }
        print(args)
        return render(request, "home/status.html", args)

    except:
        return render(request, "home/failed.html", {"title": "Not Connected"})

def aboutpage(request):
	return render(request, "home/about.html", {'title': 'About'})

def load_devices(request):
	if request.method == 'POST':
		form = device_addform(request.POST)
		try:
			if form.is_valid:
				form.save()
				hostname = form.cleaned_data.get('hostname')
				messages.success(request, f'Device successfully added: {hostname}')
				return redirect('load_devices')
		except:
			messages.warning(request, 'Error in entry - please try again (check IP)')
			return redirect('load_devices')

	else:
		form = device_addform()
	return render(request, 'home/load_devices.html', {'form': form, 'title': 'Add Device'})

def edit_devices(request):
    device_name = request.GET.get('device')
    if request.method == 'POST':
        form = device_editform(request.POST, instance=MonitoredDevice.objects.filter(hostname=device_name).first())
        try:
            if form.is_valid:
                form.save()
                hostname = form.cleaned_data.get('hostname')
                messages.success(request, f'Device successfully updated: {hostname}')
                return redirect('edit_devices')
        except:
            messages.warning(request, 'Error in entry - please try again (check IP)')
            return redirect('edit_devices')

    else:
        form = device_editform(instance=MonitoredDevice.objects.filter(hostname=device_name).first())

    return render(request, 'home/edit_devices.html', {'form': form, 'title': 'Edit Device'})

def list_devices(request):
    args = {
        'title': 'List Devices',
        'device_list': MonitoredDevice.objects.all()
    }
    if 'delete' in request.POST:
        device = request.POST['delete']
        MonitoredDevice.objects.filter(hostname=device).delete()
    elif 'monitor' in request.POST:
        device = request.POST['monitor']
        return redirect('/monitor_device/'+device)
    elif 'edit' in request.POST:
        device = request.POST['edit']
        return redirect('/edit_device/'+device)

    return render(request, 'home/list_devices.html', args)