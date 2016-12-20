import unittest
from pygraph.graph import Graph
from pygraph.digraph import DiGraph
from pygraph.algorithms.check_connectivity import check_graph_is_connected


class ConnectivityTest(unittest.TestCase):
    def test_graph_connectivity_connected(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_edge(("0", "1"))
        gr.add_edge(("1", "2"))
        gr.add_edge(("0", "2"))
        assert check_graph_is_connected(gr)

    def test_graph_connectivity_disconnected(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_node("3")
        gr.add_edge(("0", "1"))
        gr.add_edge(("1", "2"))
        gr.add_edge(("0", "2"))
        assert not check_graph_is_connected(gr)

    def test_digraph_connectivity_connected(self):
        gr = DiGraph("TestGraph")
        gr.add_node("0")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_edge(("0", "1"))
        gr.add_edge(("1", "2"))
        gr.add_edge(("2", "0"))
        assert check_graph_is_connected(gr)

    def test_digraph_connectivity_disconnected(self):
        gr = DiGraph("TestGraph")
        gr.add_node("0")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_edge(("0", "1"))
        gr.add_edge(("1", "2"))
        gr.add_edge(("0", "2"))
        assert not check_graph_is_connected(gr)
