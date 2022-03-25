from django.urls import path
from .views import *

urlpatterns = [
    path('api/post', Post_APIView.as_view()), 
    path('api/drivers', Drivers_APIView.as_view()), 
    path('api/appointments', Appointments_APIView.as_view()), 
    path('api/driver', Driver_APIView.as_view()), 
    
        
]