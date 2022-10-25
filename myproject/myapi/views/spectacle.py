
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db

import json
from numpy import *

from . import Parameters
from .concept import *


@csrf_exempt
######## ***************GET main concepts******************
def getFirstConcepts(request):
    if request.method == 'GET':
        try:
            resultStaging='Staging'
            resultEmotion='Emotion'
            resultActing='Acting'
            resultJudgement='Judgement'
            resultDramaturgy = 'Dramaturgy'
            annotationLibre='Annotation Libre'

            response = {
                "concept": [resultEmotion,resultStaging,
                 resultActing,resultDramaturgy,resultJudgement, annotationLibre ]
            }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

######## ***************GET Subclasses of a Concept and Instances******************
def getConceptSubClasses(request):
    path = Parameters.Params['Ontology_Path']
    luminaryList= Parameters.Params['luminaryList']
    suitList= Parameters.Params['suitList']
    c = request.GET.get('concept')

    if request.method == 'GET':
        uri = path+c
        try:
            Conceptquery="MATCH (n:owl__Class)-[rdfs_subClassOf]->(f:owl__Class) WHERE f.uri='%s' RETURN n.uri" %uri
            result = db.cypher_query(Conceptquery)[0]
            if(len(result)!=0):
                iteration = len(result)
                resUri=result[iteration-1][0]
                res=resUri[len(path):len(resUri)]
                 # check if concept is Emotion or Judgement or subClass of it: boolen case= EmotionOrJudgement(c) , return true is its the case, else :false
                case=emotionOrJudgement(c)
                if(case==True):
                    lis = []
                else:
                    lis = ["Judgement", "Emotion"]
                lis.append(res)
                # check if concept is Staging to append staging types
                if(isStaging(c)):
                    lis.append("StagingTypes")
                if (c in luminaryList): lis.append("Color")
                if (c in suitList): lis.append("Color")
                for i in range(iteration-1):
                    resUri = result[i][0]
                    res = resUri[len(path):len(resUri)]
                    lis.append(res)
                resp = { "concept":lis}
                return JsonResponse(resp, safe=False)

            else:
                uri=path+c
                #-------------------------------------------------------- Get Individuals
                Instancequery = "MATCH (n:owl__NamedIndividual)-[rdf_type]->(f:owl__Class) WHERE f.uri='%s' RETURN n.uri" % uri
                Instanceresult = db.cypher_query(Instancequery)[0]
                case = emotionOrJudgement(c)
                if (case == True):
                    lis = []
                else:
                    lis = ["Judgement", "Emotion"]
                if (isStaging(c)):
                    lis.append("StagingTypes")
                if(c in luminaryList): lis.append("Color")
                if (len(Instanceresult) != 0 and  Instanceresult[0][0]!= None ):
                    instance = Instanceresult[0][0]
                    if(instance!=None):
                        endString = len(instance)
                        max = len(Instanceresult)

                        lis.append(instance[len(path):endString])
                        for i in range(max - 1):
                            j = i + 1
                            it = str(j)
                            instances = Instanceresult[j][0]
                            endString = len(instances)
                            resultInstance = instances[len(path):endString]
                            lis.append(resultInstance)
                    response = {"concept":lis}
                    return JsonResponse(response, safe=False)

                else:
                    j = 0
                    while (j < len(Instanceresult)):
                        res = Instanceresult[j]
                        if (res[0] != None):
                            endString = len(res[0])
                            resultInstance = res[0][len(path):endString]
                            lis.append( resultInstance)
                        j = j + 1
                    response = {"concept":lis}
                    return JsonResponse(response, safe=False)



        #--------------------------Get Relationship-------------------------------

        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
    # Create a new spectacle
@csrf_exempt
def createSpectale(request):
    if request.method =='POST':
        json_data = json.loads(request.body)
        id = json_data['id']
        title = json_data['title']
        try:
            insertQuery="MATCH(n:owl__Class)WHERE n.uri = 'http://www.semanticweb.org/larbim/ontologies/2022/0/Emotion-initial-version#Spectacle' CREATE (s:owl__NamedIndividual{title:'%s',id:'%s'})-[r:rdf_type]->(n) RETURN s.title" %(title,id)
            query= db.cypher_query(insertQuery)[0]
            response = {
                "title":query[0][0]
            }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
