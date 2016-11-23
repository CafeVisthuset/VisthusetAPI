from django.contrib import admin
from cleaning.forms import *
'''
TODO:
* Färdigställ utifrån modellen
* Lägg till fält i admin-vyn där dagens, morgonens och att-göra uppgifter syns

'''

@admin.register(Fridge)
class FridgeAdmin(admin.ModelAdmin):
    fields = ['type', 'location', 'active']
    list_display = ['type', 'location', 'active']
    form = FridgeForm
    
@admin.register(Freezer)
class FreezerAdmin(admin.ModelAdmin):
    fields = ['type', 'location', 'active']
    list_display = ['type', 'location', 'active']
    display_radio=['active']
    form = FreezerForm
    
@admin.register(FridgeTemp)
class FridgeControl(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['unit']}),
        ('Temperaturer',    {'fields': ['measured', 'anomaly']}),
        ('Rengöring',      {'fields': ['cleaned']}),
        ('Signering',       {'fields': ['signature']}),
        ]
    list_display = ['date', 'Enhet', 'Signatur', 'anomaly']
    empty_value_display = 'Okänt'
    form = FridgeControlForm
    
    def Signatur(self,obj):
        return "%s %s" % (obj.signature.first_name, obj.signature.last_name)
    
    def Enhet(self, obj):
        return "%s, %s" % (obj.unit.type, obj.unit.location)
    
@admin.register(FreezerTemp)
class FreezerControl(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['unit']}),
        ('Temperaturer',    {'fields': ['measured', 'anomaly']}),
        ('Rengöring',      {'fields': ['cleaned', 'defrosted'] }),
        ('Signering',       {'fields': ['signature']}),
        ]
    list_display = ['date', 'unit', 'signature', 'anomaly']
    form = FreezerControlForm
    
    def Signatur(self,obj):
        return "%s %s" % (obj.signature.first_name, obj.signature.last_name)
    
    def Enhet(self, obj):
        return "%s, %s" % (obj.unit.type, obj.unit.location)
    