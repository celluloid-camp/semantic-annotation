
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
        try:
                    CreateRelationQuery = "MATCH (n:owl__ObjectProperty) WHERE n.uri = '%s'CREATE (s:owl__NamedIndividual{id:apoc.create.uuid(), label:'%s'})-[r:rdf_type]->(n) RETURN s.id" % (r,relation)
                    idRelation = db.cypher_query(CreateRelationQuery)[0][0][0]

                    CreateDomainQuery="MATCH (n:owl__NamedIndividual), (domain:owl__NamedIndividual) WHERE n.id = '%s' AND domain.id='%s' CREATE (n)-[r:rdfs_domain]->(domain) RETURN n"%(idRelation,domain)
                    db.cypher_query(CreateDomainQuery)
                    CreateRangeQuery="MATCH (n:owl__NamedIndividual), (range:owl__NamedIndividual) WHERE n.id = '%s' AND range.id='%s' CREATE (n)-[r:rdfs_range]->(range) RETURN n"%(idRelation,range)
                    db.cypher_query( CreateRangeQuery)
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

