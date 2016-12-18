from pygraph.exceptions import NodeNotFoundError, EdgeNotFoundError, \
    InvalidWeightError, InvalidLabelError, InvalidAttrKeyError


class DataMixin:
    """
    Добавление поддержки хранения данных для вершин и рёбер.
    """

    def __init__(self):
        self._edges_attrs = {}
        self._nodes_attrs = {}

    def get_node_weight(self, node) -> int:
        """
        Возвращает вес вершины.
        """
        if node not in self._nodes_attrs:
            raise NodeNotFoundError(node)
        return self._nodes_attrs[node]["weight"]

    def get_node_label(self, node) -> str:
        """
        Возвращает метку вершины.
        """
        if node not in self._nodes_attrs:
            raise NodeNotFoundError(node)
        return self._nodes_attrs[node]["label"]

    def get_edge_weight(self, edge: tuple) -> int:
        """
        Возвращает вес ребра.
        """
        if edge not in self._edges_attrs:
            raise EdgeNotFoundError(edge)
        return self._edges_attrs[edge]["weight"]

    def get_edge_label(self, edge: tuple) -> str:
        """
        Возвращает метку ребра.
        """
        if edge not in self._edges_attrs:
            raise EdgeNotFoundError(edge)
        return self._edges_attrs[edge]["label"]

    def set_node_weight(self, node, weight: int):
        """
        Присваивает указанной вершине вес.
        """
        if not isinstance(weight, int):
            raise InvalidWeightError(weight)
        self.add_node_attribute(node, "weight", weight)

    def set_node_label(self, node, label: str):
        """
        Присваивает указанной вершине метку.
        """
        if not isinstance(label, str):
            raise InvalidLabelError(label)
        self.add_node_attribute(node, "label", label)

    def set_edge_weight(self, edge: tuple, weight: int):
        """
        Присваивает указанному ребру вес.
        """
        if not isinstance(weight, int):
            raise InvalidWeightError(weight)
        self.add_edge_attribute(edge, "weight", weight)

    def set_edge_label(self, edge: tuple, label: str):
        """
        Присваивает указанному ребру метку.
        """
        if not isinstance(label, str):
            raise InvalidLabelError(label)
        self.add_edge_attribute(edge, "label", label)

    def add_node_attribute(self, node, key: str, value):
        """
        Добавляет атрибут к вершине.
        Если такой атрибут c указанным ключём уже существовал, то его значение заменяется.
        """
        if not isinstance(key, str):
            raise InvalidAttrKeyError(key)
        if node not in self._nodes_attrs:
            self._nodes_attrs[node] = {}
        self._nodes_attrs[node][key] = value

    def add_edge_attribute(self, edge: tuple, key: str, value):
        """
        Добавляет атрибут к ребру.
        Если такой атрибут уже существовал, то его значение заменяется.
        """
        if not isinstance(key, str):
            raise InvalidAttrKeyError(key)
        if edge not in self._edges_attrs:
            self._edges_attrs[edge] = {}
        self._edges_attrs[edge][key] = value
        if not self.DIRECTED and edge[0] != edge[1]:
            if (edge[1], edge[0]) not in self._edges_attrs:
                self._edges_attrs[(edge[1], edge[0])] = {}
            self._edges_attrs[(edge[1], edge[0])][key] = value

    def add_node_attributes(self, node, attrs: dict):
        """
        Добавляет набор атрибутов к вершине.
        На вход ожидается словарь с элементами вида имя_атрибута: значение.
        """
        for key, value in attrs.items():
            self.add_node_attribute(node, key, value)

    def add_edge_attributes(self, edge: tuple, attrs: dict):
        """
        Добавляет набор атрибутов к ребру.
        На вход ожидается словарь с элементами вида имя_атрибута: значение.
        """
        for key, value in attrs.items():
            self.add_edge_attribute(edge, key, value)

    def get_node_attributes(self, node) -> dict:
        """
        Возвращает словарь состоящий из атрибутов вершины.
        Каждый элемент словаря имеет вид имя_атрибута: значение.
        """
        if node not in self._nodes_attrs:
            raise NodeNotFoundError(node)
        return self._nodes_attrs[node]

    def get_edge_attributes(self, edge) -> dict:
        """
        Возвращает словарь состоящий из атрибутов ребра.
        Каждый элемент словаря имеет вид имя_атрибута: значение.
        """
        if edge not in self._edges_attrs:
            raise EdgeNotFoundError(edge)
        return self._edges_attrs[edge]

    def del_node_attribute(self, node, key: str):
        """
        Удаление атрибута с указанным ключём у вершины.
        """
        if node not in self._nodes_attrs:
            raise NodeNotFoundError(node)
        if key not in self._nodes_attrs[node]:
            raise InvalidAttrKeyError(key)
        del (self._nodes_attrs[node][key])

    def del_edge_attribute(self, edge: tuple, key: str):
        if edge not in self._edges_attrs:
            raise EdgeNotFoundError(edge)
        if key not in self._edges_attrs[edge]:
            raise InvalidAttrKeyError(key)
        del (self._edges_attrs[edge][key])

    def del_node_data(self, node):
        if node in self._nodes_attrs:
            del (self._nodes_attrs[node])
        else:
            raise NodeNotFoundError(node)

    def del_edge_data(self, edge):
        if edge not in self._edges_attrs:
            raise EdgeNotFoundError(edge)
        del (self._edges_attrs[edge])

        if not self.DIRECTED and edge[0] != edge[1]:
            reversed_edge = edge[::-1]
            if reversed_edge not in self._edges_attrs:
                raise EdgeNotFoundError(reversed_edge)
            del (self._edges_attrs[reversed_edge])

    def __eq__(self, other):
        """
        Возвращает True если атрибуты рёбер и вершин совпадают, иначе False.
        """

        def attrs_eq(attrs1: dict, attrs2: dict):
            for key1 in attrs1:
                if key1 not in attrs2:
                    return False
                if attrs1[key1] != attrs2[key1]:
                    return False

            for key2 in attrs2:
                if key2 not in attrs1:
                    return False
                if attrs1[key2] != attrs2[key2]:
                    return False
            return True

        def nodes_eq():
            for node in self.nodes():
                if not attrs_eq(self.get_node_attributes(node), other.get_node_attributes(node)):
                    return False
            return True

        def edges_eq():
            for edge in self.edges():
                if not attrs_eq(self.get_edge_attributes(edge), other.get_edge_attributes(edge)):
                    return False
            return True

        return nodes_eq() and edges_eq()
