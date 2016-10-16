from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Welcome to the docs section!")

class IndexView(generic.TemplateView):
    template_name = 'docs/Index.html'
    
class LandingView(generic.TemplateView):
    template_name = 'landing.html'
    