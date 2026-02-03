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

