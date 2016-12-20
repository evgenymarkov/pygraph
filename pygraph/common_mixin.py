from pygraph.basegraph import BaseGraph


class CommonMixin:
    """
    Общие методы для всех видов графов.
    """

    def __str__(self):
        """
        Возвращает строковое представление графа при вызове str() или print().
        """
        str_nodes = repr(self.nodes())
        str_edges = repr(self.edges())
        return "%s %s" % (str_nodes, str_edges)

    def __repr__(self):
        """
        Возвращает строковое представление графа при вызове repr().
        """
        return "<%s.%s %s>" % (self.__class__.__module__, self.__class__.__name__, str(self))

    def __iter__(self):
        """
        Возвращает итератор для прохода по всем вершинам.
        """
        for n in self.nodes():
            yield n

    def __len__(self):
        """
        Вызов len() функции для графа вернёт количество вершин.
        """
        return self.order()

    def __getitem__(self, node):
        """
        Возвращает итератор для прохода по всем соседям.
        Пример использования:
        for node in graph["target_node"]:
            print(node)
        """
        for n in self.neighbors(node):
            yield n

    def order(self):
        """
        Возвращает порядок графа (количество вершин)
        """
        return len(self.nodes())

    def complete(self):
        """
        Дополняет граф до полного.
        Модифицирует текущий граф!
        https://ru.wikipedia.org/wiki/Полный_граф
        """
        for each in self.nodes():
            for other in self.nodes():
                if each != other and not self.has_edge((each, other)):
                    self.add_edge((each, other))

    def inverse(self):
        """
        Возвращает дополнение графа (обратный граф).
        https://ru.wikipedia.org/wiki/Дополнение_графа
        """
        inv = self.__class__(self.name)
        for i in self.nodes():
            inv.add_node(i, attrs=self.get_node_attributes(i))
        inv.complete()
        for each in self.edges():
            if inv.has_edge(each):
                inv.del_edge(each)
        return inv

    def reverse(self):
        """
        Возвращает граф, полученный из заданного сменой направления ребер на противоположное.
        Если граф неориентированный, то возвращается копия графа.
        """
        new_graph = self.__class__(self.name)
        for i in self.nodes():
            new_graph.add_node(i)

        if self.DIRECTED:
            for (u, v) in self.edges():
                weight = self.get_edge_weight((u, v))
                label = self.get_edge_label((u, v))
                attributes = self.get_edge_attributes((u, v))
                new_graph.add_edge((v, u), weight, label, attributes)
        else:
            for (u, v) in self.edges():
                weight = self.get_edge_weight((u, v))
                label = self.get_edge_label((u, v))
                attributes = self.get_edge_attributes((u, v))
                new_graph.add_edge((u, v), weight, label, attributes)

        return new_graph

    def __eq__(self, other: BaseGraph) -> bool:
        """
        Возвращает True если множества вершин и рёбер совпадают.
        """

        def nodes_eq():
            for each in self.nodes():
                if not other.has_node(each):
                    return False
            for each in other.nodes():
                if not self.has_node(each):
                    return False
            return True

        def edges_eq():
            for edge in self.edges():
                if not other.has_edge(edge):
                    return False
            for edge in other.edges():
                if not self.has_edge(edge):
                    return False
            return True

        try:
            return nodes_eq() and edges_eq()
        except AttributeError:
            return False
