
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from neomodel import db
import json
from . import Parameters


@csrf_exempt
def createInstance(type,objet):
        path = Parameters.Params['Ontology_Path']
        uri= path+ objet
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
                try:
                    insertQuery = "MATCH (n:owl__Class) WHERE n.uri = '%s' CREATE (s:owl__NamedIndividual{id:apoc.create.uuid(), label:'concept'})-[r:rdf_type]->(n) RETURN s.id" % (uri)
                    query = db.cypher_query(insertQuery)[0]
                    idInstance= query[0][0]

                    return idInstance
                except:
                    # response = {"error": "Error occurred"}
                    return 0
            else:
                response = {"error": "Object type not specified"}
                return JsonResponse(response, safe=False)
#------------------------------------------- Creer une relation de type "relation" ayant un domaine et un range-------------------------------------------
@csrf_exempt
def createRelation(domain,relation,range):
    # if request.method == 'POST':
    #     json_data = json.loads(request.body)
    #     domain= json_data['idDomain']
    #     range= json_data['idRange']
    #     relation=json_data['relation']
        r=Parameters.Params['Ontology_Path']+relation
        print(r)
        try:
                    CreateRelationQuery = "MATCH (n:owl__ObjectProperty) WHERE n.uri = '%s'CREATE (s:owl__NamedIndividual{id:apoc.create.uuid(), label:'%s'})-[r:rdf_type]->(n) RETURN s.id" % (r,relation)
                    idRelation = db.cypher_query(CreateRelationQuery)[0][0][0]
                    print("id relation: ", idRelation)
                    CreateDomainQuery="MATCH (n:owl__NamedIndividual), (domain:owl__NamedIndividual) WHERE n.id = '%s' AND domain.id='%s' CREATE (n)-[r:rdfs_domain]->(domain) RETURN n"%(idRelation,domain)
                    db.cypher_query(CreateDomainQuery)
                    CreateRangeQuery="MATCH (n:owl__NamedIndividual), (range:owl__NamedIndividual) WHERE n.id = '%s' AND range.id='%s' CREATE (n)-[r:rdfs_range]->(range) RETURN n"%(idRelation,range)
                    db.cypher_query( CreateRangeQuery)
                    return idRelation
        except:
                    return 0

