
from .views import *
from django.urls import path
urlpatterns = [
     path('spectacle',getFirstConcepts),
     path('conceptSubClass',getConceptSubClasses),
     path('spec',createSpectale),
     path('annotation',createAnnotation),
    path('concept',createInstance)

     # path('getAllPersons',getAllPersons),
     # path('city',cityDetails),
     # path('getAllCities',getAllCities),
     # path('connectPaC',connectPaC),
     # path('connectPaP',connectPaP)
 ]
