from django.db import models
from django.db.models.fields.related import ForeignKey
from django.db.models.deletion import CASCADE, PROTECT

class Date(models.Model):
    date = models.DateField()
    time = models.TimeField()
    
    def __init__(self, auto_now=True):
        return self.date, self.time

class Employee(models.Model):
    id = models.IntegerField(
        primary_key=True)
    
    firstName = models.CharField(
        max_length=20)
    
    lastName = models.CharField(
        max_length=50)
    
    personNo = models.IntegerField()
    
    wage = models.DecimalField(
        max_digits=6, decimal_places=2)
    
    hours_worked = models.DecimalField(
        max_digits=6, decimal_places=2)

    def __str__(self):
        return self.firstName, self.lastName

class Guest(models.Model):
    id = models.IntegerField(primary_key = True)
    firstName = models.CharField(max_length = 30)
    lastName = models.CharField(max_length = 30)
    phoneNumber = models.IntegerField()
    eMailAdress = models.EmailField()
    
    def __str__(self):
        return self.firstName, self.lastName, self.eMailAdress
    
class Bike(models.Model):
    id = models.IntegerField(primary_key = True)
    bikeKeyNo = models.IntegerField()
    rentOutCount = models.IntegerField(default = 0)
        
class CleanPoint(models.Model):
    id = models.IntegerField(primary_key = True)
    pointType = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    cleanTask = models.CharField(max_length = 200)
    maxTemp = models.IntegerField()
    minTemp = models.IntegerField()

    def __str__(self):
        return self.pointType, self.description, self.cleanTask

class CleanDay(models.Model):
    cleanDate_id = Date.date
    
    cleanPoint_id = models.ForeignKey(
        'CleanPoint',
        on_delete=models.PROTECT
        )
    
    Employee_id = models.ForeignKey(
        'Employee',
        on_delete=models.PROTECT
        )
    
    temperatureMeasured = models.IntegerField()
    completed = models.BooleanField(default = False)
    
class Cashier(models.Model):
    countingDay = Date.date
    
    cash = models.DecimalField(
        max_digits = 7, decimal_places = 2)
    
    card = models.DecimalField(
        max_digits = 7, decimal_places = 2)
    
    cafeSales = models.DecimalField(
        max_digits = 7, decimal_places = 2)
    
    iceCreamSales = models.DecimalField(
        max_digits = 7, decimal_places = 2)
    
    foodShopSales = models.DecimalField(
        max_digits = 7, decimal_places = 2)
    
    bikeSales = models.DecimalField(
        max_digits = 7, decimal_places = 2)
    
    booksSales = models.DecimalField(
        max_digits = 7, decimal_places = 2)
    
    other12Sales = models.DecimalField(
        max_digits = 7, decimal_places = 2)
    
    other25Sales = models.DecimalField(
        max_digits = 7, decimal_places = 2)
    
class Damages(models.Model):
    bike_id = models.ForeignKey(
        'Bike',
        on_delete=models.PROTECT
        )
    
    damageType = models.CharField(max_length = 200 )
    repaired = models.BooleanField(default = False)
    repairedBy = models.ForeignKey(
        'Employee',
        on_delete=models.PROTECT
        )
    def __str__(self):
        return self.damageType
    
class BikesBooking(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    bookingDate = models.ForeignKey(
        'Date',
        on_delete=models.PROTECT
        )
    
    bookingGuest = models.ForeignKey(
        'Guest',
        on_delete=models.PROTECT
        )
    
    bikes = models.ForeignKey(
        'Bike',
        on_delete=models.PROTECT
        )
    
