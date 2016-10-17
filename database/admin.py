from django.contrib import admin
from .models import Bike, BikesBooking, Cashier, CleanPoint, CleanDay, Employee, Damages 

# register bikes for users
admin.site.register(BikesBooking)
#register cash everyday for users
admin.site.register(Cashier)
# register EKP points for users
admin.site.register(CleanDay)
# allow user to create cleanPoint
admin.site.register(CleanPoint)
# allow user to create bike
@admin.register(Bike)
class BikesAdmin(admin.ModelAdmin):
    fields = ('id', 'bikeKeyNo')
