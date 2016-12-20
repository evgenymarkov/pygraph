from pygraph.basegraph import BaseGraph
from pygraph.data_mixin import DataMixin
from pygraph.common_mixin import CommonMixin
from pygraph.exceptions import AdditionError, InvalidGraphType, \
    NodeNotFoundError, EdgeNotFoundError, InvalidIdentifierTypeError


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
        self._neighbors = {}

    def nodes(self) -> list:
        """
        Возвращает список вершин.
        """
        return list(self._neighbors.keys())

    def node_degree(self, node) -> int:
        """
        Возвращает степень указанной вершины.
        """
        if node not in self._neighbors:
            raise NodeNotFoundError(node)
        return len(self.neighbors(node))

    def neighbors(self, node) -> list:
        """
        Возвращает список соседей указанной вершины.
        """
        if node not in self._neighbors:
            raise NodeNotFoundError(node)
        return self._neighbors[node]

    def add_node(self, node, weight: int = 1, label: str = "", attrs=None):
        """
        Добавляет указанную вершину к графу.
        Опциально можно указать вес вершины, метку и другие атрибуты,
        передав их в в виде словаря с элементами вида имя_атрибута: значение.
        """
        if not isinstance(node, str):
            raise InvalidIdentifierTypeError(node)

        if attrs is None:
            attrs = {}

        if node not in self._neighbors:
            self._neighbors[node] = []
            self.set_node_weight(node, weight)
            self.set_node_label(node, label)
            self.add_node_attributes(node, attrs)
        else:
            raise AdditionError("Вершина %s уже присутствует в графе" % node)

    def has_node(self, node) -> bool:
        """
        Возвращает True если указанная вершина присутствует в графе, иначе False.
        """
        return node in self._neighbors

    def del_node(self, node):
        """
        Удаляет указанную вершину из графа, а также инцидентные ей рёбра.
        """
        if node not in self._neighbors:
            raise NodeNotFoundError(node)

        for each in list(self.neighbors(node)):
            if each != node:
                self.del_edge((each, node))
        del (self._neighbors[node])
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
        if not isinstance(edge[0], str):
            raise InvalidIdentifierTypeError(edge[0])

        if not isinstance(edge[1], str):
            raise InvalidIdentifierTypeError(edge[1])

        if attrs is None:
            attrs = {}

        u, v = edge
        if (v not in self._neighbors[u]) and (u not in self._neighbors[v]):
            self._neighbors[u].append(v)
            if u != v:
                self._neighbors[v].append(u)

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
        if edge not in self._edges_attrs:
            raise EdgeNotFoundError(edge)

        self.del_edge_data(edge)
        u, v = edge
        self._neighbors[u].remove(v)
        if u != v:
            self._neighbors[v].remove(u)

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
