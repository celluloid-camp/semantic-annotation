from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db


@csrf_exempt
def getFirstConcepts(request):
    if request.method == 'GET':
        try:
            decor = db.cypher_query("MATCH(D:n4sch__Class) WHERE D.n4sch__name='Decor' return D.n4sch__name")
            emotion = db.cypher_query("MATCH(E:n4sch__Class) WHERE E.n4sch__name='Emotion' return E.n4sch__name")
            judgement = db.cypher_query("MATCH(J:n4sch__Class) WHERE J.n4sch__name='Judgement' return J.n4sch__name")
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

