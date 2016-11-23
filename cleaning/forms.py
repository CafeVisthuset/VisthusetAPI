'''
Created on 9 nov. 2016

@author: Adrian
'''
from django.forms.models import ModelForm
from django import forms
from cleaning.models import Freezer, Fridge, FridgeTemp, FreezerTemp
from django.contrib.auth.models import User
# Special Choice Fields for models
class ColdStorageChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return"%s, %s"%(obj.type, obj.location)
    
class NameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.first_name, obj.last_name)
    
# Forms for models
class FreezerForm(ModelForm):
    class Meta:
        model = Freezer
        fields = ['type', 'location' ]

class FridgeForm(ModelForm):
    class Meta:
        model = Fridge
        fields = ['type', 'location']

class FridgeControlForm(ModelForm):
    unit = ColdStorageChoiceField(queryset=Fridge.objects.all())
    signature = NameChoiceField(queryset=User.objects.all())
    class Meta:
        model = FridgeTemp
        fields = ['date', 'unit', 'measured', 'cleaned', 'signature', 'comment']
        
class FreezerControlForm(ModelForm):
    unit = ColdStorageChoiceField(queryset=Freezer.objects.all())
    class Meta:
        model = FreezerTemp
        fields = ['date', 'unit', 'measured', 'defrosted', 'cleaned', 'signature',
                  'comment']
