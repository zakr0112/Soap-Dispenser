from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64

class Site(models.Model):
    site_id = models.CharField(max_length=4, primary_key=True)
    site_name = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    phone_number = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=64)

class Building(models.Model):
    building_id = models.CharField(max_length=6, primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    floors = models.PositiveSmallIntegerField()
    address = models.CharField(max_length=32)
    phone_number = models.BigIntegerField()
    email = models.EmailField(max_length=32)

class Room(models.Model):
    room_id = models.CharField(max_length=6, primary_key=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=32, null=True, blank=True)
    priority_level = models.PositiveSmallIntegerField()

class Dispenser(models.Model):
    Dispenser_ID = models.CharField(max_length=6, primary_key=True)
    Room_ID = models.ForeignKey(Room, on_delete=models.CASCADE)
    Dis_content = models.CharField(max_length=9)
    Level_Liquid = models.PositiveSmallIntegerField(null=True, blank=True)

class Stockroom(models.Model):
    stockroom_id = models.CharField(max_length=6, primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    soap_amount = models.PositiveIntegerField()
    sanitizer_amount = models.PositiveIntegerField()

class Supervisor(models.Model):
    supervisor_id = models.CharField(max_length=6, primary_key=True)
    firstname = models.CharField(max_length=16)
    surname = models.CharField(max_length=16)
    dob = models.DateField()
    address = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)
    phone_number = models.BigIntegerField()
    salary = models.PositiveIntegerField()
    hire_date = models.DateField()
    staff_manager = models.CharField(max_length=32)

class Restock(models.Model):
    restock_id = models.CharField(max_length=6, primary_key=True)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    soap_amount_bought = models.PositiveIntegerField()
    sanitizer_amount_bought = models.PositiveIntegerField()
    soap_price = models.PositiveIntegerField()
    sanitizer_price = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    company = models.CharField(max_length=32)
    delivery_date = models.DateField()

class RoomRestock(models.Model):
    restock = models.ForeignKey(Restock, on_delete=models.CASCADE)
    stockroom = models.ForeignKey(Stockroom, on_delete=models.CASCADE)

class Rota(models.Model):
    rota_id = models.CharField(max_length=6, primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    staff_amount = models.PositiveIntegerField()
    rota_date = models.DateField()

class Cleaner(models.Model):
    cleaner_id = models.CharField(max_length=6, primary_key=True)
    firstname = models.CharField(max_length=16)
    surname = models.CharField(max_length=16)
    dob = models.DateField()
    address = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    phone_number = models.BigIntegerField()
    salary = models.PositiveIntegerField()
    hire_date = models.DateField()
    staff_manager = models.CharField(max_length=32)

class Shift(models.Model):
    shift_id = models.CharField(max_length=6, primary_key=True)
    cleaner = models.ForeignKey(Cleaner, on_delete=models.CASCADE)
    rota = models.ForeignKey(Rota, on_delete=models.CASCADE)
    start_time = models.PositiveSmallIntegerField()
    finish_time = models.PositiveSmallIntegerField()
    overtime = models.PositiveSmallIntegerField(null=True, blank=True)
    unsocial_hours = models.CharField(max_length=5)

class Collection(models.Model):
    collection_id = models.CharField(max_length=6, primary_key=True)
    dispenser = models.ForeignKey(Dispenser, on_delete=models.CASCADE)
    collection_date = models.DateField()
    collection_time = models.PositiveSmallIntegerField()
    liquid_level = models.CharField(max_length=3)

    def __str__(self):
        return self.Dispenser_ID
