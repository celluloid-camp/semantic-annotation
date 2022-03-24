
from .views import *
from django.urls import path
urlpatterns = [
     path('concept',getFirstConcepts),
     path('conceptSubClass',getConceptSubClasses),
     path('spec',createSpectale),
     path('annotation',createAnnotation),
     # # path('annotation',getAnnotationOfSpectcale),
     # path('concept',createInstance),
     # path('relation',createRelation)

     # path('getAllPersons',getAllPersons),
     # path('city',cityDetails),
     # path('getAllCities',getAllCities),
     # path('connectPaC',connectPaC),
     # path('connectPaP',connectPaP)
 ]
