from cleaning.models import CleanDay, CleanTask
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


# Create your views here.
def index(request):
    latest_cleanday_list = CleanDay.objects.order_by('-day')[:5]
    context = {
        'latest_cleanday_list':latest_cleanday_list,
        }
    return render(request, 'cleaning/index.html', context)

def detail(request, cleanday_id):
    cleaning = get_object_or_404(CleanDay, pk=cleanday_id)
    return render(request, 'cleaning/detail.html', {'cleaning': cleaning})

def results(request, cleanday_id):
    response = "You´re looking at the results of cleaning day %s."
    return HttpResponse(response % cleanday_id)

def numberTimes(request, cleanday_id):
    cleanday = get_object_or_404(CleanDay, pk=cleanday_id)
    try:
        selected_cleanday = cleanday.cleantask_set.get(pk=request.POST['cleantask'])
    except (KeyError, CleanTask.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'cleaning/detail.html', {
            'cleanday': cleanday,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_cleanday.numberTimes += 1
        selected_cleanday.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('cleaning:results', args=(cleanday.id,)))