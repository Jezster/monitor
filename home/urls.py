from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.list_devices, name="home_page"),
    path('about/', views.aboutpage, name="about_page"),
    path('load_devices/', views.load_devices, name="load_devices"),
    path('monitor_device/', views.monitor_device, name="monitor_device"),
    path('edit_device/', views.edit_devices, name="edit_devices")
]
