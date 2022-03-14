
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
import json



@csrf_exempt
def createAnnotation(request):
    if request.method =='POST':
        json_data = json.loads(request.body)
        # id = json_data['id']
        commentaire = json_data['commentaire']
        projectId=json_data['projectId']
        userId=json_data['userId']
        startTime=json_data['startTime']
        stopTime=json_data['stopTime']
        try:
            insertQuery="MATCH (n:owl__Class) WHERE n.uri = 'http://www.semanticweb.org/larbim/ontologies/2022/0/Emotion-initial-version#Annotation' CREATE (s:owl__NamedIndividual{id:apoc.create.uuid(),projectId:'%s', userId:'%s',commentaire:'%s',startTime:'%s', stopTime:'%s'})-[r:rdf_type]->(n)  RETURN s.id" %(projectId,userId,commentaire,startTime,stopTime)
            query= db.cypher_query(insertQuery)[0]
            response = {
                "id":query[0][0]
            }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)