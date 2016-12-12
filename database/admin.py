from django.contrib import admin
from .models import Bike, Booking, BikeAvailable, BikeBooking
from database.models import Damages, Accomodation, Rooms, GuestUser,\
    AccomodationBooking
from Economy.models import Staff
from database.forms import BikesForm, BikesBookingForm, AccomodationBookingForm
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

@admin.register(BikeAvailable)
class BikesAvail(admin.ModelAdmin):
    fields = ['bike', 'start_date', 'end_date']
    
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
        (None,          {'fields': ['type', 'booking', 'booking_date']}),
        ('Info om gästen', {'fields': ['guest', 'numberOfGuests', 'discount_code']}),
        ('Specifikationer', {'fields': ['bikes', 'accomodation', 'utilities']})
        ]
    list_display = ['booking', 'booking_date', 'type', 'guest', 'numberOfGuests']

@admin.register(AccomodationBooking)    
class AccomodationBookingAdmin(admin.ModelAdmin):
    form_class = AccomodationBookingForm
    
    fieldsets = [
        (None,      {'fields': ['booking', 'booking_date']}),
        ('Preliminär', {'classes': ['collapse'],
                        'fields': ['preliminary', 'longest_prel']}),
        ('Specifikationer', {'fields': ['startDate', 'endDate', 'accomodation']}),
        ('Info om gästen', {'fields': ['guest', 'numberOfGuests', 'discount_code']})
        ]
    list_display = ['booking', 'booking_date', 'guest', 'numberOfGuests']

@admin.register(BikeBooking)   
class BikeBookingAdmin(admin.ModelAdmin):
    form = BikesBookingForm
    
    fieldsets = [
        ('Preliminär', {'classes': ['collapse'],
                        'fields': ['preliminary', 'longest_prel']}),
        ('Specifikationer', {'fields': ['startDate', 'endDate', 'bikes']}),
        ('Info om gästen', {'fields': ['guest', 'numberOfGuests', 'discount_code']})
        ]
    
    list_display = ['booking', 'booking_date', 'guest', 'numberOfGuests']
    
    class Meta:
        pass
    
    
class StaffAdmin(UserAdmin):
    pass
    
class GuestAdmin(StaffAdmin):
    pass


admin.site.unregister(User)
admin.site.register(Staff, StaffAdmin)
admin.site.register(GuestUser, GuestAdmin)