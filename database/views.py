from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.
from .models import Booking

def index(request):
    latest_booking_list = Booking.objects.order_by('-BookingDate')[:5]
    output = ', '.join([q.guest for q in latest_booking_list])
    return HttpResponse(output)

def booking(request, booking_id):
    response = "You're looking at booking %s."
    return HttpResponse(response % booking_id)