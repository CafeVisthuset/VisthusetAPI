'''
Created on 9 nov. 2016

@author: Adrian
'''
from django import forms
from .models import Booking
from database.models import BikeExtra, BikeBooking, Bike, AccomodationBooking

'''
TODO:
* Lägg in en kalender där det går att bläddra i bokningar
* Gör det möjligt att välja vilka cyklar som ska ingå i en bokning
'''
class BikesForm(forms.ModelForm):
    
    class Meta:
        model = Bike
        fields = []
        
class BikeExtraForm(forms.ModelForm):
    class Meta:
        model = BikeExtra
        fields = ['name', 'number']
        
class BikesBookingForm(forms.ModelForm):
    startDate = forms.DateField(widget=forms.SelectDateWidget)
    endDate = forms.DateField(widget=forms.SelectDateWidget)
    
    class Meta:
        model = BikeBooking
        fields = ['numberOfGuests']
        
class AccomodationBookingForm(forms.ModelForm):
    startDate = forms.DateField(widget=forms.SelectDateWidget)
    endDate = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = AccomodationBooking
        fields = ['numberOfGuests', 'other']
              
class Bookingform(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking', ]
        
