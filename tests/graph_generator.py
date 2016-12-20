from random import randint, shuffle
from pygraph.digraph import DiGraph
from pygraph.graph import Graph


class TooManyEdgesError(Exception):
    pass


def new_graph(nodes_count: int, edges_count: int, weight_range: tuple = (1, 1)):
    if edges_count > nodes_count * (nodes_count - 1):
        raise TooManyEdgesError()
    return _generate(nodes_count, edges_count, directed=False, weight_range=weight_range)


def new_digraph(nodes_count: int, edges_count: int, weight_range: tuple = (1, 1)):
    if edges_count > nodes_count * (nodes_count - 1):
        raise TooManyEdgesError()
    return _generate(nodes_count, edges_count, directed=True, weight_range=weight_range)


def _generate(nodes_count: int, edges_count: int, directed: bool, weight_range: tuple = (1, 1)):
    """
    Создание случайного графа.
    """
    if directed:
        random_graph = DiGraph("RandomDiGraph")
    else:
        random_graph = Graph("RandomGraph")

    nodes = range(nodes_count)

    for i in nodes:
        random_graph.add_node(i)

    edges = []
    for x in nodes:
        for y in nodes:
            if (directed and x != y) or (x > y):
                edges.append((x, y))

    shuffle(edges)

    min_weight = min(weight_range)
    max_weight = max(weight_range)
    for i in range(edges_count):
        random_graph.add_edge(edges[i], weight=randint(min_weight, max_weight))

    return random_graph
