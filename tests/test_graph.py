import unittest
from copy import deepcopy

from pygraph.graph import Graph
from pygraph.exceptions import AdditionError

from tests.graph_generator import new_graph


class TestGraph(unittest.TestCase):
    def test_raise_exception_on_duplicate_node_addition(self):
        gr = Graph("TestGraph")
        gr.add_node("first_node")
        try:
            gr.add_node("first_node")
        except AdditionError:
            pass
        else:
            self.fail()

    def test_raise_exception_on_duplicate_edge_addition(self):
        gr = Graph("TestGraph")
        gr.add_node("a_node")
        gr.add_node("other_node")
        gr.add_edge(("a_node", "other_node"))
        try:
            gr.add_edge(("a_node", "other_node"))
        except AdditionError:
            pass
        else:
            self.fail()

    def test_raise_exception_when_edge_added_from_non_existing_node(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_node("1")
        try:
            gr.add_edge(("3", "0"))
        except KeyError:
            pass
        else:
            self.fail()
        assert gr._neighbors == {"0": [], "1": []}

    def test_raise_exception_when_edge_added_to_non_existing_node(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_node("1")
        try:
            gr.add_edge(("0", "3"))
        except KeyError:
            pass
        else:
            self.fail()
        assert gr._neighbors == {"0": [], "1": []}

    def test_node_degree(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_node("3")

        gr.add_edge(("0", "0"))
        gr.add_edge(("0", "1"))
        gr.add_edge(("0", "2"))
        gr.add_edge(("0", "3"))

        assert gr.node_degree("0") == 4

    def test_remove_node(self):
        gr = new_graph(25, 120)
        gr.del_node("0")
        self.assertTrue("0" not in gr)
        for each, other in gr.edges():
            self.assertTrue(each in gr)
            self.assertTrue(other in gr)

    def test_remove_edge_from_node_to_same_node(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_edge(("0", "0"))
        gr.del_edge(("0", "0"))

    def test_remove_node_with_edge_to_itself(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_edge(("0", "0"))
        gr.del_node("0")

    def test_edges_between_different_nodes_should_be_arrows_in_both_ways(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_node("1")
        gr.add_edge(("0", "1"), label="label", attrs={"key": "value"})
        assert ("0", "1") in gr.edges()
        assert ("1", "0") in gr.edges()
        assert len(gr.edges()) == 2
        assert gr.neighbors("0") == ["1"]
        assert gr.neighbors("1") == ["0"]
        assert ("0", "1") in gr._edges_attrs
        assert ("1", "0") in gr._edges_attrs

    def test_edges_between_same_nodes_should_be_a_single_arrow(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_edge(("0", "0"), label="label", attrs={"key": "value"})
        assert ("0", "0") in gr.edges()
        assert len(gr.edges()) == 1
        assert gr.neighbors("0") == ["0"]
        assert ("0", "0") in gr._edges_attrs
        assert len(gr._edges_attrs[("0", "0")]) == 3

    def test_invert_graph(self):
        gr = new_graph(25, 120)
        inv = gr.inverse()
        for each in gr.edges():
            self.assertTrue(each not in inv.edges())
        for each in inv.edges():
            self.assertTrue(each not in gr.edges())

    def test_invert_empty_graph(self):
        gr = Graph("TestGraph")
        inv = gr.inverse()
        self.assertTrue(gr.edges() == [])
        self.assertTrue(inv.nodes() == [])

    def test_complete_graph(self):
        gr = Graph("TestGraph")
        for i in range(10):
            gr.add_node(str(i))
        gr.complete()
        for i in range(10):
            for j in range(10):
                self.assertTrue((str(i), str(j)) in gr.edges() or i == j)

    def test_complete_empty_graph(self):
        gr = Graph("TestGraph")
        gr.complete()
        self.assertTrue(gr.nodes() == [])
        self.assertTrue(gr.edges() == [])

    def test_complete_graph_with_one_node(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.complete()
        self.assertTrue(gr.nodes() == ["0"])
        self.assertTrue(gr.edges() == [])

    def test_reverse_digraph(self):
        gr = new_graph(25, 120)
        rev = gr.reverse()
        for (u, v) in gr.edges():
            self.assertTrue((v, u) in rev.edges())
        for (u, v) in rev.edges():
            self.assertTrue((v, u) in gr.edges())

    def test_reverse_empty_digraph(self):
        gr = Graph("TestDiGraph")
        rev = gr.reverse()
        self.assertTrue(rev.nodes() == [])
        self.assertTrue(rev.edges() == [])

    def test_repr(self):
        gr = new_graph(25, 120)
        gr_repr = repr(gr)
        assert isinstance(gr_repr, str)
        assert gr.__class__.__name__ in gr_repr

    def test_order_len_equivalence(self):
        gr = new_graph(25, 120)
        assert len(gr) == gr.order()
        assert gr.order() == len(gr.nodes())

    def test_graph_equality_nodes(self):
        gr = Graph("TestGraph")
        for i in range(6):
            gr.add_node(str(i))

        gr2 = deepcopy(gr)

        gr3 = deepcopy(gr)
        gr3.del_node("5")

        gr4 = deepcopy(gr)
        gr4.add_node("6")
        gr4.del_node("0")

        assert gr == gr2
        assert gr2 == gr
        assert gr != gr3
        assert gr3 != gr
        assert gr != gr4
        assert gr4 != gr

    def test_graph_equality_edges(self):
        gr = Graph("TestGraph")
        for i in range(5):
            gr.add_node(str(i))
        gr.add_edge(("0", "1"), weight=1)
        gr.add_edge(("0", "2"), weight=2)
        gr.add_edge(("1", "2"), weight=3)
        gr.add_edge(("3", "4"), weight=4)

        gr2 = deepcopy(gr)

        gr3 = deepcopy(gr)
        gr3.del_edge(("0", "2"))

        gr4 = deepcopy(gr)
        gr4.add_edge(("2", "4"))

        gr5 = deepcopy(gr)
        gr5.del_edge(("0", "2"))
        gr5.add_edge(("2", "4"))

        gr6 = deepcopy(gr)
        gr6.del_edge(("0", "2"))
        gr6.add_edge(("0", "2"), weight=10)

        assert gr == gr2
        assert gr2 == gr
        assert gr != gr3
        assert gr3 != gr
        assert gr != gr4
        assert gr4 != gr
        assert gr != gr5
        assert gr5 != gr
        assert gr != gr6
        assert gr6 != gr

    def test_graph_equality_labels(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_edge(("0", "1"), label="l1")
        gr.add_edge(("1", "2"), label="l2")

        gr2 = deepcopy(gr)

        gr3 = deepcopy(gr)
        gr3.del_edge(("0", "1"))
        gr3.add_edge(("0", "1"))

        gr4 = deepcopy(gr)
        gr4.del_edge(("0", "1"))
        gr4.add_edge(("0", "1"), label="l3")

        assert gr == gr2
        assert gr2 == gr
        assert gr != gr3
        assert gr3 != gr
        assert gr != gr4
        assert gr4 != gr

    def test_graph_equality_attributes(self):
        gr = Graph("TestGraph")
        gr.add_node("0")
        gr.add_node("1")
        gr.add_node("2")
        gr.add_edge(("0", "1"))
        gr.add_node_attribute("1", "a", "x")
        gr.add_node_attribute("2", "b", "y")
        gr.add_edge_attribute(("0", "1"), "c", "z")

        gr2 = deepcopy(gr)

        gr3 = deepcopy(gr)
        gr3.del_edge(("0", "1"))
        gr3.add_edge(("0", "1"))

        gr4 = deepcopy(gr)
        gr4.del_edge(("0", "1"))
        gr4.add_edge(("0", "1"))
        gr4.add_edge_attribute(("0", "1"), "d", "k")

        gr5 = deepcopy(gr)
        gr5.del_node("2")
        gr5.add_node("2")
        gr5.add_node_attribute(0, "d", "k")

        assert gr == gr2
        assert gr2 == gr
        assert gr != gr3
        assert gr3 != gr
        assert gr != gr4
        assert gr4 != gr
        assert gr != gr5
        assert gr5 != gr

    def test_graph_equality(self):
        gr = Graph("TestGraph")
        gr.add_node("2")
        gr.add_node("4")
        gr.add_node("3")
        gr.add_edge(("3", "4"))

        gr1 = Graph("TestGraph")
        gr1.add_node("2")
        gr1.add_node("3")
        gr1.add_node("4")
        gr1.add_edge(("4", "3"))

        assert gr == gr1


if __name__ == "__main__":
    unittest.main()
