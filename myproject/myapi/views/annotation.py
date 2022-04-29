

from .concept import *
from .relation import *
import json

from . import Parameters

@csrf_exempt
def createAnnotation(request):
    if request.method =='POST':
        Emotion=False
        Judgement=False
        path = Parameters.Params['Ontology_Path']+"Annotation"
        json_data = json.loads(request.body)
        commentaire = json_data['commentaire']
        projectId=json_data['projectId']
        userId=json_data['userId']
        startTime=json_data['startTime']
        stopTime=json_data['stopTime']
        userName=json_data['userName']
        spectacle = projectId
        objet = json_data['objet']
        idAnnotation=json_data['annotationId']
        # print('id annotation ', idAnnotation)
        typeRelation=json_data['relation']
        if(len(objet)!=0):
            obj=objet[len(objet)-1]
            if("Judgement" in objet):
                judgementIndex= objet.index(("Judgement"))
                if(judgementIndex!=0):
                    # traitement different
                    obj=objet[judgementIndex-1]
                    Judgement=True
                    print("index of judgement", judgementIndex)
            if ("Emotion" in objet):
                EmotionIndex = objet.index(("Emotion"))
                if (EmotionIndex != 0):
                    # traitement different
                    obj = objet[EmotionIndex - 1]
                    Emotion=True
                    print("index of emotion", EmotionIndex)

        print("type de relation", typeRelation, idAnnotation)
        try:
            insertAnnotationQuery="MATCH (n:owl__Class) WHERE n.uri = '%s' CREATE (s:owl__NamedIndividual{id:'%s',projectId:'%s', userId:'%s',commentaire:'%s',startTime:'%s', stopTime:'%s', userName:'%s', label:'annotation'})-[r:rdf_type]->(n)  RETURN s.id" %(path,idAnnotation,projectId,userId,commentaire,startTime,stopTime,userName)
            query= db.cypher_query(insertAnnotationQuery)[0]
            idAnnotation=query[0][0]
            # Création relation annotation spectacle
            relation="hasAnnotation"
            # We got to check if a spectacle exist or not, if its not the case create one
            idRelation=createRelation(spectacle, relation, idAnnotation)
            print('id relation crée',idRelation)
            # Création relation annotation concept
            idInstance=createInstance(obj,'concept')
            if idInstance !=0:
                AnnotationConcept = createRelation(idAnnotation, typeRelation, idInstance)
                print('id annotation-concept',AnnotationConcept)
                if(Judgement==True or Emotion==True):
                    # create jugement or emotion relation:
                    judgementPath=objet[len(objet)-1]
                    idJudgementInstance = createInstance(judgementPath,judgementPath)
                    judgementRelation = getJudgementRelation(objet[0])
                    if(Emotion==True):
                        judgementRelation = getEmotionRelation(objet[0])
                    if(judgementRelation!= None):
                        # get id of the created concept
                        createRelation(idJudgementInstance, judgementRelation, idInstance)

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
   # ************************** # Get annotation of spectacle
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
                    # Pour chaque annotation get la relation au quelle elle est rattachée
                    try:
                         relation=db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdfs_domain]->(f:owl__NamedIndividual) WHERE f.id='%s' AND NOT(n.label='hasAnnotation') RETURN n.id" % (instanceId))[0]
                         relation = relation[0][0]
                         try:
                             concept = db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdfs_range]-(f:owl__NamedIndividual) WHERE f.id='%s' AND n.label='concept' RETURN n.id" % (relation))[0]
                             concept=concept[0][0]
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
        # print('id annotation:', idAnnotation)
        try:
                  resRelation=db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdfs_domain]->(f:owl__NamedIndividual) WHERE f.id='%s' AND NOT(n.label='hasAnnotation') RETURN n.id,n.label" % (idAnnotation))[0]
                  relation = resRelation[0][0]
                  labelRelation=resRelation[0][1]
                  print('label 1',labelRelation)
                  try:
                             concept = db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdfs_range]-(f:owl__NamedIndividual) WHERE f.id='%s' AND n.label='concept' RETURN n.id" % (relation))[0]
                             concept=concept[0][0]
                             print("id du concept;", concept)
                             try:
                                 # Get the name of the concept
                                 conceptName = db.cypher_query("MATCH (n:owl__Class)-[rdf_type]-(f:owl__NamedIndividual) WHERE f.id='%s' RETURN n.uri" % (concept))[0]
                                 conceptName= conceptName[0][0]
                                 conceptName=conceptName[len(path): len(conceptName)]
                                 superClass = conceptName
                                 lis = []
                                 while (superClass != 'Emotion' and superClass != 'Staging' and superClass != 'Acting' and superClass != 'Dramaturgy' and superClass != 'Judgement'  and superClass != 'Spectacle'):
                                     # GET SUPER CLASS
                                     super = getConceptTreeStructur(superClass)
                                     superClass = super[len(path): len(super)]
                                     lis.append(superClass)

                                 response = {"concept": conceptName,
                                             "superConcept": lis,
                                             "relationConcept": ""
                                             }
                                 try:
                                     print('dkhlna')
                                     resQuery = db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdfs_domain]-(f:owl__NamedIndividual) WHERE f.id='%s' and not (n.label='%s') RETURN n" % (concept,labelRelation))[0]
                                     rel = resQuery[0][0]
                                     relString=str(rel)
                                     index= relString.find("'id'")
                                     id=relString[index+7:len(relString)-3]
                                     # get the instance
                                     resQuery = db.cypher_query("MATCH (n:owl__NamedIndividual)-[rdfs_domain]-(f:owl__NamedIndividual) WHERE f.id='%s'RETURN n.label" % (id))[0]
                                     relConcept = resQuery[len(resQuery)-1][0]
                                     response = {"concept": conceptName,
                                                 "superConcept": lis,
                                                 "relationConcept":relConcept
                                                 }
                                 except:
                                     print("No concepts in relation")

                                 return JsonResponse(response, safe=False)
                             except:
                                 try:
                                     conceptName = db.cypher_query("MATCH (n:Resource)-[rdf_type]-(f:owl__NamedIndividual) WHERE f.id='%s' RETURN n.uri" % (concept))[0]
                                     conceptName = conceptName[0][0]
                                     conceptName = conceptName[len(path): len(conceptName)]
                                     superClass=conceptName
                                     lis=[]
                                     while (superClass != 'Emotion' and superClass != 'Staging' and superClass != 'Acting' and superClass != 'Dramaturgy' and superClass != 'Judgement'  and superClass != 'Spectacle'):
                                         # GET SUPER CLASS
                                         super=getConceptTreeStructur(superClass)
                                         superClass=super[len(path) : len(super)]
                                         lis.append(superClass)

                                     response = {"concept":conceptName,
                                                 "superConcept":lis,
                                                 "relationConcept": ""
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


