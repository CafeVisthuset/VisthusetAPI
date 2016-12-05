from Economy.forms import CashForm, WorkHoursForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from Economy.models import WorkingHours, Employee
from django.views.generic.edit import CreateView
from django.forms.models import modelformset_factory
from django.views.generic.detail import DetailView
from datetime import datetime

"""
    TODO:
    * Create validation routine for this form
        # comment should not be validated
        # All fields cannot be 0
        # The sum of card and cash must agree with sum of sales
    * Make sure no duplicates of the same form can be made.
    * Style the view
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

class genCashierView(CreateView):
    form = CashForm
    context_object_name = 'CashCount'
    class Meta:
        verbose_name = ''
        
# Formset for calculating hours worked by staff
class ManageWorkHours(DetailView):
    queryset = WorkingHours.objects.all()[:5]
    class Meta:
        verbose_name = ''
        
data = {
    'form-TOTAL_FORMS': '5',
    'form-INITIAL_FORMS': '0',
    'form-MAX_NUM_FORMS': '10',
}
def working_hours(self, date, starttime, endtime):
    starting = datetime.combine(date, starttime)
    ending = datetime.combine(date, endtime)
    hours = ending - starting
    return hours
    
def manage_hours_worked(request):
    hoursWorkedFormset = modelformset_factory(WorkingHours, form=WorkHoursForm, fields = (
        'employee', 'date', 'startTime', 'endTime'), validate_min=1)
    if request.method == 'POST':                   
        formset = hoursWorkedFormset(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()               
            return HttpResponse('Du har nu lagt in arbetstimmarna')
    else: 
        formset = hoursWorkedFormset(data)  
    return render(request, 'economy/hours_worked_form.html', {'formset': formset})
