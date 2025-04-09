from django.shortcuts import render
from .models import Dispenser
from django.db import connection
from .models import DispenserResolved
from django.http import JsonResponse
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
   return render(request, 'dispenser/home.html')

def shifts(request):
   # 01/04/2025 Renamed curors for easier debugging
   # 09/04/2025 more specific select rather than everything also added pagination
   with connection.cursor() as cursor:
      cursor.execute("SELECT shiftID, shiftStarttime, shiftFinishtime, shiftOvertime, shiftUnsocialhours, cleanerFirstname, cleanerSurname, cleanerID FROM vwSiteRotaShiftCleanerResolved")
      cur_shifts = cursor.fetchall()

   paginator = Paginator(cur_shifts, 20)
   page_number = request.GET.get('page', 1)
   try:
      page_obj = paginator.page(page_number)
   except PageNotAnInteger:
      page_obj = paginator.page(1)
   except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
   return render(request, 'dispenser/shifts.html', {'page_obj': page_obj})

def stock(request):
   # 01/04/2025
   # Renamed curors for easier debugging
   with connection.cursor() as cursor:
      cursor.execute("SELECT Restock_ID, Supervisor_ID, Soap_Amount_Bought, Sanitizer_Amount_Bought, Soap_Price, Sanitizer_Price, Total, Company, Delivery_Date FROM RESTOCK")
      cur_restock = cursor.fetchall()
      companies_dict = {}

   for restock_recs in cur_restock:
      company = restock_recs[7]
      restock_id = restock_recs[0]

      if company not in companies_dict:
         companies_dict[company] = []

      companies_dict[company].append(restock_id)

   return render(request, 'dispenser/stock.html', {'companies_dict': companies_dict, 'dispensers': cur_restock})


def sites(request):
   # 01/04/2025
   # Renamed curors for easier debugging
   with connection.cursor() as cursor:
      cursor.execute("SELECT Site_ID, Site_Name, Address, Phone_Number, Email FROM SITE")
      cur_sites = cursor.fetchall()

   with connection.cursor() as cursor:
      cursor.execute("SELECT Building_ID, Site_ID, Floors, Address, Phone_Number, Email FROM BUILDING")
   return render(request, 'dispenser/sites.html', {'dispensers': cur_sites})


# Dispenser handling...
def dispenser_resolved(request):
   # 01/04/2025
   # Renamed curors for easier debugging
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM vwDispenserResolved")
      cur_dispenserresolved = cursor.fetchall()
   if not cur_dispenserresolved:  # Check if empty
      return render(request, 'dispenser/DispenserList.html', {'dispensers': None})

   paginator = Paginator(cur_dispenserresolved, 20)
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
   # 01/04/2025
   # Renamed curors for easier debugging
   # Changed to select just the columns required rather than everything
   with connection.cursor() as cursor:
      cursor.execute("SELECT fmtDatetime, liquidMl, fillPercentage, fillStatus FROM vwCollectionWithFormatting WHERE Dispenser_ID = %s ORDER BY Collection_Date DESC, Collection_Time DESC LIMIT 30", [dispenser_id])
      cur_collection = cursor.fetchall()

   collection_list = [
      {
         "fmtDatetime": row[0],
         "liquidMl": row[1],
         "fillPercent": row[2],
         "fillStatus": row[3]
      }
      for row in cur_collection
   ]
   return JsonResponse(collection_list, safe=False)


# Cleaner handling...
def cleaners(request):
   # 01/04/2025
   # Renamed curors for easier debugging
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM CLEANER")
      cur_cleaner = cursor.fetchall()

   paginator = Paginator(cur_cleaner, 20)
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
   # 01/04/2025
   # Renamed curors for easier debugging
   # added limit 1 to sql statement
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM CLEANER WHERE Cleaner_ID = %s LIMIT 1", [cleaner_id])
      cur_cleaner = cursor.fetchone()
   if cur_cleaner:
      # Map the raw tuple to a dictionary
      data = {
         "Cleaner_ID": cur_cleaner[0],
         "Firstname": cur_cleaner[1],
         "Surname": cur_cleaner[2],
         "DOB": cur_cleaner[3].strftime('%d/%m/%Y') if cur_cleaner[3] else "N/A",
         "Address": cur_cleaner[4],
         "Email": cur_cleaner[5],
         "Phone_Number": cur_cleaner[6],
         "Salary": cur_cleaner[7],
         "Hire_Date": cur_cleaner[8].strftime('%d/%m/%Y') if cur_cleaner[8] else "N/A",
         "Staff_Manager": cur_cleaner[9],
      }
      return JsonResponse(data)
   else:
      return JsonResponse({"error": "Cleaner not found"}, status=404)


# Supervisor handling...
def supervisors(request):
   # 01/04/2025
   # Renamed curors for easier debugging
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM SUPERVISOR")
      cur_supervisors = cursor.fetchall()

   paginator = Paginator(cur_supervisors, 20)
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
   # 01/04/2025
   # Renamed curors for easier debugging
   # Added limit 1 to sql
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM SUPERVISOR WHERE Supervisor_ID = %s LIMIT 1", [supervisor_id])
      cur_supervisor = cursor.fetchone()
   if cur_supervisor:
      # Map the raw tuple to a dictionary
      data = {
         "Supervisor_ID": cur_supervisor[0],
         "Firstname": cur_supervisor[1],
         "Surname": cur_supervisor[2],
         "DOB": cur_supervisor[3].strftime('%d/%m/%Y') if cur_supervisor[3] else "N/A",
         "Address": cur_supervisor[4],
         "Email": cur_supervisor[5],
         "Phone_Number": cur_supervisor[6],
         "Salary": cur_supervisor[7],
         "Hire_Date": cur_supervisor[8].strftime('%d/%m/%Y') if cur_supervisor[8] else "N/A",
         "Staff_Manager": cur_supervisor[9],
      }
      return JsonResponse(data)
   else:
      return JsonResponse({"error": "Supervisor not found"}, status=404)


# Restock handling...
def restock(request):
   # 01/04/2025
   # Renamed curors for easier debugging
   with connection.cursor() as cursor:
      cursor.execute("SELECT * FROM vwRestockByCompanyTotal")
      cur_restock = cursor.fetchall()

   paginator = Paginator(cur_restock, 20)
   page_number = request.GET.get('page', 1)
   try:
      page_obj = paginator.page(page_number)
   except PageNotAnInteger:
      page_obj = paginator.page(1)
   except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
   return render(request, 'dispenser/stock.html', {'page_obj': page_obj})


def get_restock_data(request, company):
   # getting potentially 30 records
   with connection.cursor() as cursor:
      cursor.execute("SELECT Restock_ID, Soap_Amount_Bought, Soap_Price, Sanitizer_Amount_Bought, Sanitizer_Price, Total, Delivery_Date FROM RESTOCK WHERE Company = %s ORDER BY Delivery_Date DESC LIMIT 30", [company])
      cur_restock = cursor.fetchall()

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
      for row in cur_restock
   ]
   return JsonResponse(restock_list, safe=False)
