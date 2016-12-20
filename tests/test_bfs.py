import unittest
from pygraph.graph import Graph
from pygraph.digraph import DiGraph
from pygraph.exceptions import NodeNotFoundError
from pygraph.algorithms.bfs import breadth_first_paths, breadth_first_bypass, breadth_first_search


class TestBFS(unittest.TestCase):
    def test_bfs_bypass_path_exists(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((1, 3))
        gr.add_edge((2, 3))

        bypassed_nodes = breadth_first_bypass(gr, 1)
        assert bypassed_nodes == [1, 2, 3]

    def test_bfs_bypass_path_not_exists(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((1, 3))
        gr.add_edge((2, 3))

        bypassed_nodes = breadth_first_bypass(gr, 2)
        assert bypassed_nodes == [2, 3]

    def test_bfs_non_existent_start_node_in_graph(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        try:
            breadth_first_search(gr, 3, 1)
        except NodeNotFoundError:
            pass
        else:
            self.fail()

    def test_bfs_non_existent_target_node_in_graph(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        try:
            breadth_first_search(gr, 1, 3)
        except NodeNotFoundError:
            pass
        else:
            self.fail()

    def test_bfs_easy_path(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((2, 3))
        path = breadth_first_search(gr, 1, 3)
        assert path == [1, 2, 3]

    def test_bfs_with_multiple_paths(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_node(4)
        gr.add_edge((1, 3))
        gr.add_edge((2, 4))
        gr.add_edge((3, 2))
        gr.add_edge((1, 4))
        path = breadth_first_search(gr, 1, 4)
        print(gr)
        print(path)
        assert path == [1, 4]

    def test_bfs_paths_in_graph_without_edges(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        paths = breadth_first_paths(gr, 1, 2)
        assert paths == []

    def test_bfs_paths_in_graph_with_single_path(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((2, 3))
        paths = breadth_first_paths(gr, 1, 3)
        assert paths == [[1, 2, 3]]
        paths = breadth_first_paths(gr, 3, 1)
        assert paths == [[3, 2, 1]]

    def test_bfs_paths_in_graph_with_multi_path(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((2, 3))
        gr.add_edge((1, 3))
        paths = breadth_first_paths(gr, 1, 3)
        assert paths == [[1, 3], [1, 2, 3]]
        paths = breadth_first_paths(gr, 3, 1)
        assert paths == [[3, 1], [3, 2, 1]]

    def test_bfs_non_existent_start_node_in_digraph(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        try:
            breadth_first_paths(gr, 3, 1)
        except NodeNotFoundError:
            pass
        else:
            self.fail()

    def test_bfs_non_existent_target_node_in_digraph(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        try:
            breadth_first_paths(gr, 1, 3)
        except NodeNotFoundError:
            pass
        else:
            self.fail()

    def test_bfs_paths_in_digraph_without_edges(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        paths = breadth_first_paths(gr, 1, 2)
        assert paths == []

    def test_bfs_paths_in_digraph_with_single_path(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((2, 3))
        paths = breadth_first_paths(gr, 1, 3)
        assert paths == [[1, 2, 3]]
        paths = breadth_first_paths(gr, 3, 1)
        assert paths == []

    def test_bfs_paths_in_digraph_with_multi_path(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((2, 3))
        gr.add_edge((1, 3))
        paths = breadth_first_paths(gr, 1, 3)
        assert paths == [[1, 3], [1, 2, 3]]
        paths = breadth_first_paths(gr, 3, 1)
        assert paths == []


if __name__ == "__main__":
    unittest.main()
