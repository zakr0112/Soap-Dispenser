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
        cursor.execute("SELECT SHIFT_ID, Cleaner_ID, Start_Time, Finish_Time FROM SHIFT")
        soaps = cursor.fetchall()
    return render(request, 'dispenser/shifts.html', {'dispensers': soaps})

def stock(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Restock_ID, Supervisor_ID, Soap_Amount_Bought, Sanitizer_Amount_Bought, Soap_Price, Sanitizer_Price, Total, Company, Delivery_Date FROM RESTOCK")
        soaps = cursor.fetchall()
        companies_dict = {}

    for soap in soaps:
        company = soap[7]  
        restock_id = soap[0] 

        if company not in companies_dict:
            companies_dict[company] = []

        companies_dict[company].append(restock_id)

    return render(request, 'dispenser/stock.html', {'companies_dict': companies_dict, 'dispensers': soaps})

def sites(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT Dispenser_ID, Room_ID, Dis_Content, Level_Liquid FROM dispenser")
        soaps = cursor.fetchall()
    return render(request, 'dispenser/sites.html', {'dispensers': soaps})