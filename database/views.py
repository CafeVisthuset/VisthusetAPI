from django.shortcuts import render
from django.http.response import HttpResponse
from .models import BikeAvailable

# Create your views here.
from .models import Booking
from datetime import timedelta

def index(request):
    latest_booking_list = Booking.objects.order_by('-BookingDate')[:5]
    output = ', '.join([q.guest for q in latest_booking_list])
    return HttpResponse(output)

def booking(request, booking_id):
    response = "You're looking at booking %s."
    return HttpResponse(response % booking_id)

def perdelta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta
        
def trial(request):
    bike_list = BikeAvailable.objects.get_available_bike()  
    output = ', '.join([str(list) for list in bike_list])
    return HttpResponse(output)