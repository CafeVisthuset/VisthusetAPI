from django.db import models
from Economy.models import Employee
'''
TODO:
* Gör klart alla modeller för att kunna genomföra bokningar
    # Grundläggande modeller som bara håller data (ex. cyklar el. utrustning) 
        görs abstrakta
        - Eventuellt: Skadorna är också en underklass av cyklar
    # Bokningsmodeller görs som förlängningar av de abstrakta modellerna
        - cykelbokningar
        - lunchbokningar
        - boendebokningar
        - tillbehörsbokningar (ex cykelkärra)
    # Gör en modell för presentkort och rabattkoder
    # Gör det möjligt att ange om bokningar är preleminära
    # Gör det möjligt att föra statistik över sålda paket
    # Lägg in tillgänglighet för cyklar vissa datum
    
* Gör managers till bokningsmodellerna för att kunna göra sökningar
*Lägg in modeller för generiska bokningar/eventbokningar

'''

class Guest(models.Model):
    firstName = models.CharField(max_length = 25)
    lastName = models.CharField(max_length = 25)
    phoneNumber = models.CharField(max_length = 15)
    eMailAdress = models.EmailField(max_length = 50)
    

    
class Bike(models.Model):
    id = models.IntegerField(primary_key = True)
    bikeKeyNo = models.IntegerField()
    rentOutCount = models.IntegerField(default = 0)
    
    def update_rent_out(self):
        self.rentOutCount += 1
        return self.rentOutCount
    
class Damages(models.Model):
    bike_id = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        )
    
    damageType = models.CharField(max_length = 200 )
    repaired = models.BooleanField(default = False)
    def __str__(self):
        return self.damageType
    repairedBy = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        default=''
        )
    
class Booking(models.Model):
    booking_id = models.IntegerField(primary_key=True)
    booking_date = models.DateField('Booking_Date')

    bikes = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        default = 1
        )
    numberOfGuests = models.IntegerField(default = 2)
