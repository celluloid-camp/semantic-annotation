from neomodel import StructuredNode, StringProperty, IntegerProperty,UniqueIdProperty,RelationshipTo
# Create your models here.


# class Person(StructuredNode):
#     uid = UniqueIdProperty()
#     name = StringProperty(unique_index=True)
#     age = IntegerProperty(index=True, default=0)
#
#     friends = RelationshipTo('Person', 'FRIEND')