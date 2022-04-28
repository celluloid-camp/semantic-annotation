
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
import json
from . import Parameters


@csrf_exempt
def createInstance(objet):
        path = Parameters.Params['Ontology_Path']
        uri= path+ objet
        type=typeOfObject(objet)
        if(type=="instance"):
            try:
                insertQuery = "MATCH (n:owl__NamedIndividual) WHERE n.uri = '%s'CREATE (s:owl__NamedIndividual{id:apoc.create.uuid(),label:'concept'})-[r:rdf_type]->(n) RETURN s.id" % (uri)
                query = db.cypher_query(insertQuery)[0]
                idInstance= query[0][0]
                return idInstance
            except:
                # response = {"error": "Error occurred"}
                return 0
        else:
            if(type=="classe"):
                print("i am a class")
                try:
                    insertQuery = "MATCH (n:owl__Class) WHERE n.uri = '%s' CREATE (s:owl__NamedIndividual{id:apoc.create.uuid(), label:'concept'})-[r:rdf_type]->(n) RETURN s.id" % (uri)
                    query = db.cypher_query(insertQuery)[0]
                    idInstance= query[0][0]
                    return idInstance
                except:
                    # response = {"error": "Error occurred"}
                    return 0
            else:
                print("am not a class")
                return 0
#------------------------------------------- Creer une relation de type "relation" ayant un domaine et un range-------------------------------------------
@csrf_exempt
def createRelation(domain,relation,range):
        r=Parameters.Params['Ontology_Path']+relation
        print('create relation func',r)
        try:
                    CreateRelationQuery = "MATCH (n:owl__ObjectProperty) WHERE n.uri = '%s'CREATE (s:owl__NamedIndividual{id:apoc.create.uuid(), label:'%s'})-[r:rdf_type]->(n) RETURN s.id" % (r,relation)
                    idRelation = db.cypher_query(CreateRelationQuery)[0][0][0]
                    print('1')
                    CreateDomainQuery="MATCH (n:owl__NamedIndividual), (domain:owl__NamedIndividual) WHERE n.id = '%s' AND domain.id='%s' CREATE (n)-[r:rdfs_domain]->(domain) RETURN n"%(idRelation,domain)
                    db.cypher_query(CreateDomainQuery)
                    print('2')
                    CreateRangeQuery="MATCH (n:owl__NamedIndividual), (range:owl__NamedIndividual) WHERE n.id = '%s' AND range.id='%s' CREATE (n)-[r:rdfs_range]->(range) RETURN n"%(idRelation,range)
                    db.cypher_query( CreateRangeQuery)
                    print('3')
                    return idRelation
        except:
                    return 0

def typeOfObject(concept):
    if len(concept)!=0:
        uri=Parameters.Params['Ontology_Path']+concept
        GetConceptQuery = "MATCH (n:owl__Class) WHERE n.uri = '%s' RETURN n" % uri
        result= db.cypher_query(GetConceptQuery )[0]
        # print("afficher resultat:", result)
        if len(result)==0:
           # Test if objet is an instance:
           GetConceptQuery = "MATCH (n:owl__NamedIndividual) WHERE n.uri = '%s' RETURN n" % uri
           res=db.cypher_query(GetConceptQuery)[0]
           if(len(res)==0):
               type=0
           else:
               type = "instance"
        else:
            type="classe"
        return type

@csrf_exempt
def typeOfRelation(request):
        concept = request.GET.get('concept')
        if request.method == 'GET':
            try:
                relation = "has" + concept
                response = {"relation": relation}
                return JsonResponse(response, safe=False)
            except:
                response = {"error": relation}
                return JsonResponse(response, safe=False)

@csrf_exempt
def getConceptTreeStructur(concept):
    if len(concept)!=0:
        path=Parameters.Params['Ontology_Path']
        uri=Parameters.Params['Ontology_Path']+concept
        GetConceptQuery = "MATCH (n:owl__Class)-[rdf_type]-(f:owl__NamedIndividual) WHERE f.uri='%s' RETURN n.uri" % uri
        result= db.cypher_query(GetConceptQuery)
        try:
            response = result[0][0][0]
            return response
        except:
            GetConceptQuery = "MATCH (n:owl__Class)<-[rdfs_subClassOf]-(f:owl__Class) WHERE f.uri='%s' RETURN n.uri" % uri
            result= db.cypher_query(GetConceptQuery)
            try:
                chaine= result[0][0][0]
                if( chaine[0:len(Parameters.Params['Ontology_Path'])]==path):
                        response = result[0][0][0]
                else:
                    response = result[0][1][0]
                return response
            except:
                  return 'error'
@csrf_exempt
def emotionOrJudgement(input):
    case=False
    path = Parameters.Params['Ontology_Path']
    if(len(input)!=0):
        try:
                superClass = input
                if(superClass=="Emotion" or superClass=="Judgement"):
                    return True
                else:
                    while (superClass != 'Emotion' and superClass != 'Staging' and superClass != 'Acting' and superClass != 'Spectacle' and superClass != 'Dramaturgy' and superClass != 'Judgement' and case == False):
                        # GET SUPER CLASS
                        super = getConceptTreeStructur(superClass)
                        superClass = super[len(path): len(super)]
                        if (superClass == 'Emotion' or superClass == 'Judgement'):
                            case = True
                    return case
        except:
            return "Error"

    else:
        return case