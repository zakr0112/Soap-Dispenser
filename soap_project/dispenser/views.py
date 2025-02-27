from django.shortcuts import render
from .models import SoapDispenser

def home(request):
    dispensers = SoapDispenser.objects.all()
    return render(request, 'dispenser/home.html', {'dispensers': dispensers})
