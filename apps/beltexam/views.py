# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt

def index(request):
    for object in User.objects.all():
        context = {
            "name":object.name,
            "username":object.username,
            "password":object.password,
            "created_at":object.created_at,
            "updated_at":object.updated_at,
        }
        
    context = {
        "user_data":User.objects.all(),
    }
    print context
    return render(request, 'beltexam/index.html', context)

def register(request):
    errors = User.objects.validator(request.POST)
    hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')    
    user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashedpw)
    request.session['logged_in'] = user.id
    print user
    return redirect('/traveldash')

def login(request):
    errors = User.objects.login(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    else:
        user= User.objects.get(username=request.POST['username'])
        request.session['logged_in'] = user.id
        return redirect('/traveldash')

def traveldash(request):
    if User.objects.get(id=request.session['logged_in']) == User.objects.last():
        status = "registered!"
    else:
        status = "logged in!"
    context = {
        'user': User.objects.get(id=request.session['logged_in']), 
        'status': status,   
        "trip_data":Trip.objects.all(),
        "trip_planned":User.objects.get(id=request.session['logged_in']).trip_joined.all(),
    }

    return render(request, 'beltexam/traveldash.html', context)

def create(request):
    return render(request, 'beltexam/addtrip.html' )

def additem(request):
    user = User.objects.get(id=request.session['logged_in'])
    trip = Trip.objects.create(trip_name = request.POST['destination'], created_by=user)
    trip.trip_planned.add(user)
    print trip 
    return redirect('/traveldash')

def join(request):
    user = User.objects.get(id=request.session['logged_in'])
    trip = Trip.objects.create(created_by=user)
    trip.trip_planned.add(user)
    return redirect('/traveldash')

def trippage(request, id):
    context = {
        "trip_data":Trip.objects.all(),
    }
    trip = Trip.objects.get(id=id) 
    return render(request,'beltexam/destination.html', context)

def delete(request, id):
    Trip.objects.get(id=id).delete()
    return redirect('/traveldash')

def remove(request, id):
    Trip.objects.get(id=id).remove()
    return redirect('/traveldash')

def logout(request):
    return render(request, 'beltexam/index.html')