
from .views import *
from django.urls import path
urlpatterns = [
    path('person',personDetails),
    path('getAllPersons',getAllPersons),
    path('city',cityDetails),
    path('getAllCities',getAllCities),
    path('connectPaC',connectPaC),
    path('connectPaP',connectPaP)
]
