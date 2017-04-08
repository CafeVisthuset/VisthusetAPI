from django.db import models
from Economy.models import Employee
from .choices import *
from .validators import validate_booking_date, validate_preliminary
from datetime import date, timedelta, datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from database.helperfunctions import listSum
from database.choices import Day_Choices
'''
TODO:
* Gör klart alla modeller för att kunna genomföra bokningar
    # Gör det möjligt att föra statistik över sålda paket
    
* Gör managers till bokningsmodellerna för att kunna göra sökningar
* Lägg in modeller för generiska bokningar/eventbokningar
* Lägg in funktion för att skapa bokningsnummer

'''

'''
Models for lunches and lunch utilities

'''
class Lunch(models.Model):
    slug = models.SlugField(default='')
    type = models.CharField(choices=Lunch_Choices, default='vegetarian', max_length= 15, verbose_name='lunchalternativ')
    price = models.PositiveIntegerField(default = 95, verbose_name='pris')
    # TODO: implement allergens with lunches
    
    class Meta:
        verbose_name = 'lunch'
        verbose_name_plural = 'luncher'
        
    def __str__(self):
        return self.type

        
class Utilities(models.Model):
    describtion = models.TextField()
    number = models.PositiveIntegerField()
    brand = models.CharField(max_length=5, choices=Brand_choices)
    
    class Meta:
        verbose_name= 'tillbehör'
        

'''
Bike models

Contain a model for bike availability(BikeAvailable) with manager (BikeAvailableManager)
and model for bikes (Bike). It also contains a model for bike extras such as childseats.
Additionally this section contains a model for damages on each bike (Damages).
'''
# Bike model
class Bike(models.Model):
    # Identification
    number = models.PositiveIntegerField(verbose_name= 'Nummer')
    bikeKeyNo = models.CharField(max_length= 15, blank= True, verbose_name='Cykelnyckel')
    
    # For statistics
    rentOutCount = models.IntegerField(default = 0, verbose_name='antal uthyrningar')
    
    # Attributes
    wheelsize = models.CharField(choices=Bike_Wheelsize_Choices, max_length= 10,
                                 verbose_name='Däckdiameter')
    attribute = models.CharField(choices=Bike_Attribute_Choices, max_length= 10,
                                 verbose_name='vuxen/barn')
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
    attached_to = models.OneToOneField(
        Bike, 
        verbose_name= 'knuten till cykel',
        related_name= 'bikeextra',
        null = True,
        blank = True,
        )
    
    def __str__(self):
        return "%s %s" % (self.name, self.id)


class Damages(models.Model):
    bike_id = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        verbose_name= 'Skada på cykel',
        related_name= 'damages',
        )
    
    # Damage description
    discoveredBy = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name = 'upptäckt av',
        related_name= 'discovered_by',
        blank=True,
        null = True,
        )
    discoveredDate = models.DateField(default=date.today, verbose_name='Skada upptäckt')
    repairedDate = models.DateField(default=date.today, verbose_name= 'Skada reparerad', blank=True)
    damageType = models.TextField(max_length = 200, verbose_name= 'beskrivning av skada' )
    
    # Repair status
    repaired = models.BooleanField(default = False, verbose_name = 'lagad (J/N)')   
    repairedBy = models.ForeignKey(
        'Economy.Employee',
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


'''
Models for accomodation. Rooms and Facilities. 
'''
#Accomodation models
class Facility(models.Model):
    # Company
    name = models.CharField(max_length=30, verbose_name= 'boendeanläggning')
    organisation_number = models.CharField(max_length = 12, blank=True)
    
    # Contact details
    telephone = models.CharField(max_length=15, verbose_name='telefon', blank=True)
    email = models.EmailField(verbose_name='E-postadress')
    website = models.URLField(verbose_name='hemsida', blank=True)
   
    # Adress
    adress = models.CharField(max_length= 25, verbose_name= 'gatuadress', blank=True)
    postCode = models.CharField(max_length=8, verbose_name='postkod', blank=True)
    location= models.CharField(max_length=25, verbose_name='ort', blank=True)
   
    
    # For building URLs
    slug = models.SlugField(default='', blank=True)
    
    def __str__(self):
        return self.name
    
    def get_full_adress(self):
        return [self.adress, str(self.postCode) +'   ' + self.location]
    
    class Meta:
        verbose_name = 'boendeanläggning'
        verbose_name_plural = 'boendeanläggningar'
    
class Rooms(models.Model):
    # Title of room
    name = models.CharField(max_length=25, verbose_name='namn')
    number = models.PositiveIntegerField(blank= True)
    
    # Room attributes
    describtion = models.TextField(max_length=255, blank=True, verbose_name='Beskrivning')
    standard = models.CharField(choices=Room_Standard_Choices, max_length=20, verbose_name='standard')
    max_guests = models.PositiveIntegerField(verbose_name='Max antal gäster', default=4)
    
    # Price per room exkl. VAT
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0, 
                                verbose_name="pris exkl. moms",
                                help_text='Pris för rum exkl. moms')
    
    owned_by = models.ForeignKey(
        Facility,
        related_name= 'rooms',
        verbose_name='anläggning',
        null=True
        )
    
    class Meta:
        verbose_name = 'rum'
        verbose_name_plural = 'rum'
        ordering = ['owned_by']

    def __str__(self):
        return '%s, %s' % (self.name, self.owned_by.name)
        

'''
Guest model, inherits from GuestUser (Proxymodel of User) and GuestExtra
(abstract model with extra information that we want about the guests.

GuestUser also has an extended manager that sorts out guests from other users
'''
class GuestManager(models.Manager):
    
    def get_queryset(self):
        return super(GuestManager, self).get_queryset().exclude(
            Q(is_staff=True) | Q(is_superuser=True))
                     
class GuestExtra(models.Model):
    newsletter = models.BooleanField(default = True)
    phone_number = models.CharField(max_length=24)
    bookings = models.ForeignKey(
        'database.Booking',
        null = True,
        blank = True,
        on_delete=models.CASCADE
        )
    
    class Meta:
        abstract = True
        
class GuestUser(User):
    objects = GuestManager()
    
    class Meta:
        proxy = True
        app_label = 'auth'
        
    
class Guest(GuestUser, GuestExtra):
    
    class Meta:
        verbose_name = 'gäst'
        verbose_name_plural = 'gäster'
        
'''
Model and validator for discount code
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
        
class Discount_codes(models.Model):
    code = models.CharField(max_length=15, verbose_name= 'kod')
    value = models.DecimalField(decimal_places=2, max_digits=8)
    guest = models.ForeignKey(
        User,
        limit_choices_to={'is_guests': True},
        verbose_name = 'gäst',
        null = True
        )

'''
Boking models.

Model for booking, manager for booking querysets, helper function for
calculating booking_number, 
'''

def calc_booking_no():
    '''
    Returns a booking number for a new booking based on the date and the
    previous number of bookings the same day.
    '''
    today = datetime.today()
    day_form = '%y%m%d'
    day_part = today.strftime(day_form)
    latest_booking = Booking.objects.latest('booking')
    bookingstr = str(latest_booking.booking)
    last_part = int(bookingstr[-2:])
    booking_no = ''
    if bookingstr[:6] == day_part:
        last_part += 1
        if last_part <= 9:
            last_part = '0' + str(last_part)
        else:
            last_part = str(last_part)
        booking_no = day_part + str(last_part)
        return int(booking_no)
    else:
        booking_no = day_part + '01'
        return int(booking_no)

# Booking models
class Booking(models.Model):
    # Guest
    guest_for_booking = models.ForeignKey(
        Guest,
        related_name='guest',
        on_delete=models.CASCADE,
        verbose_name='gäst',
        )
    
    # Booking specs
    booking = models.PositiveIntegerField(primary_key=True, verbose_name='boknings id', default=calc_booking_no)
    numberOfGuests = models.IntegerField(null= False, default = 2, verbose_name='antal gäster')
    special_requests = models.TextField(max_length = 255, blank= True, verbose_name= 'övrigt')
    
    # Fields for preliminary bookings
    preliminary = models.BooleanField(default= False, verbose_name='preliminär')
    longest_prel = models.DateTimeField(verbose_name='längsta preliminärbokning', null=True,
                                        validators= [validate_preliminary], blank=True)
   
    
    # Dates
    start_date = models.DateField(verbose_name='datum för avresa', null=True, validators=
                                 [])
    end_date = models.DateField(verbose_name='datum för hemresa', null=True, validators=
                               [])
    
    # Potential discount code
    discount_code = models.CharField(blank=True, null=True, max_length=15, verbose_name= 'rabattkod',
                                     validators = [validate_discount_code])
    
    
    # Checked in/Checked out
    checked_in = models.BooleanField(default=False, verbose_name='incheckad (J/N)')
    checked_out = models.BooleanField(default=False, verbose_name='utcheckad(J/N)')
    
    # Economy
    total = models.DecimalField(decimal_places=2, max_digits=8)
    payed = models.BooleanField(default= False, verbose_name='betald')
    
    # When was the booking created
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    
    class Meta:
        verbose_name = 'Bokning'
        verbose_name_plural = 'bokningar'
        ordering = ['-created_at']
         
    def __str__(self):
        return str(self.booking)
    
    def save(self, *args, **kwargs):
        # Calculate total price for booking when saving
        priceList = []
        bikes = BikesBooking.objects.filter(booking=self.booking)
        [priceList.append(bike.subtotal) for bike in bikes]
        rooms = RoomsBooking.objects.filter(booking=self.booking)
        [priceList.append(room.subtotal) for room in rooms]
        lunches = LunchBooking.objects.filter(booking=self.booking)
        [priceList.append(lunch.subtotal) for lunch in lunches]
        
        self.total = listSum(priceList)
        super(Booking, self).save(*args, **kwargs)
        
        # create function that gathers all related bookings and calculates
        # the total price from their subtotals.
class BikesBookingManager(models.Manager):
    
    def BookBikes(self, from_date, to_date):
        pass
     
class BikesBooking(models.Model):
    # Dates and time
    from_date = models.DateTimeField()
    to_date = models.DateTimeField()
    full_days = models.BooleanField(default=True)
    
    # Economy
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Bookings and specs
    bike = models.ForeignKey(Bike,
        related_name='bike',
        null = True,
        on_delete=models.CASCADE,
        blank=True
        )
    booking = models.ForeignKey(
        Booking,
        related_name='booked_bike',
        on_delete=models.CASCADE,
        )
    
    class Meta:
        verbose_name = 'cykelbokning'
        verbose_name_plural = 'cykelbokningar'
            
    def __str__(self):
        return str(self.booking)
    
    def save(self, *args, **kwargs):
        days = self.to_date - self.from_date
        full_day = self.full_days
        price = 200
        self.subtotal = price * (days.days +1)
        super(BikesBooking, self).save(*args, **kwargs)
        
    '''
    TODO:
    # Lägg till __str__ för bike
    # Lägg in sökning för tillgängliga cyklar
    # Överväg att lägga med datum
    # Bygg modell i ekonomi för priser
    '''

class BikeExtraBooking(models.Model):
    # Dates and times
    from_date = models.DateTimeField()
    to_date = models.DurationField(choices=Day_Choices)
    full_day = models.BooleanField(default=True)
    
    # Booking specs
    extra = models.ForeignKey(
        BikeExtra,
        null=True,
        on_delete=models.CASCADE,
        related_name='bike_extra'
        )
    booking = models.ForeignKey(
        Booking,
        null = True,
        on_delete=models.CASCADE,
        related_name='Booking',
        )
    
    def __str_(self):
        return self.extra
    
    def save(self, *args, **kwargs):
        days = self.to_date - self.from_date
        #full_day = self.full_day
        price = 200
        self.subtotal = price * (days.days +1)
        super(BikesBooking, self).save(*args, **kwargs)
        
        
class RoomsBooking(models.Model):
    # Room specs
    numberOfGuests = models.PositiveIntegerField(verbose_name='antal gäster')
    
    # Dates and times
    from_date = models.DateField()
    to_date = models.DateField()
    
    # Economics
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Booking specs
    booking = models.ForeignKey(
        Booking,
        related_name='booked_rooms',
        on_delete=models.CASCADE,
        )
    room = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE
        )
    
    class Meta:
        verbose_name = 'rumsbokning'
        verbose_name_plural = 'rumsbokningar'
    
    def __str__(self):
        return str(self.room)
    
    def save(self, *args, **kwargs):
        nights = self.to_date - self.from_date
        price = self.room.price
        self.subtotal = price * nights.days
        super(RoomsBooking, self).save(*args, **kwargs)
        
class LunchBooking(models.Model):
    # Date
    day = models.DateField()
    
    # Economics
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Booking Specs
    type = models.ForeignKey(
        Lunch,
        on_delete=models.CASCADE,
        blank = True,
        )
    booking = models.ForeignKey(
        Booking,
        related_name='booked_lunches',
        on_delete=models.CASCADE,
        )

    class Meta:
        verbose_name = 'lunchbokning'
        verbose_name_plural = 'lunchbokningar'
        
    def __str__(self):
        return '%s, %s' % (self.quantity, self.type)

    def save(self, *args, **kwargs):
        self.subtotal = self.type.price * self.quantity
        super(LunchBooking, self).save(*args, **kwargs)
        
class PackageBooking(models.Model):
    pass



'''
Models and Managers for availabilies of items to be booked.

Bikes, Rooms, ...
'''
# Availability manager
def perdelta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta
        
def find_index(lst, thing):
    for sublist, bike_no in enumerate(lst):
        try:           
            bike_ind = bike_no.index(thing)
        except ValueError:
            continue
        return sublist, bike_ind
                    
class BikeAvailableManager(models.Manager):
        
    def create_available_bike(self, bike, date):
        available_bike = self.create(bike=bike, available_date=date)
        return available_bike
        
    def get_bikes_for_day(self, day):
        return super(BikeAvailableManager, self).get_queryset().filter(
            Q(available_date=day) & Q(available=True))
        
    def book_bike(self, bike, date, booking):
        bk = self.get(bike=bike, available_date=date)
        bk.update(available=False, bookings=booking)
        
    def unbook_bike(self, bike, date):
        bk = self.get(bike=bike, available_date=date)
        bk.update(available=False, bookings=None)
    

# Abstract model for availability
class Available(models.Model):
    available_date = models.DateField()
    available = models.BooleanField(default=True)
    
    class Meta:
        abstract = True        
        
           
# Availability for bikes
class BikeAvailable(Available):
    bike = models.ForeignKey(
        Bike,
        on_delete=models.PROTECT,
        blank = True
        )
    
    bookings = models.ForeignKey(
        BikesBooking,
        related_name='availableBike',
        on_delete=models.CASCADE,
        blank = True,
        null = True
        )
    
    objects = BikeAvailableManager()  # Extended manager for finding dates
    
    class Meta:
        verbose_name = 'tillgänglighet cykel'
        verbose_name_plural = 'tillgänglighet cyklar'
        index_together = ['bike', 'available_date']
        ordering = ['available_date', 'bike', 'available']
        
    def __str__(self):
        return str(self.bike)

  
# Rooms
# Not needed until we can search external databases
class RoomsAvailable(Available):
    room = models.ForeignKey(
        Rooms,
        on_delete=models.PROTECT,
        null = True
        )
    bookings = models.ForeignKey(
        RoomsBooking,
        related_name= 'available_rooms'
        )

###############################################################################
'''
Event model class for creating events and show in a calendar on the admin index
page. 

TODO:
# Add tasks that could be associated with an event.
# Create autocreation for events, e.g., from cleaning

'''

class Event(models.Model):
    title = models.CharField(max_length=24)
    date_and_time = models.DateTimeField()
    short_description = models.TextField(max_length=100)
    # Add tasks
    
    class Meta:
        verbose_name = 'Händelse'
        verbose_name_plural = 'Händelser'
    
    def __str__(self):
        return self.title

        