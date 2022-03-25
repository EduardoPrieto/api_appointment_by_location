from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializers
from .models import Appointment
from rest_framework import status
import datetime
import requests
from django.http import Http404
from .drivers import drivers, near_drivers

#registro en la DB de los pedidos, requiso 1 
class Post_APIView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        """appointment = Appointment.objects.all()
        serializer = PostSerializers(appointment, many=True)"""
        data = drivers()
        
        return Response(data)

    def post(self, request, format=None):
        post_data = request.GET
        params = {'driver':post_data['driver'],'date':post_data['date'],'hora':post_data['time'],'lat_origin':post_data['lat_origin'],'lng_origin':post_data['lng_origin'],'lat_destination':post_data['lat_destination'],'lng_destination':post_data['lng_destination'],'description':post_data['description']}
        serializer = PostSerializers(data=params)
        appointment = Appointment.objects.filter(driver=post_data['driver'], date = post_data['date'])
        if appointment:
            for item in appointment:
                #Revisamos si ya hay un pedido para ese conductor con esa fecha y rango de hora
                time = item.hora
                tmp_datetime = datetime.datetime.combine(datetime.date(1, 1, 1), time)
                hour_ago = (tmp_datetime + datetime.timedelta(hours=1)).time()
                hour_comming = datetime.datetime.strptime(post_data['time'], '%H:%M').time()
                #si la hora que digita el usuario es mayor o igual a la hora que ya esta en la base de datos o menos que la hora de la DB +1 no le permitira ingresarlo a la DB
                if (hour_comming >= time and hour_comming <= hour_ago):
                    return Response(status=status.HTTP_208_ALREADY_REPORTED)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# filtro de conductores por fecha, hora y cercania, requisito 4
class Drivers_APIView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        data = drivers()
        data_get = request.GET
        params = {'date':[data_get['date']],'time':[data_get['time']],'lat':[data_get['lat']],'lng':[data_get['lng']]}
        driver_json = near_drivers(data, params)
                    
        
        return Response(driver_json)

""""Revisión de pedidos por conductor o fecha.
Puesto que el codigo para revisión de pedidos por conductor y fecha o por fecha es practicamente el mismo decidi hacer los requisitos 2 y 3 juntos
el codigo funciona tanto si se entrega solo la fecha como si se entrega fecha y conductor""" 
class Appointments_APIView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        data_get = request.GET
        if data_get['driver']  == '':
            appointment = Appointment.objects.filter(date=data_get['date']).order_by('hora')
            #appointment = Appointment.objects.all().order_by('hora')
            serializer = PostSerializers(appointment, many=True)
            return Response(serializer.data)
        else:
            appointment = Appointment.objects.filter(date=data_get['date'], driver=data_get['driver']).order_by('hora')
            if appointment:
                serializer = PostSerializers(appointment, many=True)
                return Response(serializer.data)
            else:
                serializer = 'error'

# Entrega la lista de conductores
class Driver_APIView(APIView):

    def get(self, request, format=None, *args, **kwargs):
        driver = drivers()
        return Response(driver)
