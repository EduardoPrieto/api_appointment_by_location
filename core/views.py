from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
import requests

# estas vistas no eran obligatorias pero me parecieron pertinentes para probar la api de manera mas fácil
# Cada una de las vistas accede a las api's como se accede normalmente a una independientemente de si estan en el mismo sistema
# Create your views here.
def welcome(request):
    url = 'http://127.0.0.1:8000/api/drivers'
    response = requests.get(url)
    data = ''
    if response.status_code == 200:
        data =  response.json()

    return render(request, "core/base.html", {'data':data})


def drivers(request):
    data = ''
    if request.method == 'POST': 
        post_data = request.POST   
        params = {'date':post_data['date'],'time':post_data['time'],'lat':post_data['lat'],'lng':post_data['lng'],}
        url = 'http://127.0.0.1:8000/api/drivers'
        response = requests.get(url, params=params)       
        if response.status_code == 200:
            data =  response.json()

    return render(request, "core/drivers.html", {'data':data})

def new_appointment(request):
    data = ''
    message = ''
    color = ''
    url = 'http://127.0.0.1:8000/api/post'
    response = requests.get(url)
    if response.status_code == 200:
        data =  response.json()
    if request.method == 'POST': 
        post_data = request.POST 
        url = 'http://127.0.0.1:8000/api/post'
        response = requests.post(url, params=post_data) 
        if response.status_code == 208:
            message = 'Lo sentimos, el conductor que eligio esta ocupado en esa fecha y hora' 
            color = 'orange'
        elif  response.status_code == 201:
            message = 'Pedido creado con exito' 
            color = 'green'
        else:
            message = 'Se ha presentado un error porfavor verifique que los datos sean correctos' 
            color = 'red'

    return render(request, "core/form.html", {'data':data,'message':message,'color':color,})


def appointments(request):
    data = ''
    url = 'http://127.0.0.1:8000/api/driver'
    response = requests.get(url)  
    data =  response.json()
    if request.method == 'POST': 
        post_data = request.POST   
        params = {'date':post_data['date'],'driver':post_data['driver']}
        url = 'http://127.0.0.1:8000/api/appointments'
        response = requests.get(url, params=params)       
        if response.status_code == 200:
            appointments =  response.json()
            return render(request, "core/appointments.html", {'data':data, 'appointments':appointments})

    return render(request, "core/appointments.html", {'data':data})