import pydot
from pygraph.graph import Graph
from pygraph.digraph import DiGraph
from pygraph.exceptions import InvalidGraphType, GraphError


def read(string: str):
    """
    Чтение графа из строки написанной в dot формате.
    """

    read_graphs = pydot.graph_from_dot_data(string)
    if len(read_graphs) != 1:
        raise GraphError("Строка содержит 0 или более 1 графа")
    dot_graph = read_graphs[0]
    name = dot_graph.get_name()

    if dot_graph.get_type() == "graph":
        graph = Graph(name)
    elif dot_graph.get_type() == "digraph":
        graph = DiGraph(name)
    else:
        raise InvalidGraphType

    # Чтение вершин
    for each_node in dot_graph.get_nodes():
        # Получение веса вершины
        if "weight" in each_node.get_attributes().keys():
            graph.weighted = True
            node_weight = int(each_node.get_attributes()["weight"])
            del (each_node.get_attributes()["weight"])
        else:
            node_weight = 1

        # Получение метки вершины
        if "label" in each_node.get_attributes().keys():
            node_label = each_node.get_attributes()["label"]
            del (each_node.get_attributes()["label"])
        else:
            node_label = ""

        graph.add_node(each_node.get_name(), weight=node_weight, label=node_label,
                       attrs=each_node.get_attributes())

    # Чтение рёбер
    for each_edge in dot_graph.get_edges():
        if not graph.has_node(each_edge.get_source()):
            graph.add_node(each_edge.get_source())
        if not graph.has_node(each_edge.get_destination()):
            graph.add_node(each_edge.get_destination())

        # pydot generates unwanted quotes on edge output
        # https://github.com/erocarrera/pydot/issues/66
        for key, value in each_edge.get_attributes().items():
            if value.startswith('"') and value.endswith('"'):
                each_edge.set(key, value[1:-1])

        # Получение веса ребра
        if "weight" in each_edge.get_attributes().keys():
            graph.weighted = True
            edge_weight = int(each_edge.get_attributes()["weight"])
            del (each_edge.get_attributes()["weight"])
        else:
            edge_weight = 1

        # Получение метки ребра
        if "label" in each_edge.get_attributes().keys():
            edge_label = each_edge.get_attributes()["label"]
            del (each_edge.get_attributes()["label"])
        else:
            edge_label = ""

        graph.add_edge((each_edge.get_source(), each_edge.get_destination()),
                       weight=edge_weight, label=edge_label, attrs=each_edge.get_attributes())

    return graph


def write(graph) -> str:
    """
    Возвращает строку в формате dot описывающую заданный граф.
    """
    dot_graph = pydot.Dot()
    dot_graph.set_name(graph.name)

    if isinstance(graph, Graph):
        dot_graph.set_type("graph")
        directed = False
    elif isinstance(graph, DiGraph):
        dot_graph.set_type("digraph")
        directed = True
    else:
        raise InvalidGraphType("Ожидался ориентированный или неориентированный граф." +
                               "Получен %s" % repr(graph))

    for node in graph.nodes():
        dot_node = pydot.Node(str(node), **graph.get_node_attributes(node))
        dot_graph.add_node(dot_node)

    seen_edges = set([])
    for edge_from, edge_to in graph.edges():
        edge = edge_from, edge_to
        if (str(edge_from) + "-" + str(edge_to)) in seen_edges:
            continue
        if (not directed) and (str(edge_to) + "-" + str(edge_from)) in seen_edges:
            continue

        # Удаление атрибута веса для невзвешенных графов
        if not graph.weighted:
            graph.del_edge_attribute(edge, "weight")

        dot_edge = pydot.Edge(str(edge_from), str(edge_to), **graph.get_edge_attributes(edge))
        dot_graph.add_edge(dot_edge)
        seen_edges.add(str(edge_from) + "-" + str(edge_to))

    return dot_graph.to_string()
