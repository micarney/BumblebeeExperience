from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^traveldash$', views.traveldash),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^additem$', views.additem),
    url(r'^beltexam/(?P<id>\d+)/delete$', views.delete),
    url(r'^beltexam/(?P<id>\d+)/trippage$', views.trippage),
    url(r'^logout$', views.logout),
    url(r'^beltexam/(?P<id>\d+)/remove$', views.remove),
    url(r'^join$', views.join),

]