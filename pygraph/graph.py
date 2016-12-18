from pygraph.basegraph import BaseGraph
from pygraph.data_mixin import DataMixin
from pygraph.common_mixin import CommonMixin
from pygraph.exceptions import AdditionError, InvalidGraphType


class Graph(CommonMixin, DataMixin, BaseGraph):
    """
    Класс описывающий неориентированный граф.
    """
    DIRECTED = False

    def __init__(self, name, weighted=False):
        """
        Инициализация графа.
        """
        CommonMixin.__init__(self)
        DataMixin.__init__(self)
        BaseGraph.__init__(self, name, weighted)
        self.node_neighbors = {}

    def nodes(self) -> list:
        """
        Возвращает список вершин.
        """
        return list(self.node_neighbors.keys())

    def neighbors(self, node) -> list:
        """
        Возвращает список соседей указанной вершины.
        """
        return self.node_neighbors[node]

    def add_node(self, node, weight: int = 1, label: str = "", attrs=None):
        """
        Добавляет указанную вершину к графу.
        Опциально можно указать вес вершины, метку и другие атрибуты,
        передав их в в виде словаря с элементами вида имя_атрибута: значение.
        """
        if attrs is None:
            attrs = {}

        if node not in self.node_neighbors:
            self.node_neighbors[node] = []
            self.set_node_weight(node, weight)
            self.set_node_label(node, label)
            self.add_node_attributes(node, attrs)
        else:
            raise AdditionError("Вершина %s уже присутствует в графе" % node)

    def has_node(self, node) -> bool:
        """
        Возвращает True если указанная вершина присутствует в графе, иначе False.
        """
        return node in self.node_neighbors

    def del_node(self, node):
        """
        Удаляет указанную вершину из графа, а также инцидентные ей рёбра.
        """
        for each in list(self.neighbors(node)):
            if each != node:
                self.del_edge((each, node))
        del (self.node_neighbors[node])
        del (self._nodes_attrs[node])

    def edges(self) -> list:
        """
        Возвращает список рёбер.
        """
        return [a for a in self._edges_attrs.keys()]

    def add_edge(self, edge: tuple, weight: int = 1, label: str = "", attrs=None):
        """
        Добавляет указанное ребро, соединяющее две вершины.
        Ребро - пара вершин вида (u, v).
        Опциально можно указать вес ребра, метку и другие атрибуты,
        передав их в в виде словаря с элементами вида имя_атрибута: значение.
        """
        if attrs is None:
            attrs = {}

        u, v = edge
        if v not in self.node_neighbors[u] and u not in self.node_neighbors[v]:
            self.node_neighbors[u].append(v)
            if u != v:
                self.node_neighbors[v].append(u)

            self.set_edge_weight((u, v), weight)
            self.set_edge_label((u, v), label)
            self.add_edge_attributes((u, v), attrs)
        else:
            raise AdditionError("Ребро (%s, %s) уже присутствует в графе" % (u, v))

    def has_edge(self, edge: tuple) -> bool:
        """
        Возвращает True если указанное ребро присутствует в графе, иначе False.
        """
        u, v = edge
        return (u, v) in self._edges_attrs

    def del_edge(self, edge: tuple):
        """
        Удаляет указанное ребро из графа.
        """
        self.del_edge_data(edge)
        u, v = edge
        self.node_neighbors[u].remove(v)
        if u != v:
            self.node_neighbors[v].remove(u)

    def __eq__(self, other) -> bool:
        """
        Перегрузка оператора ==
        Возвращает True если граф совпадает по вершинам, рёбрам и атрибутам, иначе False.
        """
        if not isinstance(other, BaseGraph):
            raise InvalidGraphType()
        return CommonMixin.__eq__(self, other) and DataMixin.__eq__(self, other)

    def __ne__(self, other) -> bool:
        """
        Перегрузка оператора !=
        Возвращает True если граф не совпадает по вершинам, рёбрам или атрибутам, иначе False.
        """
        return not (self == other)
