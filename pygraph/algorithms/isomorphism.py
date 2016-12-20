def isomorphism(graph_1, graph_2):
    """Определяет, являются ли два неориентированных графа graph_1 и graph_2,
    представленных своими матрицами смежности изоморфными.

    Если да, то возвращает список phi длины N (число вершин в графах),
    состоящий из чисел 0..N-1, такой что phi[i] - номер вершины второго графа,
    соответствующей i-й вершине первого графа
    (верщины нумеруются числами 0..N-1); если нет - возвращает
    пустой список."""

    g_len = len(graph_1)
    if g_len != len(graph_2):
        return False

    # хеш-таблица, отображающая ключ - характеристику-инвариант
    # вершин при перенумерации в пару списков номеров вершин имеющих эту
    # характеристикой из графов G1 и G2
    groups = {}

    for g in [0, 1]:
        graph = [graph_1, graph_2][g]
        for x in graph.nodes():
            # в данном алгоритме характеристика каждой вершин
            # состоит из ее степени (v_pov)
            # и мультимножества степеней соседних с ней вершин (a_pov)
            v_pow = len(graph.neighbors(x))
            a_pov = tuple(sorted(len(graph.neighbors(y)) for y in graph[x]))
            c = (v_pow, a_pov)

            if c not in groups:
                groups[c] = [[], []]
            groups[c][g].append(x)

    # проверяем что размеры группы вершин с одинаковой характеристикой
    # одинаковы в обоих графах
    for A, B in groups.values():
        if len(A) != len(B):
            return False

    # теперь остается только перебрать какая вершина первого графа
    # соответствует какой вершине второго графа внутри каждой группы

    # упорядочиваем группы по возрастанию их размера
    sgroups = [(len(A), A, B) for A, B in groups.values()]
    sgroups = sorted(sgroups)

    # перебор
    phi = dict()
    rev = dict()

    def good(x, y):
        for z in graph_1[x]:
            # если есть образ,который не соединен с образом X,
            # то предположение не верно
            if z in phi and not graph_2.has_edge((phi[x], phi[z])):
                return False
        for z in graph_2[y]:
            # если есть праобраз,который не соединен с праобразом Y,
            # то предположение не верно
            if z in rev and not graph_1.has_edge((rev[y], rev[z])):
                return False
        return True

    def rec(k, i):
        #  закончили работать с группами
        if k == len(sgroups):
            return True

        # закончили работать с конкретной группой
        L, A, B = sgroups[k]
        if i == L:
            return rec(k+1, 0)

        x = A[i]
        for y in B:
            #  если у элемента уже есть праобраз, то мы его пропускаем
            if y in rev:
                continue

            # строим отображение
            phi[x] = y
            rev[y] = x
            if good(x, y) and rec(k, i+1):
                return True
            phi.pop(x)
            rev.pop(y)

    if rec(0, 0):
        return phi
    return False
