'''
Created on 16 okt. 2016

@author: Adrian
'''
# Create landing view
from django.http.response import HttpResponse

def LandingView(request):
    return HttpResponse(request)