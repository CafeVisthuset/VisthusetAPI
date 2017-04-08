'''
Created on 9 nov. 2016

@author: Adrian
'''
from django import forms
from .models import Booking, Lunch
from database.models import BikeExtra, Bike, LunchBooking, BikesBooking,\
    BikeAvailable
from .choices import Lunch_Choices, Action_Choices, YEARS, MONTHS
from django.forms.formsets import BaseFormSet
from django.forms.widgets import SelectDateWidget
from django.forms.models import BaseModelForm
from datetime import timedelta, date
from database.choices import Day_Choices
from database.validators import positive_integer


'''
TODO:
* Lägg in en kalender där det går att bläddra i bokningar
* Gör det möjligt att välja vilka cyklar som ska ingå i en bokning
* 
'''
class BikesForm(forms.ModelForm):
    
    class Meta:
        model = Bike
        fields = ['number', 'bikeKeyNo', 'wheelsize', 'attribute', 'extra']
        
class BikeExtraForm(forms.ModelForm):
    class Meta:
        model = BikeExtra
        fields = ['name', 'number']
        
class AutomaticBikeBookingForm(forms.ModelForm):
    from_date = forms.DateField()
    duration = forms.CharField(widget=SelectDateWidget, required = False) 
                                   #choices=[Day_Choices + [(timedelta(hours=4), 'Halvdag')]])
    quantity = forms.IntegerField()
    
class BikeBookingForm(forms.ModelForm):
    bike = forms.ModelChoiceField(queryset=Bike.objects.all(), required=False)
    from_date = forms.DateField(widget=SelectDateWidget(years=YEARS, months=MONTHS))
    to_date = forms.DateField(widget=SelectDateWidget(years=YEARS, months=MONTHS))
    
    class Meta:
        model = BikesBooking
        fields = ['bike', 'full_days', 'from_date', 'to_date', 'subtotal']
        readonly_fields = ['subtotal']
        
    def clean(self):
        cleaned_data = super(BikeBookingForm, self).clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        bike = cleaned_data.get('bike')
        
        if from_date > to_date:
            raise forms.ValidationError(
                'Startdatumet får inte vara före slutdatumet')
        
        bike_dates = [date for date in BikeAvailable.objects.filter(bike=bike, available=True)]
        numdays = to_date.day - from_date.day
        date_list = [(from_date + timedelta(days=x)) for x in range(0,numdays + 1)]
        
        if date_list not in bike_dates:
            raise forms.ValidationError(
                'Denna cykel är inte ledig mellan dessa datum'
                )
            
class LunchBookingForm(forms.ModelForm):
    type = forms.ModelChoiceField(queryset=Lunch.objects.all())
    class Meta:
        model = LunchBooking
        fields = ['type', 'quantity', 'day', 'subtotal']
        help_texts = {'quantity': 'Hur många av den givna lunchen?'}
        label = {'quantity': 'kvantitet', 'subtotal': 'delsumma',
                 'type': 'Lunchtyp'}
        
###############################################################################
'''
Create forms for creating new available bikes

TODO:
# Se till att felet som visas om datumen inte stämmer överens visas i HTML-fältet.
'''
  


class CreateAvailableBikeForm(forms.Form): 
    action = forms.ChoiceField(choices=Action_Choices, required=False)
    bike = forms.ModelChoiceField(queryset=Bike.objects.all(), label='Välj cykel...',
                                  required=False)
    from_date = forms.DateField(widget=SelectDateWidget(years=YEARS, months=MONTHS,
                                        empty_label='Välj...'))
    to_date = forms.DateField(widget=SelectDateWidget(years=YEARS, months=MONTHS,
                                        empty_label='Välj...'))
    

class BaseCreateAvailableBikeFormset(BaseFormSet):
    def clean(self):
        '''
        Cleaning
        '''
        #cleaned_data = super(BikeBookingForm, self).clean()
        #for form in self.forms:
        #    from_date = cleaned_data.get('from_date')
        #    to_date = cleaned_data.get('to_date')
        
        #    if from_date > to_date:
        #        raise forms.ValidationError(
        #            'Startdatumet får inte vara före slutdatumet')
                

class BookingForm(forms.Form):
    # Dates and time
    start_date = forms.DateField(required=True,
                                 initial=date.today(),
                                 widget=forms.SelectDateWidget)
    duration = forms.ChoiceField(choices=Day_Choices, required=True)
    
    # Bikes and extras
    number_adult_bikes = forms.ChoiceField(
        initial=2,
        choices=[(number, '%s' % (number)) for number in range(0,11)])
    number_child_bikes = forms.ChoiceField(
        choices=[(number, '%s' % (number)) for number in range(0,4)])
    number_extras = forms.MultipleChoiceField(
        choices=BikeExtra.objects.all())
    
    # Lunches
    number_veg_lunches = forms.IntegerField(validators=[positive_integer])
    number_meat_lunches = forms.IntegerField(validators=[positive_integer])
    number_fish_lunches = forms.IntegerField(validators=[positive_integer])
    
    # Guest info
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    phone_number = forms.CharField(max_length=25, required=False)
    email = forms.EmailField()
    newsletter = forms.BooleanField(
        initial = True,
        help_text= 'Vill du ha nyheter och erbjudanden från oss?')
    
    # Extra message
    other = forms.CharField(widget=forms.Textarea, max_length=200, required=False)
