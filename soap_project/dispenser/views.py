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


# Dispenser handling...
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

# Dispenser collection data (bootstrap modal form / ajax ) data...
def get_collection_data(request, dispenser_id):
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM vwCollectionWithFormatting WHERE Dispenser_ID = %s ORDER BY Collection_Date DESC LIMIT 30", [dispenser_id])
      collection_data = cursor.fetchall()

   # Convert to dictionary format for JSON response
   collection_list = [
      {
         "collection_id": row[0],
         "timedate": row[1],
         "level": row[2]
      }
      for row in collection_data
   ]
   return JsonResponse(collection_list, safe=False)


# Cleaner handling...
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

# Cleaner (bootstrap modal form / ajax ) data...
def get_cleaner_data(request, cleaner_id):
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM CLEANER WHERE Cleaner_ID = %s", [cleaner_id])
      row = cursor.fetchone()
   print("Requested Cleaner ID:", cleaner_id)
   print("Fetched Row:", row)
   if row:
      # Map the raw tuple to a dictionary
      data = {
         "Cleaner_ID": row[0],
         "Firstname": row[1],
         "Surname": row[2],
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

# Supervisor handling...
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

# Supervisor (bootstrap modal form / ajax ) data...
def get_supervisor_data(request, supervisor_id):
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM SUPERVISOR WHERE Supervisor_ID = %s", [supervisor_id])
      row = cursor.fetchone()
   print("Requested Supervisor ID:", supervisor_id)
   print("Fetched Row:", row)
   if row:
      # Map the raw tuple to a dictionary
      data = {
         "Supervisor_ID": row[0],
         "Firstname": row[1],
         "Surname": row[2],
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
      return JsonResponse({"error": "Supervisor not found"}, status=404)

def restock(request):
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM vwRestockByCompanyTotal")
      currestock = cursor.fetchall()

   paginator = Paginator(currestock, 10)
   page_number = request.GET.get('page', 1)
   try:
      page_obj = paginator.page(page_number)
   except PageNotAnInteger:
      page_obj = paginator.page(1)
   except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
   return render(request, 'dispenser/stock.html', {'page_obj': page_obj})

def get_restock_data(request, company):
   with connection.cursor() as cursor:
      cursor.execute("SELECT Restock_ID, Soap_Amount_Bought, Soap_Price, Sanitizer_Amount_Bought, Sanitizer_Price, Total, Delivery_Date FROM RESTOCK WHERE Company = %s ORDER BY Delivery_Date DESC LIMIT 30", [company])
      restock_data = cursor.fetchall()

   restock_list = [
      {
         "Restock_ID": row[0],
         "Soap_Amount_Bought": row[1],
         "Soap_Price": "{:.2f}".format(row[2]),
         "Sanitizer_Amount_Bought": row[3],
         "Sanitizer_Price": "{:.2f}".format(row[4]),
         "Total": "{:.2f}".format(row[5]),
         "Delivery_Date": row[6].strftime('%d/%m/%Y') if row[6] else "N/A"
      }
      for row in restock_data
   ]
   return JsonResponse(restock_list, safe=False)
