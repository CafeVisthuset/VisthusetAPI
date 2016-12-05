from django.contrib import admin
from .models import Bike, Booking
from database.models import Damages, Accomodation, Rooms
from database.forms import BikesForm
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

# Guest table
'''
@admin.register(Guest)    
class GuestAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,          {'fields': [('firstName', 'lastName')]}),
        ('Kontaktuppgifter', {'fields': ['phoneNumber', 'eMailAdress']})
        ]
    list_display = ('firstName', 'lastName', 'phoneNumber', 'eMailAdress')
    
    search_fields = ['firstName', 'lastName']
'''
# register bikes for users
def reset_rent_out_count(self, obj):
    obj.rentOutCount = 0
    return obj.rentOutCount
reset_rent_out_count.short_description = 'Återställ antal uthyrningar till 0'

@admin.register(Bike)
class BikesAdmin(admin.ModelAdmin):
    form = BikesForm
    fields = ['number', 'bikeKeyNo', 'wheelsize', 'attribute', 'extra']
    list_display = ('number', 'attribute', 'wheelsize','rentOutCount')
    
    admin_actions = [reset_rent_out_count, ]  

    
@admin.register(Damages)
class DamagesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['bike_id', 'discoveredDate', 'discoveredBy']}),
        ('Beskrivning', {'fields': ['damageType', ]}),
        ('Lagning',     {'fields': ['repaired', 'repairedBy', 'repairedDate'],
                         'classes': ['collapse', ]}),
        ]
    
    list_display = ['bike_id', 'discoveredDate', 'repaired', 'repairedDate', 'repairedBy']

@admin.register(Accomodation)
class AccomodationAdmin(admin.ModelAdmin):
    # form = AccomodationForm
    list_display = ['name', 'email', 'telephone','website', 'adress_report']
    readonly_fields = ('adress_report', )
    
    def adress_report(self, instance):
        return format_html_join(
            mark_safe('<br/>'),
            '{}',
            ((line, ) for line in instance.get_full_adress()),
            ) or mark_safe("<span class='errors'>I can´t determine this adress</span>")
    adress_report.short_description = 'Adress'
    
@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['name', 'owned_by', 'standard']}),
        ('Specifikationer',     {'fields': ['max_guests', 'price']}),
        (None,          {'fields': ['describtion']}),
        ]
    list_display = ['name', 'owned_by', 'standard', 'max_guests', 'price']
#Allows editing of Bookings
@admin.register(Booking)
class BookingsAdmin(admin.ModelAdmin):
    
    fieldsets = [
        (None,          {'fields': ['booking_id', 'booking_date']}),
        ('Info om gästen', {'fields': ['guest', 'numberOfGuests', 'discount_code']}),
        ('Specifikationer', {'fields': ['bikes', 'accomodation', 'utilities']})
        ]
    