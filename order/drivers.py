
#esta función usa una tecnica de scrapping web para traer los datos del json desde github
def drivers():
    import requests
    from bs4 import BeautifulSoup
    import json
    url = 'https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json'
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'html.parser')
    site_json=json.loads(s.text)
    data = site_json['alfreds']
    return data

#Esta función es la que me dice la proximidad de cada conductor a las coordenadas entregadas por el usuario y nos dice si esta disponible u ocupado
def near_drivers(data, data_get):
    from .models import Appointment
    import pandas as pd
    from scipy import spatial
    import numpy as np
    import datetime
    #creamos dataframes a partir de los datos puesto que estos facilitan la manipulación de los datos
    df = pd.DataFrame(data)
    df.drop(['lastUpdate'], axis=1, inplace=True)
    df[['lat', 'lng']] = df[['lat', 'lng']].astype(float)
    df_i = pd.DataFrame(data_get)
    df_i[['lat', 'lng']] = df_i[['lat', 'lng']].astype(float)
    df_drivers = df[['id']]
    #usamos la libreria scipy para calcular la minima distancia entre 2 puntos
    df_drivers["distancia_min"] = np.min(spatial.distance.cdist(
        df[["lng", "lat"]], df_i[["lng", "lat"]]
        ), axis=1)
    #Reducimos la cantidad de decimales a 2
    df_drivers['distancia_min'] = pd.Series([round(val,2) for val in df_drivers['distancia_min']])
    disponibilidad = []

    appointment = Appointment.objects.filter(date=data_get['date'][0])

    """crea una lista con la disponibilidad de cada conductor, al iniciar todos los conductores estan disponibles.
    Despues revisamos si estos estan en la base de datos con pedidos a la fecha ingresada por el cliente.
    De ser asi revisamos si la hora ingresada esta en un rango de la hora en la bd + 1 hora de ser asi el estado de disponiblidad pasa de
    Disponible a ocupado y rompe el ciclo """
    for i in range(len(df_drivers)):
        disponibilidad.append('Disponible')
        for item in appointment:
            time = item.hora
            tmp_datetime = datetime.datetime.combine(datetime.date(1, 1, 1), time)
            hour_ago = (tmp_datetime + datetime.timedelta(hours=1)).time()
            hour_comming = datetime.datetime.strptime(data_get['time'][0], '%H:%M').time()
            if item.driver == df_drivers['id'].iloc[i]:
                if hour_comming >= time and hour_comming <= hour_ago:
                    disponibilidad[i] = 'Ocupado'
                    break
                
    df_drivers['Disponibilidad'] = disponibilidad    
    #Organizamos el df de menor a mayor en cuanto a la distancia entre los 2 puntos
    df_drivers = df_drivers.sort_values('distancia_min')
    #Convertimos el df en json
    js = df_drivers.to_json(orient = 'records')
    return js
