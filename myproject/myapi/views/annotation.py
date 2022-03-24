
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
from .concept import *
import json

from . import Parameters

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
        # typeConcept=json_data['type']
        objet = json_data['objet']
        typeRelation=json_data['relation']
        try:
            insertAnnotationQuery="MATCH (n:owl__Class) WHERE n.uri = 'http://www.semanticweb.org/larbim/ontologies/2022/0/Emotion-initial-version#Annotation' CREATE (s:owl__NamedIndividual{id:apoc.create.uuid(),projectId:'%s', userId:'%s',commentaire:'%s',startTime:'%s', stopTime:'%s', label:'annotation'})-[r:rdf_type]->(n)  RETURN s.id" %(projectId,userId,commentaire,startTime,stopTime)
            query= db.cypher_query(insertAnnotationQuery)[0]
            idAnnotation=query[0][0]
            # Création relation annotation spectacle
            relation="hasAnnotation"
            print("id annotation", idAnnotation)
            idRelation=createRelation(spectacle, relation, idAnnotation)
            print("coco")
            # Création relation annotation concept
            idInstance=createInstance(objet)
            print(idInstance)
            if idInstance !=0:
                AnnotationConcept = createRelation(idAnnotation, typeRelation, idInstance)
                response = {
                    "idAnnotation": idAnnotation,
                    "idRelation": idRelation,
                    " AnnotationConcept": AnnotationConcept
                }
            else:
                response = {"error": "Fail to create annotation"}

            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
   # **************************     # Get annotation of spectacle
    if request.method == 'GET':
            path = Parameters.Params['Ontology_Path']
            # idSpectacle= request.GET.get('idSpectacle')
            D = path + "Annotation"
            try:
                annotations = db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdf_type]->(f:owl__Class) WHERE f.uri='%s' RETURN n.id" % D)[0]
                max=len(annotations)
                responseInstance = ""
                for i in range(max):
                    j = i +1
                    it = str(j)
                    instance = annotations[i][0]
                    responseInstance = responseInstance + "'annotation " + it + "':'" + instance + "',"
                    print(responseInstance)
                    response = "{" + responseInstance + "}"
                # annotation = uri[len(path):len(uri)]
                #     response = {
                #     "annotation": uri
                # }
                return JsonResponse(response, safe=False)
            except:
                response = {"error": "Error occurred"}
                return JsonResponse(response, safe=False)


        # Get All Annotation of a spectacle
# def getAnnotationOfSpectcale(request):
#     if request.method == 'GET':
#         path=Parameters.Params['Ontology_Path']
#         # idSpectacle= request.GET.get('idSpectacle')
#         D=path+"Annotation"
#         try:
#             annotation = db.cypher_query("MATCH(D:owl__Class) WHERE D.uri='%s' return D.uri" %D)
#
#             uri = annotation[0][0][0]
#             annotation = uri[len(path):len(uri)]
#             response = {
#                 "annotation": annotation,
#             }
#             return JsonResponse(response, safe=False)
#         except:
#             response = {"error": "Error occurred"}
#             return JsonResponse(response, safe=False)