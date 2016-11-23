from Economy.forms import CashForm, hoursWorkedForm
from django.http.response import HttpResponse, HttpResponseRedirect
from Economy.models import Dagskassa
from django.shortcuts import render
from django.views.generic.edit import CreateView, FormView
from django.views import generic
from django.urls.base import reverse
from django.forms.formsets import formset_factory


# Create your views here.

"""   
class SuperForm(View):
    casherForm = modelformset_factory(
        Cashier, form=CashForm, formfield_callback=None, formset=BaseModelFormSet,
        extra=0, can_delete=False, can_order=False, max_num=None, fields=None,
        exclude=None, widgets=None, validate_max=False, validate_min=False,
        localized_fields=None, labels=None, help_texts=None, error_messages=None,
        min_num=None, field_classes=None)
    
    def get(self, request):
        return HttpResponseRedirect(request, 'develop/base_form.html', {'FormSet' : casherForm})
"""
def ResultsView(request):
    return render(request, 'economy/results.html')

def CashierView(request):
    if request.method == 'POST':
        form = CashForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('cashflow/results')
    else:
        form = CashForm()
    return render(request, 'economy/base_form.html', {'form': form})

class HoursWorkedView(FormView):
    template_name = 'economy/hours_worked_form.html'
    form_class = hoursWorkedForm
         
    """
    TODO:
    * Create validation routine for this form
        # comment should not be validated
        # All fields cannot be 0
        # The sum of card and cash must agree with sum of sales
    * Make sure no duplicates of the same form can be made.
    * Style the view
    """
    
def manage_hours_worked(request):
    hoursWorkedFormset = formset_factory(hoursWorkedForm) 
    if request.method == 'POST':
        formset = hoursWorkedFormset(request.POST)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = hoursWorkedFormset()
    return render(request, 'economy/hours_worked_form.html', {'formset': formset})