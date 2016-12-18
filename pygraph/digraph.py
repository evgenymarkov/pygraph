from pygraph.basegraph import BaseGraph
from pygraph.data_mixin import DataMixin
from pygraph.common_mixin import CommonMixin
from pygraph.exceptions import AdditionError, InvalidGraphType


class DiGraph(CommonMixin, DataMixin, BaseGraph):
    """
    Класс описывающий ориентированный граф.
    """
    DIRECTED = True

    def __init__(self, name, weighted=False):
        """
        Инициализация ориентированного графа.
        """
        CommonMixin.__init__(self)
        DataMixin.__init__(self)
        BaseGraph.__init__(self, name, weighted)
        self.node_neighbors = {}
        self.node_incidence = {}

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

    def incidents(self, node) -> list:
        """
        Возвращает список вершин инцидентных указанной.
        """
        return self.node_incidence[node]

    def edges(self) -> list:
        """
        Возвращает список рёбер.
        """
        return [a for a in self._edges()]

    def _edges(self):
        for n, neighbors in self.node_neighbors.items():
            for neighbor in neighbors:
                yield (n, neighbor)

    def has_node(self, node) -> bool:
        """
        Возвращает True если указанная вершина присутствует в графе, иначе False.
        """
        return node in self.node_neighbors

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
            self.node_incidence[node] = []
            self.set_node_weight(node, weight)
            self.set_node_label(node, label)
            self.add_node_attributes(node, attrs)
        else:
            raise AdditionError("Вершина %s уже присутствует в графе" % node)

    def add_edge(self, edge, weight: int = 1, label: str = "", attrs=None):
        """
        Добавляет направленное ребро соединяющее две вершины.
        Ребро - пара вершин вида (u, v).
        Опциально можно указать вес ребра, метку и другие атрибуты,
        передав их в в виде словаря с элементами вида имя_атрибута: значение.
        """
        if attrs is None:
            attrs = {}
        u, v = edge
        for n in [u, v]:
            if n not in self.node_neighbors:
                raise AdditionError("Вершина %s отсутствует в таблице соседей" % n)
            if n not in self.node_incidence:
                raise AdditionError("Вершина %s отсутствует в таблице инцидентности" % n)

        if v in self.node_neighbors[u] and u in self.node_incidence[v]:
            raise AdditionError("Ребро (%s, %s) уже присутствует в графе" % (u, v))
        else:
            self.node_neighbors[u].append(v)
            self.node_incidence[v].append(u)
            self.set_edge_weight(edge, weight)
            self.set_edge_label(edge, label)
            self.add_edge_attributes(edge, attrs)

    def del_node(self, node):
        """
        Удаляет вершину из графа.
        """
        for each in list(self.incidents(node)):
            # Удаление всех рёбер инцидентных с заданной вершиной
            self.del_edge((each, node))

        for each in list(self.neighbors(node)):
            # Удаление у соседей информации о рёбрах ведущих в указанную вершину
            self.del_edge((node, each))

        # Удаление указанной вершины из таблицы соседей и инцидентности
        del (self.node_neighbors[node])
        del (self.node_incidence[node])

        # Удаление атрибутов вершины
        self.del_node_data(node)

    def del_edge(self, edge: tuple):
        """
        Удаление направленного ребра.
        """
        u, v = edge
        self.node_neighbors[u].remove(v)
        self.node_incidence[v].remove(u)
        self.del_edge_data((u, v))

    def has_edge(self, edge: tuple) -> bool:
        """
        Возвращает True если указанное ребро присутствует в графе, иначе False.
        """
        return edge in self._edges_attrs.keys()

    def __eq__(self, other):
        """
        Перегрузка оператора ==
        Возвращает True если граф совпадает по вершинам, рёбрам и данным, иначе False.
        """
        if not isinstance(other, BaseGraph):
            raise InvalidGraphType()
        return CommonMixin.__eq__(self, other) and DataMixin.__eq__(self, other)

    def __ne__(self, other):
        """
        Перегрузка оператора !=
        Возвращает True если граф не совпадает по вершинам, рёбрам или данным, иначе False.
        """
        return not (self == other)
