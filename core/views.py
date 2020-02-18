from django.shortcuts import render, HttpResponse, redirect
from core.models import Event
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
        raise Http404
    else:
        if event.location == "":
            location = 'not informed.'
        else:
            location = event.location
        return HttpResponse('Event location is: {}'.format(location))

@login_required(login_url='/login/')
def event_list(request):
    user = request.user
    event = Event.objects.filter(user=user)
    # event = Event.objects.all()
    data = {'events': event}
    return render(request, 'schedule.html', data)


# def index(request):
#     return redirect('/schedule/')
