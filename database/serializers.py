'''
Created on 25 dec. 2016

@author: Adrian

TODO:
# Write update and delete functions for all serializers

'''
from rest_framework import serializers
from database.models import Booking, BikesBooking, Guest, Discount_codes,\
    BikeExtraBooking, BikeExtra
from django.contrib.auth.models import User
from database.choices import Day_Choices
from database.validators import positive_integer
        
class GuestUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=25, required=False)
    phone_number = serializers.CharField(max_length=25, required=False) # temporary debugfield
    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'email', 'phone_number',
                  'newsletter']
        
        def create(self, validated_data):
            try:
                user = Guest.objects.get(username=validated_data['email'])
            except:
                user = None
            
            if not user:
                validated_data['password'] = User.objects.make_random_password()
                validated_data['username'] = validated_data['email']
                return Guest.objects.create(**validated_data)
            else:
                return user

class BikeBookingSerializer(serializers.ModelSerializer):
    number_of_bikes = serializers.DurationField()
    class Meta:
        model = BikesBooking
        fields = ['number_of_bikes']
        
    def create(self, validated_data):
        '''
        Do things to get available dates and update them according to the current booking
        '''
        return BikesBooking.objects.create(full_days=True, **validated_data)
        
class BikeExtraSerializer(serializers.ModelSerializer):

    class Meta:
        model = BikeExtraBooking
        fields = ['extra']

class DiscountSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=24, required=False)
    class Meta:
        model = Discount_codes
        fields = ['code']
        
class BookingBikeSerializer(serializers.ModelSerializer):
    bike = BikeBookingSerializer(many=True, required=True)
    extras = BikeExtraSerializer(many=True, required=False)
    discounts = DiscountSerializer(required=False)
    person = GuestUserSerializer(required=True)
    # lunches = LunchSerializer(many=True, required=False)
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'numberOfGuests', 'person', 'discounts',
                  'bike', 'extras']

class BookingSerializer(serializers.Serializer):
    # Dates and time
    start_date = serializers.DateField(required=True)
    duration = serializers.DurationField(required=True)
    
    # Bikes and extras
    number_adult_bikes = serializers.ChoiceField(
        choices=[(number, '%s' % (number)) for number in range(1,10)])
    number_child_bikes = serializers.ChoiceField(
        choices=[(number, '%s' % (number)) for number in range(1,3)])
    number_extras = serializers.MultipleChoiceField(
        choices=BikeExtra.objects.all())
    
    # Lunches
    number_veg_lunches = serializers.IntegerField(validators=[positive_integer])
    number_meat_lunches = serializers.IntegerField(validators=[positive_integer])
    number_fish_lunches = serializers.IntegerField(validators=[positive_integer])
    
    # Guest info
    first_name = serializers.CharField(max_length=25)
    last_name = serializers.CharField(max_length=25)
    phone_number = serializers.CharField(max_length=25, required=False)
    email = serializers.EmailField()
    newsletter = serializers.BooleanField(
        default=True,
        help_text= 'Vill du ha nyheter och erbjudanden från oss?')
    
    # Extra message
    other = serializers.CharField(max_length=200)
    