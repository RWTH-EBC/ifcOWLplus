import requests
from rdflib import Graph


base_url = "http://137.226.248.187:7200"
repo = "mbe-custom-ruleset"
session = requests.Session()


IFC4x3_GRAPH = Graph().parse('../ontologies/IFC4x3.ttl')
IFCplus_GRAPH = Graph().parse('../ontologies/IFC4x3plus.ttl')
IFC_INSTANCE_GRAPH = Graph().parse('HG.ttl')

graph = IFC4x3_GRAPH + IFCplus_GRAPH + IFC_INSTANCE_GRAPH

graph.serialize()


def execute_sparql_update(update: str):

    url = f"{base_url}/repositories/{repo}"
    headers = {
        "Content-Type": "application/sparql-query",
        "Accept": "application/sparql-results+json"
    }
    data = {"update": update}

    response = session.post(url, headers=headers, data=data)
    response.raise_for_status()

    return response.json()


def execute_sparql_insert(update: str):

    url = f"{base_url}/repositories/{repo}/statements"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"update": update}

    response = session.post(url, headers=headers, data=data)
    response.raise_for_status()

    return None

