from pygraph.exceptions import NodeNotFoundError


def breadth_first_search(graph, start_node, target_node) -> list:
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

