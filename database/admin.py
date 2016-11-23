from django.contrib import admin
from .models import Bike, Booking
from database.models import Guest

# register bikes for users
@admin.register(Bike)
class BikesAdmin(admin.ModelAdmin):
    fields = ('id', 'bikeKeyNo')
    exclude = ['rentOutCount']
    order = 'id'
    list_display = ('id', 'rentOutCount')
        
#Allows editing of Bookings
@admin.register(Booking)
class BookingsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': ['booking_id', 'bookingDate']}),
        ]

# Guest table
@admin.register(Guest)    
class GuestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': [('firstName', 'lastName')]}),
        ('Kontaktuppgifter', {'fields': ['phoneNumber', 'eMailAdress']})
        ]
    exclude = ('id',)
    list_display = ('firstName', 'lastName', 'phoneNumber', 'eMailAdress')
    
    search_fields = ['firstName', 'lastName']