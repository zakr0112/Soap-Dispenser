from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64

class Site(models.Model):
    Site_ID = models.CharField(max_length=4, primary_key=True)
    site_Name = models.CharField(max_length=32)
    Address = models.CharField(max_length=64)
    Phone_Number = models.BigIntegerField(null=True, blank=True)
    Email = models.EmailField(max_length=64)

class Building(models.Model):
    Building_ID = models.CharField(max_length=6, primary_key=True)
    Site_ID = models.ForeignKey(Site, on_delete=models.CASCADE)
    Floors = models.PositiveSmallIntegerField()
    Address = models.CharField(max_length=32)
    Phone_Number = models.BigIntegerField()
    Email = models.EmailField(max_length=32)

class Room(models.Model):
    Room_ID = models.CharField(max_length=6, primary_key=True)
    Building_ID = models.ForeignKey(Building, on_delete=models.CASCADE)
    Room_Type = models.CharField(max_length=32, null=True, blank=True)
    Priority_Level = models.PositiveSmallIntegerField()

class Dispenser(models.Model):
    Dispenser_ID = models.CharField(max_length=6, primary_key=True)
    Room_ID = models.ForeignKey(Room, on_delete=models.CASCADE)
    Dis_content = models.CharField(max_length=9)
    Level_Liquid = models.PositiveSmallIntegerField(null=True, blank=True)

class DispenserResolved(models.Model):
    siteName = models.CharField(max_length=32)
    roomType = models.CharField(max_length=32)
    dispenserID = models.CharField(max_length=6)
    dispenserContent = models.CharField(max_length=9)
    dispenserLevelLiquid = models.PositiveSmallIntegerField()
    dispenserPercentage = models.DecimalField(decimal_places=2, max_digits=8)
    dispenserStatus = models.CharField(max_length=10)

    def __str__(self):
        return self.siteName

class Stockroom(models.Model):
    Stockroom_ID = models.CharField(max_length=6, primary_key=True)
    Site_ID = models.ForeignKey(Site, on_delete=models.CASCADE)
    Soap_Amount = models.PositiveIntegerField()
    Sanitizer_Amount = models.PositiveIntegerField()

class Supervisor(models.Model):
    Supervisor_ID = models.CharField(max_length=6, primary_key=True)
    Firstname = models.CharField(max_length=16)
    Surname = models.CharField(max_length=16)
    DOB = models.DateField()
    Address = models.CharField(max_length=32)
    Email = models.EmailField(max_length=32)
    Phone_Number = models.BigIntegerField()
    Salary = models.PositiveIntegerField()
    Hire_Date = models.DateField()
    Staff_Manager = models.CharField(max_length=32)

class Restock(models.Model):
    Restock_ID = models.CharField(max_length=6, primary_key=True)
    Supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    Soap_Amount_Bought = models.PositiveIntegerField()
    Sanitizer_Amount_Bought = models.PositiveIntegerField()
    soap_price = models.PositiveIntegerField()
    sanitizer_Price = models.PositiveIntegerField()
    Total = models.PositiveIntegerField()
    Company = models.CharField(max_length=32)
    Delivery_Date = models.DateField()

class RoomRestock(models.Model):
    Restock = models.ForeignKey(Restock, on_delete=models.CASCADE)
    Stockroom = models.ForeignKey(Stockroom, on_delete=models.CASCADE)

class Rota(models.Model):
    Rota_ID = models.CharField(max_length=6, primary_key=True)
    Site = models.ForeignKey(Site, on_delete=models.CASCADE)
    Supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    Staff_Amount = models.PositiveIntegerField()
    Rota_Date = models.DateField()

class Cleaner(models.Model):
    Cleaner_ID = models.CharField(max_length=6, primary_key=True)
    Firstname = models.CharField(max_length=16)
    Surname = models.CharField(max_length=16)
    DOB = models.DateField()
    Address = models.CharField(max_length=64)
    Email = models.EmailField(max_length=64)
    Phone_Number = models.BigIntegerField()
    Salary = models.PositiveIntegerField()
    Hire_Date = models.DateField()
    Staff_Manager = models.CharField(max_length=32)

class Shift(models.Model):
    Shift_ID = models.CharField(max_length=6, primary_key=True)
    Cleaner = models.ForeignKey(Cleaner, on_delete=models.CASCADE)
    Rota = models.ForeignKey(Rota, on_delete=models.CASCADE)
    Start_Time = models.PositiveSmallIntegerField()
    Finish_Time = models.PositiveSmallIntegerField()
    Overtime = models.PositiveSmallIntegerField(null=True, blank=True)
    Unsocial_Hours = models.CharField(max_length=5)

class Collection(models.Model):
    Collection_ID = models.CharField(max_length=6, primary_key=True)
    Dispenser = models.ForeignKey(Dispenser, on_delete=models.CASCADE)
    Collection_Date = models.DateField()
    Collection_Time = models.PositiveSmallIntegerField()
    Liquid_Level = models.CharField(max_length=3)

    def __str__(self):
        return self.Dispenser_ID
