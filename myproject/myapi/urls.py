
from .views import *
from django.urls import path
urlpatterns = [
     path('concept',getFirstConcepts), ##GET Annotation branches
     path('conceptSubClass',getConceptSubClasses),  ##GET concept compoenents and relations
     path('spec',createSpectale), ##Create specatcle
     path('annotation',createAnnotation),##Create and Get Annotation
     path('relation',typeOfRelation), ##Return type of relation
     path('ontology',getAnnotationConcept), ##Get concepts of annotation

 ]
