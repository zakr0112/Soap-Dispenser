from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Dispenser)
admin.site.register(DispenserResolved)
admin.site.register(Stockroom)
admin.site.register(Supervisor)
admin.site.register(Restock)
admin.site.register(RoomRestock)
admin.site.register(Rota)
admin.site.register(Shift)
admin.site.register(Collection)
