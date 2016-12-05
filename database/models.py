from django.db import models
from Economy.models import Employee
from .choices import *
from .validators import validate_booking_date, validate_preliminary
from datetime import date
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
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
    # Gör det möjligt att ange om bokningar är preleminära
    # Gör det möjligt att föra statistik över sålda paket
    # Lägg in tillgänglighet för cyklar vissa datum
    
* Gör managers till bokningsmodellerna för att kunna göra sökningar
* Lägg in modeller för generiska bokningar/eventbokningar
* Lägg in funktion för att skapa bokningsnummer

'''
def validate_discount_code(value):
    found = False
    for item in Discount_codes.objects.all():
        if value == item.code:
            found = True
            break
        
    if found == False:
        raise ValidationError(
                '''rabattkoden verkar inte finnas i vårt system, 
                vänligen kontakta oss om problemet kvarstår'''
                )
        
# Guest information
'''
class Guest(models.Model):
    user = models.OneToOneField(
        User,
        limit_choices_to={'is_guests': True}
        )
    firstName = models.CharField(max_length = 25)
    lastName = models.CharField(max_length = 25)
    phoneNumber = models.CharField(max_length = 15)
    eMailAdress = models.EmailField(max_length = 50)
    
    def __str__(self):
        return "%s %s" % (self.firstName, self.lastName)
'''    
# Lunch models
class Lunch(models.Model):
    type = models.CharField(choices=Lunch_Choices, default='vegetarian', max_length= 15, verbose_name='lunchalternativ')
    price = models.PositiveIntegerField(default = 95, verbose_name='pris')
    #allergens
    
    class Meta:
        verbose_name = 'lunch'
        verbose_name_plural = 'luncher'
        
class Utilities(models.Model):
    class Meta:
        verbose_name= 'tillbehör'
        
# Bike models
class Bike(models.Model):
    number = models.PositiveIntegerField(null= True, verbose_name= 'Nummer')
    bikeKeyNo = models.CharField(max_length= 15, blank= True, verbose_name='Cykelnyckel')
    rentOutCount = models.IntegerField(default = 0, verbose_name='antal uthyrningar')
    wheelsize = models.CharField(choices=Bike_Wheelsize_Choices, max_length= 10,
                                 verbose_name='Däckdiameter', null=True)
    attribute = models.CharField(choices=Bike_Attribute_Choices, max_length= 10,
                                 verbose_name='vuxen/barn', null=True)
    extra = models.CharField(choices=Bike_Extra_Choices, max_length= 15,
                             verbose_name='Knuten till tillbehör', blank=True)
    
    
    def __str__(self):
        return "%scykel %s" % (self.attribute, self.number)
    
    class Meta:
        verbose_name = 'cykel'
        verbose_name_plural = 'cyklar'
        ordering = ['-attribute', 'number']
        unique_together = ['number', 'attribute']
        
class BikeExtra(models.Model):
    name = models.CharField(max_length= 10, choices=Bike_Extra_Choices, verbose_name= 'cykeltillbehör')
    number = models.PositiveIntegerField(default= None, verbose_name= 'Nummer')
    attached_to = models.CharField(max_length= 10, blank=True, verbose_name= 'knuten till cykel')
    
    def __str__(self):
        return "%s %s" % (self.name, self.id)

class Damages(models.Model):
    bike_id = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        verbose_name = 'Skada på cykel'
        )
    discoveredBy = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name = 'upptäckt av',
        related_name= 'Discovered_by',
        blank=True,
        null = True,
        )
    discoveredDate = models.DateField(default= date.today, verbose_name='Skada upptäckt')
    repairedDate = models.DateField(default= date.today, verbose_name= 'Skada reparerad')
    damageType = models.TextField(max_length = 200, verbose_name= 'beskrivning av skada' )
    repaired = models.BooleanField(default = False, verbose_name = 'lagad (J/N)')   
    repairedBy = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        blank = True,
        null = True,
        verbose_name= 'lagad av',
        related_name= 'repaired_by', 
        )
    
    def __str__(self):
        return self.damageType
    
    class Meta:
        verbose_name = 'skada'
        verbose_name_plural = 'skador'
        ordering = ['repaired', 'discoveredDate']
        
#Accomodation models
class Accomodation(models.Model):
    name = models.CharField(max_length=30, verbose_name= 'boendeanläggning')
    classification = models.CharField(max_length=10, verbose_name= 'klass')
    telephone = models.CharField(max_length=15, verbose_name='telefon')
    adress = models.CharField(max_length= 25, verbose_name= 'gatuadress')
    postCode = models.CharField(max_length=8, verbose_name='postkod')
    location= models.CharField(max_length=25, verbose_name='ort')
    email = models.EmailField(verbose_name='E-postadress')
    website = models.URLField(verbose_name='hemsida')
    
    def __str__(self):
        return self.name
    
    def get_full_adress(self):
        return [self.adress, str(self.postCode) +'   ' + self.location]
    
    class Meta:
        verbose_name = 'boendeanläggning'
        verbose_name_plural = 'boendeanläggningar'
        
class Rooms(models.Model):
    name = models.CharField(null=True, max_length=25, verbose_name='namn')
    standard = models.CharField(choices=Room_Standard_Choices, max_length=20, verbose_name='standard')
    max_guests = models.PositiveIntegerField(verbose_name='Max antal gäster')
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0, 
                                verbose_name="pris exkl. moms")
    describtion = models.TextField(max_length=255, blank=True, verbose_name='Beskrivning')
    owned_by =models.ForeignKey(
        Accomodation,
        verbose_name='anläggning',
        null= True
        )
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'rum'
        ordering = ['owned_by']

# Booking models
class Discount_codes(models.Model):
    code = models.CharField(max_length=15, verbose_name= 'kod')
    guest = models.ForeignKey(
        User,
        limit_choices_to={'is_guests': True},
        verbose_name = 'gäst',
        null = True
        )
    
class Booking(models.Model):
    booking_id = models.PositiveIntegerField(primary_key=True, verbose_name='boknings id')
    booking_date = models.DateField(default=date.today, verbose_name='bokningsdatum', validators=
                                    [])
    preliminary = models.BooleanField(default= False, verbose_name='preliminär')
    longest_prel = models.DateTimeField(verbose_name='längsta preliminärbokning', null=True,
                                        validators= [validate_preliminary])
    payed = models.BooleanField(default= False, verbose_name='betald')
    startDate = models.DateField(verbose_name='datum för avresa', blank=True, null=True, validators=
                                 [])
    endDate = models.DateField(verbose_name='datum för hemresa', blank=True, null=True, validators=
                               [])
    discount_code = models.CharField(blank=True, null=True, max_length=15, verbose_name= 'rabattkod',
                                     validators = [validate_discount_code])
    numberOfGuests = models.IntegerField(null= False, default = 2, verbose_name='antal gäster')
    guest = models.OneToOneField(
        User,
        limit_choices_to={'is_guests': True},
        on_delete=models.CASCADE,
        verbose_name='gäst',
        blank=True,
        null= True,
        )
    bikes = models.ManyToManyField(
        Bike,
        verbose_name='cyklar',
        blank=True,
#        limit_choices_to= Q(Booking.objects.filter(booking__bikes = '') and )
        )
    
    bike_extras = models.ManyToManyField(
        BikeExtra,
        verbose_name= 'cykeltillbehör',
        blank=True,
        )
    accomodation = models.ManyToManyField(
        Accomodation,
        verbose_name='boende',
        blank=True,
        )
    utilities = models.ManyToManyField(
        Utilities,
        verbose_name='tillbehör',
        blank=True
        )
    other = models.TextField(max_length = 255, blank= True, verbose_name= 'övrigt')
    
    def __str__(self):
        return u'[{0}] 0{1}'.format(self.booking_date, self.booking_id)
    
    class Meta:
        verbose_name = 'Bokning'
        verbose_name_plural = 'bokningar'
        ordering = ['booking_date']