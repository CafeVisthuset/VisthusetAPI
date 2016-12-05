'''
Created on 9 nov. 2016

@author: Adrian
'''
from django.forms import ModelForm
from .models import Booking
from database.models import Bike, BikeExtra

'''
TODO:
* Lägg in en kalender där det går att bläddra i bokningar
* Gör det möjligt att välja vilka cyklar som ska ingå i en bokning
'''

class BikesForm(ModelForm):
    
    class Meta:
        model = Bike
        fields = []
        
class BikeExtraForm(ModelForm):
    class Meta:
        model = BikeExtra
        fields = ['name', 'number']
        
class Bookingform(ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_id', ]
        
