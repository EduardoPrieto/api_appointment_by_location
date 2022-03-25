from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('drivers', views.drivers, name='drivers'),
    path('new_appointment', views.new_appointment, name='new_appointment'),
    path('appointments', views.appointments, name='appointments'),
]