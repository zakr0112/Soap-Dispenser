from django.shortcuts import render
from .models import Dispenser
from django.db import connection



def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Dispenser_ID, Room_ID, Dis_Content, Level_Liquid FROM dispenser")
        soaps = cursor.fetchall()

    return render(request, 'dispenser/home.html', {'dispensers': soaps})