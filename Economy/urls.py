'''
Created on 12 nov. 2016

@author: Adrian
'''
from django.conf.urls import url

from . import views


app_name = "Economy"
urlpatterns = [
    url(r'^cashflow/', views.CashierView, name='cashflow'),
    url(r'^worked/', views.manage_hours_worked),
    url(r'^results/', views.ResultsView, name='results'),
    ]