from django.shortcuts import render, redirect, HttpResponse
from apps.login.models import Person
from .models import Event
from django.contrib import messages
import datetime

	
def show_dashboard(request, person_id):
    if not request.session['logged-in']:
        return redirect("/")
    p = Person.objects.get(id=person_id)
    h_events = Event.objects.filter(organizer=p)
    a_events = p.attending_events.all()
    o_events = Event.objects.exclude(organizer=p)
    for a in a_events:
        o_events = o_events.exclude(id=a.id)
    context = { 'this_person' : p,
                'h_events' : h_events,
                'a_events' : a_events,
                'o_events' : o_events }
    return render(request, "belt/dashboard.html", context)

def show_new_event_form(request):
    if request.session['logged-in']:
        return render(request, "belt/add_event.html")
    else:
        return redirect("/")

def add_event(request):
    if not request.session['logged-in']:
        return redirect("/")
    errors = Event.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        context = { 'dest': request.POST['dest'],
                    'start_dt' : request.POST['start_dt'],
                    'end_dt' : request.POST['end_dt'],
                    'plan' : request.POST['plan']
        }
        return render(request, "belt/add_event.html", context)
    host=Person.objects.get(id=request.session['user_id'])
    ev=Event.objects.create(destination=request.POST['dest'],
                start_date=request.POST['start_dt'],
                end_date=request.POST['end_dt'],
                plan=request.POST['plan'],
                organizer=host)
    #req_rel_date = datetime.datetime.strptime(request.POST['ev_date'], '%Y-%m-%d')
    if not ev:
        messages.error(request, "Could not add this trip")
        return render(request, "belt/add_event.html", context)
    else:
        return redirect(f"/dashboard/{request.session['user_id']}")
    
def edit_event(request, event_id):         
    if not request.session['logged-in']:
        return redirect("/")
    this_ev=Event.objects.get(id=event_id)
    context = { 'id' : this_ev.id,
                'dest' : this_ev.destination,
                'start_dt' : this_ev.start_date.strftime('%Y-%m-%d'), 
                'end_dt' : this_ev.end_date.strftime('%Y-%m-%d'),
                'plan' : this_ev.plan
    }
    return render(request, "belt/edit_event.html", context)

# ("/users/<user_id>/update", methods=["POST"]) url(r'^users/(?P<id>\d+)/update$', views.update_show),         
def update_event(request, event_id):       
    if not request.session['logged-in']:
        return redirect("/")
    errors = Event.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        ev=Event()
        ev.destination=request.POST['dest'],
        ev.start_date=request.POST['start_dt'],
        ev.end_date=request.POST['end_dt'],
        ev.plan=request.POST['plan']
        context = { 'this_ev' : ev }
        return render(request, "belt/edit_event.html", context)
    this_ev=Event.objects.get(id=event_id)
    this_ev.destination=request.POST['dest']
    this_ev.start_date=datetime.datetime.strptime(request.POST['start_dt'], '%Y-%m-%d')
    this_ev.end_date=datetime.datetime.strptime(request.POST['end_dt'], '%Y-%m-%d')
    this_ev.plan=request.POST['plan']
    this_ev.save()  
    return redirect(f"/dashboard/{request.session['user_id']}")

# ("/users/<user_id>/destroy") url(r'^users/(?P<id>\d+)/destroy$', views.delete_show),
def delete_event(request, event_id):       
    if not request.session['logged-in']:
        return redirect("/")
    ev=Event.objects.get(id=event_id)
    success=ev.delete()
    return redirect(f"/dashboard/{request.session['user_id']}")

def show_one_event(request, event_id):
    if not request.session['logged-in']:
        return redirect("/")
    ev=Event.objects.get(id=event_id)
    context = { 'event' : ev,
                'host' : ev.organizer,
                'coming' : ev.attendees.all()}
    return render(request, "belt/show_event.html", context)

def join_event(request, event_id):
    if not request.session['logged-in']:
        return redirect("/")
    p=Person.objects.get(id=request.session['user_id'])
    ev=Event.objects.get(id=event_id)
    ev.attendees.add(p)
    return redirect(f"/dashboard/{request.session['user_id']}")

def unjoin_event(request, event_id):
    if not request.session['logged-in']:
        return redirect("/")
    p=Person.objects.get(id=request.session['user_id'])
    ev=Event.objects.get(id=event_id)
    ev.attendees.remove(p)
    return redirect(f"/dashboard/{request.session['user_id']}")
