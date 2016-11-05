'''
Created on 31 okt. 2016

@author: Adrian
'''
from django.conf.urls import url

from . import views

app_name = 'cleaning'
urlpatterns = [
    # ex: /cleaning/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<cleanday_id>[0-9]+)/$', views.detail, name = 'detail'),
    url(r'^(?P<cleanday_id>[0-9]+)/results/$', views.results, name = 'results'),
    url(r'^(?P<cleanday_id>[0-9]+)/numberTimes/$', views.numberTimes, name = 'cleanings'),
    ]