class GraphError(RuntimeError):
    """
    Базовый класс описывающий ошибки, которые могут быть получены при работе
    со структурами данных представленными в данном модуле.
    """
    pass


class InvalidIdentifierTypeError(GraphError):
    """
    Ошибка сигнализирующая о том, что выбран неподходящий идентификатор вершины или ребра.
    """
    def __init__(self, identifier):
        self.msg = "Идентификатор имеет тип %s, но он должен быть строкой" % type(identifier)
        self.identifier = identifier


class NodeNotFoundError(GraphError):
    """
    Указанная вершина не найдена в графе.
    """

    def __init__(self, node):
        self.msg = "Вершина %s не найдена" % (repr(node))
        self.node = node


class EdgeNotFoundError(GraphError):
    """
    Указанное ребро не найдено в графе.
    """

    def __init__(self, edge: tuple):
        self.msg = "Ребро %s не найдено" % (repr(edge))
        self.edge = edge


class InvalidWeightError(GraphError):
    """
    Ошибка информирующая о том что вес графа задан неверно.
    """

    def __init__(self, weight):
        self.msg = "Вес должен быть целым числом. Указан %s." % (repr(weight))
        self.weight = weight


class InvalidLabelError(GraphError):
    """
    Ошибка информирующая о том что метка графа задана неверно.
    """

    def __init__(self, label):
        self.msg = "Метка должна быть строкой. Указана %s." % (repr(label))
        self.label = label


class InvalidAttrKeyError(GraphError):
    """
    Ошибка информирующая о том что ключ атрибута задан неверно.
    """

    def __init__(self, key):
        self.msg = "Ключ атрибута должен быть непустой строкой. Указан %s." % (repr(key))
        self.key = key


class AdditionError(GraphError):
    """
    Ошибка возникающая при неудачном добавлении рёбер или вершин в граф.
    """
    pass


class InvalidGraphType(GraphError):
    """
    Неподдерживаемый тип графа.
    """
    pass


class NodeUnreachable(GraphError):
    """
    Целевая вершина не может быть достигнута.
    """

    def __init__(self, start, goal):
        self.msg = "Вершина %s не может быть достигнута из вершины %s" % (repr(goal), repr(start))
        self.start = start
        self.goal = goal


class AlgorithmError(RuntimeError):
    """
    Базовый класс для различных ошибок, которые могут произойти в ходе работы
    алгоритмов работающих с графами.
    """
    pass
