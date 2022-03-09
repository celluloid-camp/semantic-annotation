from django.http import JsonResponse
from ..models import *
from django.views.decorators.csrf import csrf_exempt
import json
from neomodel import db

def getAllPersons(request):
    if request.method == 'GET':
        try:
            persons = Person.nodes.all()
            response = []
            for person in persons :
                obj = {
                    "uid": person.uid,
                    "name": person.name,
                    "age": person.age,
                }
                response.append(obj)
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
@csrf_exempt
def personDetails(request):
    if request.method == 'GET':
        # get one person by name
        name = request.GET.get('name', ' ')
        try:
            person = Person.nodes.get(name=name)
            response = {
                "uid": person.uid,
                "name": person.name,
                "age": person.age,
            }
            return JsonResponse(response, safe=False)
        except :
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

    if request.method == 'POST':
        # create one person


        json_data = json.loads(request.body)
        name = json_data['name']
        age = int(json_data['age'])
        print(name)

        try:
            insert_query= "CREATE (friend:Person {name:'%s', age:%d}) RETURN friend" % (name,age)
            db.cypher_query(insert_query)
            response = {"message": "Person succesufuly created!"}
            return JsonResponse(response)
        except:
            response = {"error": "coucou"}
            return JsonResponse(response, safe=False)

    if request.method == 'PUT':
        # update one person
        json_data = json.loads(request.body)
        name = json_data['name']
        age = int(json_data['age'])
        uid = json_data['uid']
        print(uid,name,age)
        try:   
            person = Person.nodes.get(uid=uid)
            person.name = name
            person.age = age
            person.save()
            response = {
                "uid": person.uid,
                "name": person.name,
                "age": person.age,
            }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

    if request.method == 'DELETE':
        # delete one person
        json_data = json.loads(request.body)
        uid = json_data['uid']
        name= json_data['name']
        print(uid)
        try:
            delete_query = "MATCH (n:Person {name: '%s'}) DELETE n" % name
            db.cypher_query(delete_query)
            response = {"message": "Person succesufuly deleted!"}
            return JsonResponse(response)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)