import os
import logging

from graphDBdrivers.graphDB import GraphDBClient

current_path = os.path.dirname(os.path.abspath(__file__))

query_files = [
    "IfcHVACDesign.sparql",
    "IfcSensor.sparql",
    "IfcValve.sparql",
]


def add_datapoints(client: GraphDBClient):

    for query_file in query_files:

        with open(f'{current_path}/queries/{query_file}', mode='r', encoding="utf8") as file:
            query = file.read()

        success, exec_time, n_added = client.execute_sparql_insert(query)

        print(
            f'Query: {query_file} took {exec_time:.2f} seconds and added {n_added} triples.'
        )


if __name__ == "__main__":

    client = GraphDBClient(base_url="http://137.226.248.187:7200", repository_id="mbe-custom-ruleset")
    client.logger.setLevel(logging.INFO)

