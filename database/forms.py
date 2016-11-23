'''
Created on 9 nov. 2016

@author: Adrian
'''
from django.forms import ModelForm
from .models import Booking

'''
TODO:
* Lägg in en kalender där det går att bläddra i bokningar
* Gör det möjligt att välja vilka cyklar som ska ingå i en bokning
'''
class Bookingform(ModelForm):
    class Meta:
        model = Booking
        fields = ['Booking_id', ]
        
