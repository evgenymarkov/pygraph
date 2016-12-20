import unittest
from pygraph.graph import Graph
from pygraph.digraph import DiGraph
from pygraph.algorithms.dfs import depth_first_bypass, depth_first_search, depth_first_paths


class TestDFS(unittest.TestCase):
    def test_dfs_bypass_in_graph_path_exists(self):
        gr = Graph("TestGraph")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_node("3")
        gr.add_node("4")
        gr.add_edge(("1", "2"))
        gr.add_edge(("1", "3"))
        gr.add_edge(("2", "4"))
        bypassed_nodes = depth_first_bypass(gr, "1")
        assert bypassed_nodes == ["1", "3", "2", "4"] or bypassed_nodes == ["1", "2", "4", "3"]

    def test_dfs_bypass_in_graph_path_not_exists(self):
        gr = Graph("TestGraph")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_node("3")
        gr.add_node("4")
        gr.add_edge(("1", "2"))
        gr.add_edge(("1", "3"))
        bypassed_nodes = depth_first_bypass(gr, "4")
        assert bypassed_nodes == ["4"]

    def test_dfs_search_in_graph_path_exists(self):
        gr = Graph("TestGraph")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_node("3")
        gr.add_node("4")
        gr.add_node("5")
        gr.add_edge(("1", "1"))
        gr.add_edge(("2", "2"))
        gr.add_edge(("1", "2"))
        gr.add_edge(("1", "3"))
        gr.add_edge(("1", "4"))
        gr.add_edge(("4", "5"))
        gr.add_edge(("2", "5"))
        gr.add_edge(("3", "5"))
        path = depth_first_search(gr, "1", "5")
        assert path == ["1", "2", "5"] or path == ["1", "3", "5"] or path == ["1", "4", "5"]

    def test_dfs_search_in_graph_node_unreachable(self):
        gr = Graph("TestGraph")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_node("3")
        gr.add_node("4")
        gr.add_node("5")
        gr.add_edge(("1", "1"))
        gr.add_edge(("2", "2"))
        gr.add_edge(("1", "2"))
        gr.add_edge(("1", "3"))
        gr.add_edge(("1", "4"))
        gr.add_edge(("4", "3"))
        gr.add_edge(("2", "4"))
        path = depth_first_search(gr, "1", "5")
        assert path is None

    def test_dfs_paths_in_graph(self):
        gr = Graph("TestGraph")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_node("3")
        gr.add_node("4")
        gr.add_node("5")
        gr.add_edge(("1", "1"))
        gr.add_edge(("2", "2"))
        gr.add_edge(("1", "2"))
        gr.add_edge(("1", "3"))
        gr.add_edge(("1", "4"))
        gr.add_edge(("4", "5"))
        gr.add_edge(("2", "5"))
        gr.add_edge(("3", "5"))
        gr.add_edge(("1", "5"))
        paths = depth_first_paths(gr, "1", "5")
        assert ["1", "5"] in paths and \
               ["1", "2", "5"] in paths and \
               ["1", "3", "5"] in paths and \
               ["1", "4", "5"] in paths

    def test_dfs_bypass_in_digraph_path_exists(self):
        gr = DiGraph("TestGraph")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_node("3")
        gr.add_node("4")
        gr.add_edge(("1", "1"))
        gr.add_edge(("1", "4"))
        gr.add_edge(("4", "2"))
        gr.add_edge(("2", "4"))
        gr.add_edge(("2", "3"))
        bypassed_nodes = depth_first_bypass(gr, "1")
        assert bypassed_nodes == ["1", "4", "2", "3"]

    def test_dfs_bypass_in_digraph_path_not_exists(self):
        gr = DiGraph("TestGraph")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_node("3")
        gr.add_node("4")
        gr.add_edge(("1", "2"))
        gr.add_edge(("1", "3"))
        gr.add_edge(("2", "4"))
        gr.add_edge(("4", "4"))
        gr.add_edge(("4", "2"))
        bypassed_nodes = depth_first_bypass(gr, "4")
        assert bypassed_nodes == ["4", "2"]
