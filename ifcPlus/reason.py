import typing
import os
import pathlib

# get current directory of this file
current_directory = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
QUERY_FOLDER = current_directory.parent.joinpath("reasoning/sparql")
QUERY_FILES = [
    # spatial relationships
    "hasLocation.sparql",
    "hasWall.sparql",
    "isAdjacentTo.sparql",
    "IsExternal.sparql",
    "contains.sparql",

    # connectivity relationships
    "feedsPort.sparql",
    "feedsIndirectly.sparql",
    "isConnectedTo.sparql",
    # "supplies_returns.sparql",
    "supplies_returns_HLS.sparql",
    "serves.sparql",

    # system
    # "assemblyConnection.sparql",
    "belongsToSystem.sparql",

    "supplies_returns_HLS.sparql",
]


def read_queries() -> typing.List[typing.Tuple[str, str]]:

    queries = []
    for file in QUERY_FILES:
        with open(QUERY_FOLDER.joinpath(file), 'r', encoding='utf-8') as f:
            query = f.read()
            queries.append((file, query))

    return queries


def execute_reasoning(query_callback: typing.Callable) -> dict:

    queries = read_queries()
    results = {}
    for file, query in queries:
        print(file)
        results[file] = query_callback(query)

    return results


if __name__ == "__main__":

    # print queries to console
    q = read_queries()
    for file, query in q:
        print(f"Query: {file}\n{query}\n")
