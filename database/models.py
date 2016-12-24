from django.db import models
from Economy.models import Employee
from .choices import *
from .validators import validate_booking_date, validate_preliminary
from datetime import date, timedelta, datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Q
from django.db.models.fields import related
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

'''
Proxy model for guests.
'''
class GuestManager(models.Manager):
    
    def get_queryset(self):
        return super(GuestManager, self).get_queryset().exclude(
            Q(is_staff=True) | Q(is_superuser=True))
                     
class GuestExtra(models.Model):
    newsletter = models.BooleanField(default = True)
    class Meta:
        abstract = True
        
class GuestUser(User):
    objects = GuestManager()
    
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'gäst'
        verbose_name_plural = 'gäster'
    
class Guest(GuestUser, GuestExtra):
    pass
     
# Lunch models
class Lunch(models.Model):
    slug = models.SlugField(default='/')
    type = models.CharField(choices=Lunch_Choices, default='vegetarian', max_length= 15, verbose_name='lunchalternativ')
    price = models.PositiveIntegerField(default = 95, verbose_name='pris')
    #allergens
    
    class Meta:
        verbose_name = 'lunch'
        verbose_name_plural = 'luncher'
        
class Utilities(models.Model):
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
    def get_available_bike(self):
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT  b.bike_id, b.start_date, b.end_date
                FROM database_bike p, database_bikeavailable b
                WHERE p.id = b.bike_id
                ORDER BY b.bike_id
                ''')
            avail_list = []
            for row in cursor.fetchall():
                b = self.model(bike_id=row[0], start_date=row[1], end_date=row[2])
                temp_date_list = [str(d) for d in perdelta(b.start_date, b.end_date, timedelta(days=1))]
                avail_list.append([b.bike_id, temp_date_list])
            
            bike_list = []
            available_dates_list = []
            temp_dates = []
            for item in avail_list:
                bike = item[0]
                    
                if bike in bike_list:
                    temp_dates = item[1]
                    
                    ind = find_index(available_dates_list, bike)
                    
                    for date in temp_dates:
                        if date not in available_dates_list[ind[0]]:
                            available_dates_list[ind[0]].append(date)
                    bike_list.append(bike)
                else:
                    bike_list.append(bike)
                    available_dates_list.append(item)
                          
            return available_dates_list
"""    
    def find_first_avail_date(self):
        with connection.cursor() as cursor:
            cursor.execute('''
            SELECT b.bike_id, b.start_date
            FROM database_bikeavailable b, database_bike p
            WHERE b.bike_id = p.id
            ''')
            
            for row in cursor.fetchall():
                b = self.model(bike_id=row[0], start_date=row[1])
                lowest = b.start_date
                if b.start_date <= lowest:
                    lowest = b.start_date
            return lowest
"""        
# Availability for bikes
class BikeAvailable(models.Model):
    bike = models.ForeignKey(
        Bike,
        on_delete=models.PROTECT,
        null = True,
        )
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    
    objects = BikeAvailableManager()  # Extended manager for finding dates
    
    class Meta:
        verbose_name = 'tillgänglighet cykel'
        verbose_name_plural = 'tillgänglighet cyklar'
        
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

'''
Models for accomodation

Contains model for accomodation facility (Accomodation) and rooms associated with facility (Rooms)
'''       
#Accomodation models
class Accomodation(models.Model):
    slug = models.SlugField(default='/')
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
    owned_by = models.ForeignKey(
        Accomodation,
        related_name= 'rooms',
        verbose_name='anläggning',
        null= True
        )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'rum'
        verbose_name_plural = 'rum'
        ordering = ['owned_by']

class RoomsAvailableManager(models.Manager):
    def get_available_bike(self):
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT  a.room_id, a.start_date, a.end_date.
                FROM database_rooms r, database_roomsavailable a
                WHERE r.id = a.room_id
                ORDER BY a.room_id
                ''')
            avail_list = []
            for row in cursor.fetchall():
                a = self.model(room_id=row[0], start_date=row[1], end_date=row[2])
                temp_date_list = [str(d) for d in perdelta(a.start_date, a.end_date, timedelta(days=1))]
                avail_list.append([a.room_id, temp_date_list])
            
            room_list = []
            available_dates_list = []
            temp_dates = []
            for item in avail_list:
                room = item[0]
                    
                if room in room_list:
                    temp_dates = item[1]
                    
                    ind = find_index(available_dates_list, room)
                    
                    for date in temp_dates:
                        if date not in available_dates_list[ind[0]]:
                            available_dates_list[ind[0]].append(date)
                    room_list.append(room)
                else:
                    room_list.append(room)
                    available_dates_list.append(item)
                          
            return available_dates_list

class RoomsAvailable(models.Model):
    room = models.ForeignKey(
        Rooms,
        on_delete=models.PROTECT,
        null = True
        )
    start_date = models.DateField()
    end_date = models.DateField()
    
    objects = RoomsAvailableManager()

# Booking models
def calc_booking_no():
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
    
class Discount_codes(models.Model):
    code = models.CharField(max_length=15, verbose_name= 'kod')
    guest = models.ForeignKey(
        User,
        limit_choices_to={'is_guests': True},
        verbose_name = 'gäst',
        null = True
        )

class BookingQuerySet(models.QuerySet):
    def accomodation(self):
        return self.filter(type='A')
    
    def bike(self):
        return self.filter(type='B')

class Booking(models.Model):
    type = models.CharField(choices= Booking_choices, max_length= 25, default= 'B',
                            verbose_name='bokningstyp')
    booking = models.PositiveIntegerField(primary_key=True, verbose_name='boknings id', default=calc_booking_no)
    booking_date = models.DateField(default=datetime.today, verbose_name='bokningsdatum', validators=
                                    [])
    preliminary = models.BooleanField(default= False, verbose_name='preliminär')
    longest_prel = models.DateTimeField(verbose_name='längsta preliminärbokning', null=True,
                                        validators= [validate_preliminary], blank=True)
    payed = models.BooleanField(default= False, verbose_name='betald')
    startDate = models.DateField(verbose_name='datum för avresa', null=True, validators=
                                 [])
    endDate = models.DateField(verbose_name='datum för hemresa', null=True, validators=
                               [])
    discount_code = models.CharField(blank=True, null=True, max_length=15, verbose_name= 'rabattkod',
                                     validators = [validate_discount_code])
    numberOfGuests = models.IntegerField(null= False, default = 2, verbose_name='antal gäster')
    checked_in = models.BooleanField(default=False, verbose_name='incheckad (J/N)')
    checked_out = models.BooleanField(default=False, verbose_name='utcheckad(J/N)')
    
    other = models.TextField(max_length = 255, blank= True, verbose_name= 'övrigt')
    guest = models.ForeignKey(
        GuestUser,
        verbose_name='gäst',
        blank=True,
        null= True,
        )
    
    bikes = models.ManyToManyField(
        Bike,
        related_name='bikes',
        verbose_name='cyklar',
        blank=True,
        )
    
    bike_extras = models.ManyToManyField(
        BikeExtra,
        verbose_name= 'cykeltillbehör',
        blank=True,
        )
    accomodation = models.ManyToManyField(
        Accomodation,
        related_name='accomodation',
        verbose_name='boende',
        blank=True,
        )
    utilities = models.ManyToManyField(
        Utilities,
        related_name='utilities',
        verbose_name='tillbehör',
        blank=True
        )
    
    def __str__(self):
        return str(self.booking)
    
    class Meta:
        verbose_name = 'Bokning'
        verbose_name_plural = 'bokningar'
        ordering = ['-booking_date']

class AccomodationBookingManager(models.Manager):
    
    def get_queryset(self):
        return super(AccomodationBookingManager, self).get_queryset().filter(type='A')

    def create(self, *args, **kwargs):
        kwargs.update({'type': 'A'})
        return super(AccomodationBookingManager, self).create(*args, **kwargs)

class AccomodationBooking(Booking):
    objects = AccomodationBookingManager()
    
    class Meta:
        proxy = True
        verbose_name = 'boendebokning'
        verbose_name_plural = 'bokningar boende'
        
    def save(self, *args, **kwargs):
        self.type = 'A'
        super(AccomodationBooking, self).save(*args, **kwargs)
        
class BikeBookingManager(models.Manager):   
    
    def get_queryset(self):
        return super(BikeBookingManager, self).get_queryset().filter(type='B')
    
    def create(self, *args, **kwargs):
        kwargs.update({'type': 'B'})
        return super(BikeBookingManager, self).create(*args, **kwargs)
    
class BikeBooking(Booking):
    ojects = BikeBookingManager()
    class Meta:
        proxy = True
        verbose_name= 'cykelbokning'
        verbose_name_plural= 'cykelbokningar'