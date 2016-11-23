from django.contrib import admin
from .models import Dagskassa
from Economy.models import Employee
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(Dagskassa)    
class CashierAdmin(admin.ModelAdmin):
    order = 'date'
    fieldsets = [
        (None,      {'fields' : [ 'date']}),
        ('Kontant/Kort', {'fields' : ['cash', 'card']}),
        ('Specificerad försäljning', {'fields': ['cafeSales', 'iceCreamSales',
                                      'foodShopSales', 'bikeSales', 'booksSales',
                                      'other12Sales', 'other25Sales']}),
        ('Signering',                 {'fields': ['Signatur', 'comment']}),
        ]
    list_display = (
        'date','cafeSales', 'iceCreamSales', 'foodShopSales', 
        'bikeSales', 'booksSales', 'other12Sales', 'other25Sales', 'Signatur',
        'comment')
    list_filter = ['date', 'signature']
    search_fields = ['date', 'signature']
    
    def Signatur(self, obj):
        return "%s %s" % (obj.signature.first_name, obj.signature.last_name)

class UserInLine(admin.TabularInline):
    model = Employee
    can_delete = False

       
class UserAdmin(BaseUserAdmin):
    fieldsets = [
        ('Personuppgifter',          {'fields': ['user', 'person_number']}),
        ('Löneuppgifter',   {'fields': ['wage', 'tax', 'drawTax']}),
        ]
    inlines = (UserInLine, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Personuppgifter',          {'fields': ['user', 'person_number']}),
        ('Löneuppgifter',   {'fields': ['wage', 'tax', 'drawTax']}),
        ]
    
    list_display = ['Förnamn', 'Efternamn', 'wage', 'hours_worked', 'drawTax']
    def Förnamn(self, obj):
        return obj.user.first_name
    
    def Efternamn(self, obj):
        return obj.user.last_name