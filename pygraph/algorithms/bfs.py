from pygraph.exceptions import NodeNotFoundError


def breadth_first_bypass(graph, start_node) -> list:
    """
    Обход графа в ширину.
    Возвращает список пройденных вершин в порядке их обхода.
    """
    if not graph.has_node(start_node):
        raise NodeNotFoundError(start_node)

    visited, queue = [], [start_node]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
            node_neighbours = set(x for x in graph[node])
            queue.extend(node_neighbours.difference(visited))
    return visited


def breadth_first_search(graph, start_node, target_node) -> list:
    """
    Поиск пути от стартовой вершины до конечной.
    Возвращает список пройденных вершин или None если вершина недостижима.
    """
    if not graph.has_node(start_node):
        raise NodeNotFoundError(start_node)
    if not graph.has_node(target_node):
        raise NodeNotFoundError(target_node)

    queue = [(start_node, [start_node])]  # (node, [path_to_target])
    while queue:
        (node, path) = queue.pop(0)
        # Проход по всем соседям за исключением тех кого уже обошли
        node_neighbours = set(x for x in graph[node])
        for neighbour in node_neighbours - set(path):
            if neighbour == target_node:
                return path + [neighbour]
            else:
                queue.append((neighbour, path + [neighbour]))

    return None


def breadth_first_paths(graph, start_node, target_node) -> list:
    """
    Поиск всех путей от стартовой вершины до конечной.
    Возвращает список путей, где каждый путь - набор пройденных вершин.
    """
    if not graph.has_node(start_node):
        raise NodeNotFoundError(start_node)
    if not graph.has_node(target_node):
        raise NodeNotFoundError(target_node)

    all_paths = []
    queue = [(start_node, [start_node])]  # (node, [path_to_target])
    while queue:
        (node, path) = queue.pop(0)
        # Проход по всем соседям за исключением тех кого уже обошли
        node_neighbours = set(x for x in graph[node])
        for neighbour in node_neighbours - set(path):
            if neighbour == target_node:
                all_paths.append(path + [neighbour])
            else:
                queue.append((neighbour, path + [neighbour]))

    return all_paths
