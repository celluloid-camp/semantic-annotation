
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
from .concept import *
import json

from . import Parameters

@csrf_exempt
def createAnnotation(request):
    if request.method =='POST':
        path = Parameters.Params['Ontology_Path']+"Annotation"
        json_data = json.loads(request.body)
        commentaire = json_data['commentaire']
        projectId=json_data['projectId']
        userId=json_data['userId']
        startTime=json_data['startTime']
        stopTime=json_data['stopTime']
        userName=json_data['userName']
        # spectacle = json_data['idSpectacle']
        spectacle = projectId
        # typeConcept=json_data['type']
        objet = json_data['objet']
        idAnnotation=json_data['annotationId']
        print('id annotation ', idAnnotation)
        typeRelation=json_data['relation']
        print("type de relation", typeRelation)
        try:
            insertAnnotationQuery="MATCH (n:owl__Class) WHERE n.uri = '%s' CREATE (s:owl__NamedIndividual{id:'%s',projectId:'%s', userId:'%s',commentaire:'%s',startTime:'%s', stopTime:'%s', userName:'%s', label:'annotation'})-[r:rdf_type]->(n)  RETURN s.id" %(path,idAnnotation,projectId,userId,commentaire,startTime,stopTime,userName)
            query= db.cypher_query(insertAnnotationQuery)[0]
            idAnnotation=query[0][0]
            # Création relation annotation spectacle
            relation="hasAnnotation"
            idRelation=createRelation(spectacle, relation, idAnnotation)
            # Création relation annotation concept
            idInstance=createInstance(objet)
            if idInstance !=0:
                AnnotationConcept = createRelation(idAnnotation, typeRelation, idInstance)
                response = {
                    "idAnnotation": idAnnotation,
                    "idRelation": idRelation,
                    "AnnotationConcept": AnnotationConcept
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
            idProject= request.GET.get('idProject')
            D = path + "Annotation"
            try:
                annotations = db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdf_type]->(f:owl__Class) WHERE f.uri='%s' AND n.projectId='%s' RETURN n.id, n.commentaire" % (D,idProject))[0]
                max=len(annotations)
                lis = []
                for i in range(max):
                    instanceId = annotations[i][0]
                    commentaire= annotations[i][1]
                    # Pour chaque annotation get la relation auquelle elle est rattachée
                    try:
                         relation=db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdfs_domain]->(f:owl__NamedIndividual) WHERE f.id='%s' AND NOT(n.label='hasAnnotation') RETURN n.id" % (instanceId))[0]
                         relation = relation[0][0]
                         # data = {"id": instanceId, "commentaire": commentaire, "idRelation": relation}
                         # lis.append(data)
                         # Get concept
                         try:
                             concept = db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdfs_range]-(f:owl__NamedIndividual) WHERE f.id='%s' AND n.label='concept' RETURN n.id" % (relation))[0]
                             concept=concept[0][0]
                             # data = {"id":instanceId, "commentaire": commentaire, "idRelation": relation,"idConcept": concept}
                             # lis.append(data)
                             try:
                                 # Get the name of the concept
                                 conceptName = db.cypher_query("MATCH (n:owl__Class)-[rdf_type]-(f:owl__NamedIndividual) WHERE f.id='%s' RETURN n.uri" % (concept))[0]
                                 conceptName= conceptName[0][0]
                                 conceptName=conceptName[len(path): len(conceptName)]
                                 data = {"id": instanceId, "commentaire": commentaire,"concept":conceptName}
                                 lis.append(data)
                             except:
                                 #Its an instance
                                 try:
                                     conceptName = db.cypher_query("MATCH (n:Resource)-[rdf_type]-(f:owl__NamedIndividual) WHERE f.id='%s' RETURN n.uri" % (concept))[0]
                                     conceptName = conceptName[0][0]
                                     conceptName = conceptName[len(path): len(conceptName)]
                                     data = {"id": instanceId, "commentaire": commentaire,"concept": conceptName}
                                     lis.append(data)
                                 except:
                                     print("ERROR GET Instance of Annotation")

                         except:
                             data = {"id": instanceId, "commentaire": commentaire,"concept":""}
                             lis.append(data)
                    except:
                        # Annotation sans relation | elle doit etre un commentaire libre
                        data = {"id": instanceId, "commentaire": commentaire,"concept":""}
                        lis.append(data)
                response = {"annotation": lis}
                return JsonResponse(response, safe=False)
            except:
                response = {"error": "Error When Get Annotations of project"}
                return JsonResponse(response, safe=False)

@csrf_exempt
def getAnnotationConcept(request):
    path = Parameters.Params['Ontology_Path']
    if request.method == 'GET':
        idAnnotation= request.GET.get('idAnnotation')
        try:
                  relation=db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdfs_domain]->(f:owl__NamedIndividual) WHERE f.id='%s' AND NOT(n.label='hasAnnotation') RETURN n.id" % (idAnnotation))[0]
                  relation = relation[0][0]
                  try:
                             concept = db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdfs_range]-(f:owl__NamedIndividual) WHERE f.id='%s' AND n.label='concept' RETURN n.id" % (relation))[0]
                             concept=concept[0][0]
                             try:
                                 # Get the name of the concept
                                 conceptName = db.cypher_query("MATCH (n:owl__Class)-[rdf_type]-(f:owl__NamedIndividual) WHERE f.id='%s' RETURN n.uri" % (concept))[0]
                                 conceptName= conceptName[0][0]
                                 conceptName=conceptName[len(path): len(conceptName)]
                                 superClass = conceptName
                                 lis = []
                                 while (superClass != 'Emotion' and superClass != 'Decor' and superClass != 'Interpretation'):
                                     # GET SUPER CLASS
                                     super = getConceptTreeStructur(superClass)
                                     superClass = super[len(path): len(super)]
                                     print('tupe classe :', superClass)

                                     lis.append(superClass)

                                 response = {"concept": conceptName,
                                             "superConcept": lis
                                             }
                                 return JsonResponse(response, safe=False)
                             except:
                                 #Its an instance
                                 try:
                                     conceptName = db.cypher_query("MATCH (n:Resource)-[rdf_type]-(f:owl__NamedIndividual) WHERE f.id='%s' RETURN n.uri" % (concept))[0]
                                     conceptName = conceptName[0][0]
                                     conceptName = conceptName[len(path): len(conceptName)]
                                     superClass=conceptName
                                     lis=[]
                                     while (superClass != 'Emotion' and superClass != 'Decor' and superClass != 'Interpretation'):
                                         # GET SUPER CLASS
                                         super=getConceptTreeStructur(superClass)
                                         superClass=super[len(path) : len(super)]
                                         print('la super classe',superClass)

                                         lis.append(superClass)

                                     response = {"concept":conceptName,
                                                 "superConcept":lis
                                                 }
                                     return JsonResponse(response, safe=False)
                                 except:
                                     print("ERROR GET Instance of Annotation")

                  except:
                            response = {"concept":conceptName}
                            return JsonResponse(response, safe=False)
        except:
                 response = {"concept": ""}
                 return JsonResponse(response, safe=False)


