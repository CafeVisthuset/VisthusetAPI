from django.shortcuts import render
from django.views import generic
from django.http.response import HttpResponse

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'index.html'
