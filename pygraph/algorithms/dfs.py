from pygraph.exceptions import NodeNotFoundError


def depth_first_bypass(graph, start_node) -> list:
    """
    Обход графа в глубину.
    Возвращает список пройденных вершин в порядке их обхода.
    """
    if not graph.has_node(start_node):
        raise NodeNotFoundError(start_node)

    visited, stack = [], [start_node]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            node_neighbours = set(x for x in graph[node])
            stack.extend(node_neighbours.difference(visited))
    return visited


def depth_first_search(graph, start_node, target_node) -> list:
    """
    Поиск пути от стартовой вершины до конечной.
    Возвращает список пройденных вершин или None если вершина недостижима.
    """
    if not graph.has_node(start_node):
        raise NodeNotFoundError(start_node)
    if not graph.has_node(target_node):
        raise NodeNotFoundError(target_node)

    stack = [(start_node, [start_node])]
    while stack:
        (node, path) = stack.pop()
        node_neighbours = set(x for x in graph[node])
        for neighbour in node_neighbours.difference(set(path)):
            if neighbour == target_node:
                return path + [neighbour]
            else:
                stack.append((neighbour, path + [neighbour]))

    return None


def depth_first_paths(graph, start_node, target_node) -> list:
    """
    Поиск всех путей от стартовой вершины до конечной.
    Возвращает список путей, где каждый путь - набор пройденных вершин.
    """
    if not graph.has_node(start_node):
        raise NodeNotFoundError(start_node)
    if not graph.has_node(target_node):
        raise NodeNotFoundError(target_node)

    all_paths = []
    stack = [(start_node, [start_node])]
    while stack:
        (node, path) = stack.pop()
        node_neighbours = set(x for x in graph[node])
        for neighbour in node_neighbours.difference(set(path)):
            if neighbour == target_node:
                all_paths.append(path + [neighbour])
            else:
                stack.append((neighbour, path + [neighbour]))

    return all_paths
