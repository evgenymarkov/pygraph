from pygraph.algorithms.bfs import breadth_first_bypass


def check_graph_is_connected(graph) -> bool:
    # Шаг 1: обход графа с 1-ой вершины
    bypassed_nodes = breadth_first_bypass(graph, graph.nodes()[0])

    # Если посещены не все вершины, то возвращаем False
    if len(bypassed_nodes) != graph.order():
        return False

    # Шаг 2: получаем обратный граф
    reversed_graph = graph.reverse()

    # Шаг 3: обход обратного графа с 1-ой вершины
    bypassed_nodes = breadth_first_bypass(reversed_graph, graph.nodes()[0])

    # Если посещены не все вершины, то возвращаем False
    if len(bypassed_nodes) != graph.order():
        return False

    return True
