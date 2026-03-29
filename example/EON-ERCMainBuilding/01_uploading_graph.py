import logging
from rdflib import Graph

from graphDBdrivers.graphDB import GraphDBClient

client = GraphDBClient(base_url="http://137.226.248.187:7200", repository_id="mbe-custom-ruleset")
client.logger.setLevel(logging.INFO)

IFC4x3_GRAPH = Graph().parse(r"../../ontologies\IFC4x3.ttl")
IFCplus_GRAPH = Graph().parse(r"../../ontologies\IFC4x3plus.ttl")
IFC_INSTANCE_GRAPH = Graph().parse(r"HG.ttl")
graph = IFC4x3_GRAPH + IFCplus_GRAPH + IFC_INSTANCE_GRAPH

client.delete_all_triples()
client.upload_rdflib_graph(graph)

if True:
    client.add_custom_ruleset_from_file(r"D:\PycharmProjects\ifcPlus\reasoning\rulesets\ifcPlusOptimized.pie")
    client.execute_inference()
