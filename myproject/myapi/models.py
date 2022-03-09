from django.db import models

# Create your models here.
from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty, RelationshipTo

class Animal(StructuredNode):
    code=StringProperty(unique_index=True, required=True)
    category= StringProperty(default="domestique")
class Food(StructuredNode):
   name= StringProperty(default="chakhchoukha")
   quantity= IntegerProperty(default=0)