from django.shortcuts import render
from .models import SoapDispenser
from django.db import connection



def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, soap_level, last_refill FROM dispenser")
        soaps = cursor.fetchall()

    return render(request, 'dispenser/home.html', {'dispensers': soaps})