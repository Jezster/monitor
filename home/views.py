from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import device_addform
from .models import MonitoredDevice
import requests
import urllib3
import json

# Create your views here.

def openSession(ipaddress, username, password):
	headers = {
		'Host': ipaddress,
		'content-type': 'application/json',
		'Connection': 'keep-alive'
	}
	payload = "{\"login\": {\r\n      \"password\":\""+password+"\",\r\n      \"username\":\""+username+"\"}}"
	url = "https://"+ipaddress+"/sdwan/nitro/v1/config/login?action=add"
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	r = requests.Session()
	login = r.post (url ,data=payload, headers=headers, verify=False)
	print("Connect Successful")
	return r

def getSystemOptions(r, ipaddress):
	headers = {
		'Host': ipaddress,
		'content-type': 'application/json',
		'Connection': 'keep-alive'
	}
	Systemstatusurl = "https://"+ipaddress+"/sdwan/nitro/v1/config/system_options"
	load_status = r.get (Systemstatusurl, headers=headers)
	system_status = load_status.json()
	return system_status

def getVP(r, ipaddress):
	headers = {
		'Host': ipaddress,
		'content-type': 'application/json',
		'Connection': 'keep-alive'
	}
	VPstatusurl = "https://"+ipaddress+"/sdwan/nitro/v1/monitor/virtual_paths"
	load_status = r.get (VPstatusurl, headers=headers)
	vp_status = load_status.json()
	return vp_status

def monitor_device(request):
	device_name = request.GET.get('device')
	device = MonitoredDevice.objects.filter(hostname=device_name).first()
	ipaddress = device.ipaddress
	username = device.username
	password = device.password

	try:
		r = openSession(ipaddress, username, password)
		print(r)
		vp_status = getVP(r, ipaddress)
		system_status = getSystemOptions(r, ipaddress)
		args = {
			"title": "SDWAN Monitor",
			"vpStatus": vp_status,
			"system": system_status
		}
		print(args)
		return render(request, "home/status.html", args)

	except:
		return render(request, "home/failed.html", {"title": "Not Connected"})

def homepage(request):
	return render(request, "home/home.html", {'title': 'Home'})


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

def list_devices(request):
	context = {
		'title': 'List Devices',
		'device_list': MonitoredDevice.objects.all()
	}
	if 'delete' in request.POST:
		device = request.POST['delete']
		MonitoredDevice.objects.filter(hostname=device).delete()
	elif 'monitor' in request.POST:
		device = request.POST['monitor']
		return redirect('/monitor_device/'+device)

	return render(request, 'home/list_devices.html', context)

    

    