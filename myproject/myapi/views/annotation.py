
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
from .concept import *
import json



@csrf_exempt
def createAnnotation(request):
    if request.method =='POST':
        json_data = json.loads(request.body)
        commentaire = json_data['commentaire']
        projectId=json_data['projectId']
        userId=json_data['userId']
        startTime=json_data['startTime']
        stopTime=json_data['stopTime']
        spectacle = json_data['idSpectacle']
        typeConcept=json_data['type']
        objet = json_data['objet']
        typeRelation=json_data['relation']
        try:
            insertAnnotationQuery="MATCH (n:owl__Class) WHERE n.uri = 'http://www.semanticweb.org/larbim/ontologies/2022/0/Emotion-initial-version#Annotation' CREATE (s:owl__NamedIndividual{id:apoc.create.uuid(),projectId:'%s', userId:'%s',commentaire:'%s',startTime:'%s', stopTime:'%s', label:'annotation'})-[r:rdf_type]->(n)  RETURN s.id" %(projectId,userId,commentaire,startTime,stopTime)
            query= db.cypher_query(insertAnnotationQuery)[0]
            idAnnotation=query[0][0]
            # Création relation annotation spectacle
            relation="hasAnnotation"
            idRelation=createRelation(spectacle, relation, idAnnotation)
            response = {
                    "idAnnotation": idAnnotation,
                    "idRelation": idRelation
            }
            # Création relation annotation concept
            idInstance=createInstance(typeConcept, objet)
            print(idInstance)
            AnnotationConcept=createRelation(idAnnotation, typeRelation, idInstance)

            response = {
                "idAnnotation": idAnnotation,
                "idRelation": idRelation,
                " AnnotationConcept": AnnotationConcept
            }

            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)