

Lo primero que tenemos que hacer para correr el proyecto es hacer las respectivas migraciones usando el comando 

`python manage.py makemigrations`

Después corremos las migraciones

`python manage.py migrate`

Las librerías usadas están contenidas en requeriments.txt, por lo que es necesario correrlo

Una vez terminemos estos pasos podremos usar la orden 

`python manage.py runserver`

aunque el proyecto era un api se crearon algunas vistas para facilitar probar la api, el código esta documentado con el fin de facilitar su entendimeinto
