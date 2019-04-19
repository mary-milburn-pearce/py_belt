
from django.shortcuts import render, redirect, HttpResponse
import datetime, random, re, datetime, bcrypt
from django.contrib import messages
from apps.login.models import Person

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

def user_login(session, user_id, fname, lname, email):
    session['user_id']=user_id
    session['first_name']=fname
    session['last_name']=lname
    session['email']=email
    session['logged-in']=True

def user_registered(email_addr):
    try:
        user = Person.objects.get(email=email_addr)
    except:
        return False
    else:
        return user
    
def save_post_data(postData):
    context = { 'fname' : postData['fname'],
                'lname' : postData['lname'],
                'email' : postData['email'] }
    return context

def index(request):
    request.session['logged-in']=False
    return render(request, "login/index.html")

def register(request):
    request.session['logged-in']=False
    errors = Person.objects.basic_validation(request.POST)
    is_valid = True
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        is_valid = False
    else:
        if user_registered(request.POST['email']):
            messages.error(request, "This email address is already registered")
            is_valid=False
        else:
            hashed_pw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
            user = Person.objects.create( \
                    first_name=request.POST['fname'], \
                    last_name=request.POST['lname'], \
                    email=request.POST['email'], \
                    password=hashed_pw)
            if not user:
                messages.error(request, "User could not be added")
                is_valid=False
    if is_valid:
        user_login(request.session, user.id, user.first_name, user.last_name, user.email)
        return redirect(f"/dashboard/{user.id}")
    else:
        context = save_post_data(request.POST)
        return render(request, "login/index.html", context)

def login(request):
    is_valid=True
    request.session['logged-in']=False
    print('In Login')
    if not EMAIL_REGEX.match(request.POST['email']): 
        print('Not REgex')
        messages.error(request, "Invalid email address!")
        is_valid=False
    if len(request.POST['pw'])<1:
        messages.error(request, "Please enter password")
        is_valid=False
    if is_valid:
        print('checking user registered')
        user=user_registered(request.POST['email'])
        if not user:
            messages.error(request, "User not yet registered")
            is_valid=False
        else:
            hashed_pw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
            print('From User record: ', user.password, 'From input: ', hashed_pw)
            if not bcrypt.checkpw(request.POST['pw'].encode(), user.password.encode()):
                messages.error(request, "Invalid login")
                is_valid=False
    if is_valid:
        user_login(request.session, user.id, user.first_name, user.last_name, user.email)
        return redirect(f"/dashboard/{user.id}")
    else:
        return render(request, "login/index.html")

def logout(request):
    request.session.clear()
    request.session['logged-in']=False
    return redirect("/")
