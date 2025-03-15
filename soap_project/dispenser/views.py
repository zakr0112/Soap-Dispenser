from django.shortcuts import render
from .models import Dispenser
from django.db import connection
from .models import DispenserResolved
from django.http import JsonResponse
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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
        cursor.execute("SELECT Site_ID, Site_Name, Address, Phone_Number, Email FROM SITE")
        soaps = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("SELECT Building_ID, Site_ID, Floors, Address, Phone_Number, Email FROM BUILDING")

    return render(request, 'dispenser/sites.html', {'dispensers': soaps})

def dispenser_resolved(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM vwDispenserResolved")
        soaps = cursor.fetchall()

    if not soaps:  # Check if empty
        return render(request, 'dispenser/DispenserList.html', {'dispensers': None})

    paginator = Paginator(soaps, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'dispenser/DispenserList.html', {'page_obj': page_obj})

def get_collection_data(request, dispenser_id):
   with connection.cursor() as cursor:
      cursor.execute("SELECT COLLECTION_ID, formatted_timedate, liquidMl FROM vwCollectionWithFormatting WHERE Dispenser_ID = %s LIMIT 10", [dispenser_id])
      collection_data = cursor.fetchall()

   # Convert to dictionary format for JSON response
   collection_list = [
      {"collection_id": row[0], "timedate": row[1], "level": row[2]}
      for row in collection_data
   ]
   return JsonResponse(collection_list, safe=False)
