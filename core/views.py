from django.shortcuts import render, HttpResponse
from core.models import Event
from django.http import Http404


# Create your views here.
def return_location(request, event_title):
    try:
        event = Event.objects.get(title=event_title)
    except:
        raise Http404
    else:
        if event.location == "":
            location = 'not informed.'
        else:
            location = event.location
        return HttpResponse('Event location is: {}'.format(location))
