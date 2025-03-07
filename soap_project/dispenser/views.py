from django.shortcuts import render
from .models import Dispenser
from django.db import connection



def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Dispenser_ID, Room_ID, Dis_Content, Level_Liquid FROM dispenser")
        soaps = cursor.fetchall()

    return render(request, 'dispenser/home.html', {'dispensers': soaps})


def dispenser_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Dispenser_ID, Room_ID, Dis_Content, Level_Liquid FROM dispenser")
        soaps = cursor.fetchall()
    return render(request, 'dispenser/DispenserList.html', {'dispensers': soaps})

def shifts(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Dispenser_ID, Room_ID, Dis_Content, Level_Liquid FROM dispenser")
        soaps = cursor.fetchall()
    return render(request, 'dispenser/shifts.html', {'dispensers': soaps})

def stock(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Dispenser_ID, Room_ID, Dis_Content, Level_Liquid FROM dispenser")
        soaps = cursor.fetchall()
    return render(request, 'dispenser/stock.html', {'dispensers': soaps})

def sites(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Dispenser_ID, Room_ID, Dis_Content, Level_Liquid FROM dispenser")
        soaps = cursor.fetchall()
    return render(request, 'dispenser/sites.html', {'dispensers': soaps})