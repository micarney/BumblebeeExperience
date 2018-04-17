# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import date, datetime


class beltManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = 'Name must be more than 3 characters'
        if len(postData['username']) < 3:
            errors['username'] = 'Username must be more than 3 characters.'  
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least eight characters.'  
        if postData['confirmed_password'] != postData['password']:
            errors['confirmed_password'] = 'Passwords must match'
        
        return errors

    def login(self,postData):
        
        user = User.objects.filter(username = postData['username'])
        errors = {}
        if not user:
            errors['username'] = 'Username not valid.' 
        if user and not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['password'] = 'Incorrect password.'
        return errors

class User(models.Model):
    name = models.CharField(max_length = 255, blank=False)
    username = models.CharField(max_length = 255, blank=False)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = beltManager()

class Trip(models.Model):
    start_month_day_year = models.DateField(blank=True, null=True) #blank=True, null=True,'%m/%d/%Y'
    end_month_day_year = models.DateField(blank=True, null=True)
    trip_name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='trip_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    trip_planned = models.ManyToManyField(User, related_name="trip_joined")
    objects = beltManager() 
    
