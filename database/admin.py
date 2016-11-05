from django.contrib import admin
from .models import Bike, BikesBooking, Cashier, CleanPoint, CleanDay, Employee, Damages, Date 
from database.models import Guest

# allow user to add dates when booking
admin.site.register(Date)
class DateInLine(admin.TabularInline):
    model = Date
    extra = 2

@admin.register(Bike)
class BikesAdmin(admin.ModelAdmin):
    fields = ('id', 'bikeKeyNo')
    exclude = ['rentOutCount']
    order = 'id'
    list_display = ('id', 'rentOutCount')
        
class BikesInLine(admin.TabularInline):
    model = Bike
    extra = 0
        
# register bikes for users
class BookingsAdmin(admin.ModelAdmin):
    '''fieldsets = [
        (None,          {'fields': ['booking_id', 'bookingDate']}),
        ('Bikes',       {'fields': ['bikes'], 'classes' : ['collapse']}),
        ]'''
    
    inlines = [BikesInLine]
    
admin.site.register(BikesBooking, BookingsAdmin)

# Guest table
#class GuestInLine(admin.TabularInline):
#    model = Guest
    
class GuestAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields': [('firstName', 'lastName')]}),
        ('Contact details', {'fields': ['phoneNumber', 'eMailAdress']})
        ]
    exclude = ('id',)
    list_display = ('firstName', 'lastName', 'phoneNumber', 'eMailAdress')
    
    search_fields = ['firstName', 'lastName']
    
#    inlines = [GuestInLine]
    
admin.site.register(Guest, GuestAdmin)
#register cash everyday for users
admin.site.register(Cashier)
# register EKP points for users
admin.site.register(CleanDay)
# allow user to create cleanPoint
admin.site.register(CleanPoint)
# allow user to create bike


