from django.db import models

class SoapDispenser(models.Model):
    name = models.CharField(max_length=100) 
    soap_level = models.FloatField(help_text="Soap Level in percentage") 
    last_refill = models.CharField(max_length=19, help_text="Formated: YYYY-MM-DD HH:MM:SS")

    def __str__(self):
        return self.name
