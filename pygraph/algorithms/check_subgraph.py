import itertools
from pygraph.graph import Graph
from pygraph.algorithms.isomorphism import isomorphism
from pygraph.algorithms.check_connectivity import check_graph_is_connected


def is_subgraph(graph: Graph, subgraph: Graph) -> (bool, Graph):
    """
    Для двух заданных невзвешанных и неориентированных графов
    определяет является ли один из графов подграфом другого графа.
    """
    if len(subgraph.nodes()) < len(graph.nodes()):
        for sub_nodes in itertools.combinations(graph.nodes(), len(subgraph.nodes())):
            subg = Graph("TmpSubgraph")
            for node in sub_nodes:
                subg.add_node(node)
                for neighbour in graph.neighbors(node):
                    new_edge = (node, neighbour)
                    if not subg.has_edge(new_edge):
                        try:
                            subg.add_edge(new_edge)
                        except KeyError:
                            pass
            if check_graph_is_connected(subg) and isomorphism(subg, subgraph):
                return True, subg
    return False, None
