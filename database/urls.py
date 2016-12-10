'''
Created on 16 okt. 2016

@author: Adrian
'''
from django.conf.urls import url
from . import views

app_name = "database"
urlpatterns = [
    # /database/
    url(r'^$', views.index , name="index"),
    # /database/bookingNo/
    url(r'^(?P<booking_id>[0-9]+)/$', views.booking, name='booking'),
    url(r'^test/', views.trial),
    ]