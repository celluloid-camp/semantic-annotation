import numpy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
import json
from numpy import *

from . import Parameters


@csrf_exempt
######## ***************GET main concepts******************
def getFirstConcepts(request):
    if request.method == 'GET':
        path=Parameters.Params['Ontology_Path']
        D=path+'Decor'
        E=path+'Emotion'
        J=path+'Judgement'
        I=path+'Interpretation'
        try:
            decor = db.cypher_query("MATCH(D:owl__Class) WHERE D.uri='%s' return D.uri" %D)
            emotion = db.cypher_query("MATCH(D:owl__Class) WHERE D.uri='%s' return D.uri" %E)
            interpretation = db.cypher_query("MATCH(D:owl__Class) WHERE D.uri='%s' return D.uri" %I)
            emotionuri=emotion[0][0][0]
            resultemotion = emotionuri[len(path):len(emotionuri)]
            interpretationuri = interpretation[0][0][0]
            resultinterpretation=  interpretationuri[len(path):len( interpretationuri)]
            decoruri = decor[0][0][0]
            resultdecor = decoruri[len(path):len(decoruri)]
            response = {
                "concept": [resultdecor,
                resultemotion,
                 resultinterpretation]
            }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

######## ***************GET Subclasses of a Concept and Instances******************
def getConceptSubClasses(request):
    path = Parameters.Params['Ontology_Path']
    c = request.GET.get('concept')
    print(c)
    if request.method == 'GET':
        uri = path+c
        try:
            Conceptquery="MATCH (n:owl__Class)-[rdfs_subClassOf]->(f:owl__Class) WHERE f.uri='%s' RETURN n.uri" %uri
            result = db.cypher_query(Conceptquery)[0]
            if(len(result)!=0):
                iteration = len(result)
                resUri=result[iteration-1][0]
                res=resUri[len(path):len(resUri)]
                lis=[]
                lis.append(res)
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
                if (len(Instanceresult) != 0 and  Instanceresult[0][0]!= None ):
                    instance = Instanceresult[0][0]
                    endString = len(instance)
                    max = len(Instanceresult)
                    lis = []
                    lis.append(instance[len(path):endString])
                    for i in range(max - 1):
                        j = i + 1
                        it = str(j)
                        instances = Instanceresult[j][0]
                        endString = len(instances)
                        resultInstance = instances[len(path):endString]
                        lis.append(resultInstance)

                    response = { "concept":lis}
                    return JsonResponse(response, safe=False)

                else:
                    lis = []
                    lis.append(c)
                    response =  {"concept":lis}
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
