'''
Created on 12 nov. 2016

@author: Adrian
'''
from .models import Dagskassa
from django.forms import ModelForm, Textarea
from django import forms
from Economy.models import Employee
from django.forms.formsets import formset_factory

"""
    TODO:
    * Lägg till en snyggare css+js-widget för datumet genom en Form Asset.
    * skriv klart labels
    * skriv klart helper_texts
    * lägg till error_messages
"""
class CashForm(ModelForm):
    """
    Formulär för att lägga in dagskassor
    """
    
    class Meta:
        model = Dagskassa
        fields =['date', 'cash', 'card','cafeSales', 'iceCreamSales', 'foodShopSales', 
                 'bikeSales', 'booksSales', 'other12Sales', 'other25Sales', 'signature',
                'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 50, 'rows' : 10}),
            }
        labels = {
            'date': "Datum:",
            'cash': "Kontanter:",
            'card': "Kort:",
            'comment': "Kommentar",
            }
        help_texts = {
            'date' : "vilket datum gäller dagskassan?",
            'comment' : "Om något inte stämmer kan du lägga till en kommentar här",
            }
        widgets = {
            'comment': Textarea(attrs={'cols': 50, 'rows' : 10}),
            }
        labels = {
            'date': "Datum:",
            'cash': "Kontanter:",
            'card': "Kort:",
            'comment': "Kommentar",
            }
        help_texts = {
            'date' : "vilket datum gäller dagskassan?",
            'comment' : "Om något inte stämmer kan du lägga till en kommentar här",
            }
        error_message = {
            'date' : 'Denna måste fyllas i',
            'signature' : 'denna måste fyllas i',
            }

employed_set = Employee.objects.all()
EMPLOYEE_CHOICES = []
for employed in employed_set:
    EMPLOYEE_CHOICES.append((employed.user.first_name, employed.get_full_name()))
                
Date_input = ['%H.%M, %d/%m', ]
Time_Error ={
        'required': 'Du måste fylla i starttid',
        'invalid': 'Fyll i tid med rätt format',
        }

class hoursWorkedForm(forms.Form):
    name = forms.ChoiceField(choices=EMPLOYEE_CHOICES, error_messages={
        'required': 'Du måste fylla i namn',
        })
    startTime = forms.DateTimeField(input_formats=Date_input, error_messages=Time_Error)
    endTime = forms.DateTimeField(input_formats=Date_input, error_messages=Time_Error)
    
    class Meta:
        labels ={'name': 'Namn',
                 'startTime': 'Började:',
                 'endTime': 'Slutade:',
                 }
        help_texts ={
            'name': 'vem jobbade arbetspasset?',
            'startTime': 'När började arbetspasset? Ange i format hh.mm, dd/mm',
            'endTime': 'När slutade arbetspasset? Ange i format hh.mm, dd/mm'
            }
    