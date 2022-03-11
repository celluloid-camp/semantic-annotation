import numpy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
import json
from numpy import *


@csrf_exempt
######## ***************GET main concepts******************
def getFirstConcepts(request):
    if request.method == 'GET':
        try:
            decor = db.cypher_query("MATCH(D:n4sch__Class) WHERE D.n4sch__name='Decor' return D.n4sch__name")
            emotion = db.cypher_query("MATCH(E:n4sch__Class) WHERE E.n4sch__name='Emotion' return E.n4sch__name")
            judgement = db.cypher_query("Match(J:n4sch__Class) WHERE J.n4sch__name='Judgement' return J.n4sch__name")
            interpretation = db.cypher_query("MATCH(I:n4sch__Class) WHERE I.n4sch__name='Interpretation' return I.n4sch__name")
            response = {
                "decor": decor[0][0][0],
                "emotion": emotion[0][0][0],
                "judgement": judgement[0][0][0],
                "interpretation": interpretation[0][0][0]
            }
            return JsonResponse(response, safe=False)
        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)

######## ***************GET Subclasses of a Concept and Instances******************
def getConceptSubClasses(request):
    if request.method == 'GET':
        classe= request.GET.get('concept')
        startString = len("http://www.semanticweb.org/larbim/ontologies/2022/0/Emotion-initial-version#")
        try:
            Conceptquery="MATCH (n:n4sch__Class)-[rdfs_subClassOf]->(f:n4sch__Class) WHERE f.n4sch__name='%s' RETURN n.n4sch__name" %classe
            result = db.cypher_query(Conceptquery)[0]
            print(result)
            if(len(result)!=0):
                iteration = (len(result) // 2)
                response = "'concept 0':" + "'" + result[iteration-1][0] + "'"
                for i in range(iteration-1):
                    j = i + 1
                    it = str(j)
                    response = response + ",'concept " + it + ":'" + result[i][0] + "'"
                response = "{" + response + "}"
                return JsonResponse(response, safe=False)

            else:
                Instancequery = "MATCH (n:owl__NamedIndividual)-[rdf_type]->(f:n4sch__Class) WHERE f.n4sch__name='%s' RETURN n.uri" % classe
                Instanceresult = db.cypher_query(Instancequery)[0]
                if (len(Instanceresult) != 0):
                    instance = Instanceresult[0][0]
                    endString = len(instance)
                    responseInstance = "'instance 0':" + "'" + instance[startString:endString] + "'"
                    max = len(Instanceresult)
                    for i in range(max - 1):
                        j = i + 1
                        it = str(j)
                        instances = Instanceresult[j][0]
                        endString = len(instances)
                        resultInstance = instances[startString:endString]
                        responseInstance = responseInstance + ",'instance " + it + "':'" + resultInstance + "'"
                    response = "{" + responseInstance + "}"
                    return JsonResponse(response, safe=False)

                else:
                     response = {"Message": "No Content"}
                     return JsonResponse(response, safe=False)

            # Get Individuals




        except:
            response = {"error": "Error occurred"}
            return JsonResponse(response, safe=False)
