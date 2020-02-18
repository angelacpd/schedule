from django.shortcuts import render, HttpResponse, redirect
from core.models import Event
from django.http.response import Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta


# Create your views here.
def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'User or password invalid.')
    # else:
    #     return redirect('/')
    return redirect('/')


@login_required(login_url='/login/')
def return_location(request, event_title):
    try:
        event = Event.objects.get(title=event_title)
    except:
        raise Http404()
    else:
        if event.location == "":
            location = 'not informed.'
        else:
            location = event.location
        return HttpResponse('Event location is: {}'.format(location))


@login_required(login_url='/login/')
def event_list(request):
    user = request.user
    current_date = datetime.now() - timedelta(hours=1)
    event = Event.objects.filter(user=user, #)  #,
                                 event_date__gt=current_date)  # suffix __gt = greater than, suffix __lt = less than
    # event = Event.objects.all()
    data = {'events': event}
    return render(request, 'schedule.html', data)


@login_required(login_url='/login/')
def event(request):
    id_event = request.GET.get('id')
    data = {}
    if id_event:  # If there id_event exists
        data['event'] = Event.objects.get(id=id_event)
    return render(request, 'event.html', data)


@login_required(login_url='/login/')
def submit_event(request):
    if request.POST:
        user = request.user
        title = request.POST.get('title')
        event_date = request.POST.get('event_date')
        description = request.POST.get('description')
        location = request.POST.get('location')
        event_id = request.POST.get('event_id')
        if event_id:
            event = Event.objects.get(id=event_id)
            if event.user == user:
                event.title = title
                event.event_date = event_date
                event.description = description
                event.location = location
                event.save()
            # Event.objects.filter(id=event_id).update(title=title,
            #                                          event_date=event_date,
            #                                          description=description,
            #                                          location=location)
        else:
            Event.objects.create(user=user,
                                 title=title,
                                 event_date=event_date,
                                 description=description,
                                 location=location)
    return redirect('/')


@login_required(login_url='/login/')
def delete_event(request, id_event):
    user = request.user
    try:
        event = Event.objects.get(id=id_event)
    except:
        raise Http404()
    if user == event.user:
        event.delete()
    else:
        raise Http404()
    return redirect('/')


@login_required(login_url='/login/')
def json_event_list(request):
    user = request.user
    event = Event.objects.filter(user=user).values('id', 'title')
    return JsonResponse(list(event), safe=False)  # safe is necessary if the argument is a list, not needed for dict.


# def index(request):
#     return redirect('/schedule/')
