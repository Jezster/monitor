from django import forms
from .models import MonitoredDevice


class device_addform(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())
	ipaddress = forms.GenericIPAddressField(label = 'Management IP Address')

	class Meta:
		model = MonitoredDevice
		fields = ['hostname', 'ipaddress', 'username', 'password']


class device_editform(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())
	ipaddress = forms.GenericIPAddressField(label = 'Management IP Address')

	class Meta:
		model = MonitoredDevice
		fields = ['hostname', 'ipaddress', 'username', 'password']