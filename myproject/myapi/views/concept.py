
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
import json
from . import Parameters


@csrf_exempt
def createInstance(request):
    if request.method =='POST':
        json_data = json.loads(request.body)
        type = json_data['type']
        id=json_data['id']
        objet=json_data['objet']
        path = Parameters.Params['Ontology_Path']
        uri= path+ objet
        if(type=="instance"):
            try:
                insertQuery = "MATCH (n:owl__NamedIndividual) WHERE n.uri = '%s'CREATE (s:owl__NamedIndividual{id:'%s'})-[r:rdf_type]->(n) RETURN s.id" % (uri,id)
                query = db.cypher_query(insertQuery)[0]
                response = {
                    "id": query[0][0]
                }
                return JsonResponse(response, safe=False)
            except:
                response = {"error": "Error occurred"}
                return JsonResponse(response, safe=False)
        else:
            if(type=="classe"):
                try:
                    insertQuery = "MATCH (n:owl__Class) WHERE n.uri = '%s' CREATE (s:owl__NamedIndividual{id:'%s'})-[r:rdf_type]->(n) RETURN s.id" % (uri,id)
                    query = db.cypher_query(insertQuery)[0]
                    response = {
                        "id": query[0][0]
                    }
                    return JsonResponse(response, safe=False)
                except:
                    response = {"error": "Error occurred"}
                    return JsonResponse(response, safe=False)
            else:
                response = {"error": "Object type not specified"}
                return JsonResponse(response, safe=False)

