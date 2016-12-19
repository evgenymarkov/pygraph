import unittest
from pygraph.graph import Graph
from pygraph.digraph import DiGraph
from pygraph.algorithms.bfs import breadth_first_search
from pygraph.exceptions import NodeNotFoundError


class TestBFS(unittest.TestCase):
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

    def test_bfs_in_graph_without_edges(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        paths = breadth_first_search(gr, 1, 2)
        assert paths == []

    def test_bfs_in_graph_with_single_path(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((2, 3))
        paths = breadth_first_search(gr, 1, 3)
        assert paths == [[1, 2, 3]]
        paths = breadth_first_search(gr, 3, 1)
        assert paths == [[3, 2, 1]]

    def test_bfs_in_graph_with_multi_path(self):
        gr = Graph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((2, 3))
        gr.add_edge((1, 3))
        paths = breadth_first_search(gr, 1, 3)
        assert paths == [[1, 3], [1, 2, 3]]
        paths = breadth_first_search(gr, 3, 1)
        assert paths == [[3, 1], [3, 2, 1]]

    def test_bfs_non_existent_start_node_in_digraph(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        try:
            breadth_first_search(gr, 3, 1)
        except NodeNotFoundError:
            pass
        else:
            self.fail()

    def test_bfs_non_existent_target_node_in_digraph(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        try:
            breadth_first_search(gr, 1, 3)
        except NodeNotFoundError:
            pass
        else:
            self.fail()

    def test_bfs_in_digraph_without_edges(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        paths = breadth_first_search(gr, 1, 2)
        assert paths == []

    def test_bfs_in_digraph_with_single_path(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((2, 3))
        paths = breadth_first_search(gr, 1, 3)
        assert paths == [[1, 2, 3]]
        paths = breadth_first_search(gr, 3, 1)
        assert paths == []

    def test_bfs_in_digraph_with_multi_path(self):
        gr = DiGraph("TestGraph")
        gr.add_node(1)
        gr.add_node(2)
        gr.add_node(3)
        gr.add_edge((1, 2))
        gr.add_edge((2, 3))
        gr.add_edge((1, 3))
        paths = breadth_first_search(gr, 1, 3)
        assert paths == [[1, 3], [1, 2, 3]]
        paths = breadth_first_search(gr, 3, 1)
        assert paths == []


if __name__ == "__main__":
    unittest.main()
