from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Booking, Bike
from .forms import CreateAvailableBikeForm
from datetime import datetime, timedelta, date
from django.forms.formsets import formset_factory
from database.forms import BaseCreateAvailableBikeFormset, BookingForm
from django.contrib.admin.views.decorators import staff_member_required
from database.models import BikeAvailable
from django.utils.safestring import mark_safe
from database.calendars import BikeCalendar
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from database.serializers import BookingSerializer
from rest_framework import status

def index(request):
    latest_booking_list = Booking.objects.order_by('-BookingDate')[:5]
    output = ', '.join([q.guest for q in latest_booking_list])
    return HttpResponse(output)

def ThanksView(request):
    return HttpResponse('Tack för din bokning!')

def booking(request, booking):
    response = "You're looking at booking %s."
    return HttpResponse(response % booking)
  
def perdelta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta
    
def trial(request):
    today = datetime.today()
    
    output = today.strftime(format)
    return HttpResponse(output)

@staff_member_required
def create_available_bikes(request):
    # Formset for creating bikes
    CreateAvailableBikeFormset = formset_factory(CreateAvailableBikeForm,
                                                 formset=BaseCreateAvailableBikeFormset,
                                                 extra=len(Bike.objects.all()),
                                                 max_num=25,
                                                 )
    if request.method == 'POST':
        formset = CreateAvailableBikeFormset(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                data = form.cleaned_data
                if data['bike'] is not None:
                    start = data['from_date']
                    numdays = data['to_date'].day - start.day
                    date_list = [(start + timedelta(days=x)) for x in range(0,numdays + 1)]
                
                    # Create available bike
                    if data['action'] == 'create':
                        for day in date_list:
                            # See if object is already created
                            try:
                                BikeAvailable.objects.get(
                                    bike = data['bike'],
                                    available_date = day)
                            # Create a new object if try fails    
                            except:
                                BikeAvailable.objects.create_available_bike(
                                    bike=data['bike'],
                                    date=day)
                
                    # Delete available bike
                    elif data['action'] == 'delete':
                        bk = BikeAvailable.objects.filter(
                                bike = data['bike'],
                                available_date__gte = start).filter(
                                    bike = data['bike'],
                                available_date__lte = data['to_date'])
                        bk.delete()

                        
                        
    else:
        formset = CreateAvailableBikeFormset()
        
    # Calendar
    today = datetime.now()
    my_bikes = BikeAvailable.objects.all().order_by('available_date')
    calendar = BikeCalendar(my_bikes).formatmonth(today.year, today.month)
    '''
    TODO:
    # Make sure no two same available bikes can be created. For instance via unique together
    # create calendar for bikes
    '''
    
    return render(request, 'bookings/create_available_bikes.html',
                  {'formset': formset,
                   'calendar': mark_safe(calendar),
                   })

def BikeBookingFormResponse(request):
    
    if request.method == 'GET':
        initial = {
            'start_date': date.today(),
            'duration': timedelta(days=1),
            'number_adult_bikes': 2,
            'number_child_bikes': 0,
            'number_extras': 0,
            'number_veg_lunches': 0,
            'number_meat_lunches': 0,
            'number_fish_lunches': 0,
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'email': '',
            'newsletter': True,
            'other': '',
            }
        form = BookingForm
        return render(request, 'bookings/bike_booking_form.html', {'form': form})
    
    if request.method == 'POST':
        return HttpResponse(request.path)

#@api_view(['POST'])
def BikeBookingResponse(request):
    '''
    View with responses for Bike Booking
    
    More docs...
    '''
    print(request)
    print(request.method)
    if request.method == 'POST':
        print(request)
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)