from django.shortcuts import render
from .models import Dispenser
from django.db import connection
from .models import DispenserResolved
from django.http import JsonResponse
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return render(request, 'dispenser/home.html')


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


def cleaners(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM CLEANER")
        curcleaner = cursor.fetchall()

        paginator = Paginator(curcleaner, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'dispenser/cleaners.html', {'page_obj': page_obj})

'''
def get_cleaner_data(request, cleaner_id):
    from django.http import JsonResponse
    from .models import Cleaner
    print("Requested Cleaner ID:", cleaner_id)  # For debugging

    try:
        cleaner = Cleaner.objects.get(Cleaner_ID=cleaner_id)
        data = {
            "Cleaner_ID": cleaner.Cleaner_ID,
            "Firstname": cleaner.Firstname,
            "Surname": cleaner.Surname,
            "DOB": cleaner.DOB.strftime('%d/%m/%Y'),  # UK date format
            "Address": cleaner.Address,
            "Email": cleaner.Email,
            "Phone_Number": cleaner.Phone_Number,
            "Salary": cleaner.Salary,
            "Hire_Date": cleaner.Hire_Date.strftime('%d/%m/%Y'),  # UK date format
            "Staff_Manager": cleaner.Staff_Manager,
        }
        return JsonResponse(data)
    except Cleaner.DoesNotExist:
        return JsonResponse({"error": "Cleaner not found"}, status=404)
'''

def get_cleaner_data(request, cleaner_id):
    with connection.cursor() as cursor:
        # Use parameterized query to prevent SQL injection
        cursor.execute("SELECT * FROM CLEANER WHERE Cleaner_ID = %s", [cleaner_id])
        row = cursor.fetchone()

    # Debugging to see if data was fetched
    print("Requested Cleaner ID:", cleaner_id)
    print("Fetched Row:", row)

    if row:
        # Map the raw tuple to a dictionary
        data = {
            "Cleaner_ID": row[0],         # Index 0 corresponds to Cleaner_ID
            "Firstname": row[1],          # Index 1 corresponds to Firstname
            "Surname": row[2],            # Index 2 corresponds to Surname
            "DOB": row[3].strftime('%d/%m/%Y') if row[3] else "N/A",
            "Address": row[4],
            "Email": row[5],
            "Phone_Number": row[6],
            "Salary": row[7],
            "Hire_Date": row[8].strftime('%d/%m/%Y') if row[8] else "N/A",
            "Staff_Manager": row[9],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Cleaner not found"}, status=404)


def supervisors(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM SUPERVISOR")
        cursupervisor = cursor.fetchall()

        paginator = Paginator(cursupervisor, 10)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'dispenser/supervisors.html', {'page_obj': page_obj})


def get_supervisor_data(request, supervisor_id):
    with connection.cursor() as cursor:
        # Use parameterized query to prevent SQL injection
        cursor.execute("SELECT * FROM SUPERVISOR WHERE Supervisor_ID = %s", [supervisor_id])
        row = cursor.fetchone()

    # Debugging to see if data was fetched
    print("Requested Supervisor ID:", supervisor_id)
    print("Fetched Row:", row)

    if row:
        # Map the raw tuple to a dictionary
        data = {
            "Supervisor_ID": row[0],         # Index 0 corresponds to Supervisor_ID
            "Firstname": row[1],          # Index 1 corresponds to Firstname
            "Surname": row[2],            # Index 2 corresponds to Surname
            "DOB": row[3].strftime('%d/%m/%Y') if row[3] else "N/A",
            "Address": row[4],
            "Email": row[5],
            "Phone_Number": row[6],
            "Salary": row[7],
            "Hire_Date": row[8].strftime('%d/%m/%Y') if row[8] else "N/A",
            "Staff_Manager": row[9],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Cleaner not found"}, status=404)

