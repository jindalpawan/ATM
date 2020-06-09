
from django.contrib import admin
from django.urls import path, include
from machine import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('machine.urls')),
]
