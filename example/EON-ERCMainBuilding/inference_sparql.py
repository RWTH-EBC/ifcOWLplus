import os
import logging

from graphDBdrivers.graphDB import GraphDBClient
from graphLib.namespaces import IFCplus

current_path = os.path.dirname(os.path.abspath(__file__))

query_files = [
    "HasLocation.sparql",
    "Device.sparql",
    "HasPropertySet.sparql",
    "HasPort.sparql",
    "FeedsPort.sparql",
    "Feeds.sparql",
    "FeedsInDirectly.sparql",
    "IsConnectedTo.sparql",
    "ReturnsWater.sparql",
    "SuppliesWater.sparql",
    "SuppliesAir.sparql",
    "ReturnsAir.sparql",
]


def ifc_plus_inference(client: GraphDBClient):

    for query_file in query_files:

        with open(f'{current_path}/queries/{query_file}', mode='r', encoding="utf8") as file:
            query = file.read()

        success, exec_time, n_added = client.execute_sparql_insert(query)

        print(
            f'Query: {query_file} took {exec_time:.2f} seconds and added {n_added} triples.'
        )


def ifc_plus_remove(client: GraphDBClient):

    success, exec_time, n_removed = client.delete_namespace(IFCplus)
    print(
        f'Removed {n_removed} triples from IFCplus namespace in {exec_time:.2f} seconds.'
    )


if __name__ == "__main__":

    client = GraphDBClient(base_url="http://137.226.248.187:7200", repository_id="mbe-ifc")
    client.logger.setLevel(logging.INFO)

    ifc_plus_inference(client)

