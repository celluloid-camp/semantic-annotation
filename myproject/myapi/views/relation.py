from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
import json
from . import Parameters
@csrf_exempt
def getJudgementRelation(objet):
    if(objet!=None):
        if(objet=="Emotion"):
            return "judgeEmotion"
        elif (objet=="Staging"):
            return "judgeStaging"
        elif (objet=="Dramaturgy"):
            return "judgeDramaturgy"
        elif (objet=="Acting"):
            return "judgeActing"
        else:
            return None
@csrf_exempt
def getEmotionRelation(objet):
    if (objet != None):
        if (objet == "Staging"):
            return "feelsForStaging"
        elif (objet == "Dramaturgy"):
            return "feelsForDramaturgy"
        elif (objet == "Acting"):
            return "feelsForActing"
        else:
            return None
@csrf_exempt
def ColorRelation(): return "hasColor"
@csrf_exempt
def StagingTypesRelation(): return "hasStagingType"