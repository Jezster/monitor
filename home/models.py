from django.db import models

# Create your models here.
class MonitoredDevice(models.Model):
	hostname	= models.CharField(max_length = 100)
	ipaddress	= models.GenericIPAddressField()
	username	= models.CharField(max_length = 100)
	password	= models.CharField(max_length = 100)

	def __str__(self):
		return self.hostname