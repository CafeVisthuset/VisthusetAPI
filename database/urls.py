'''
Created on 16 okt. 2016

@author: Adrian
'''
from django.conf.urls import url
from . import views, calendars

app_name = "database"
urlpatterns = [
    # /bookings/
    url(r'^$', views.index , name="index"),
    url(r'^availablebike/$', views.create_available_bikes, name='createbikes'),
    # /bookings/bookingNo/
    url(r'^(?P<booking_id>[0-9]+)/$', views.booking, name='booking'),
    url(r'^thanks/', views.ThanksView, name= 'thanks'),
    url(r'^test/', views.trial),
    url(r'^calendar/$', calendars.calendar, name='eventcalendar'),
    url(r'^bikebooking/', views.BikeBookingFormResponse),
    url(r'^bikebooking/resp', views.BikeBookingResponse),
    ]