import unittest
from pygraph.readwrite import read, write
from tests.graph_generator import new_graph, new_digraph


def graph_equality(gr1, gr2):
    for each in gr1.nodes():
        assert each in gr2.nodes()
    for each in gr2.nodes():
        assert each in gr1.nodes()
    for each in gr1.edges():
        assert each in gr2.edges()
    for each in gr2.edges():
        assert each in gr1.edges()


class TestReadWrite(unittest.TestCase):
    def test_dot_for_graph(self):
        gr = new_graph(25, 120)
        dotstr = write(gr)
        gr1 = read(dotstr)
        dotstr = write(gr1)
        gr2 = read(dotstr)
        graph_equality(gr1, gr2)
        assert len(gr.nodes()) == len(gr1.nodes())
        assert len(gr.edges()) == len(gr1.edges())

    def test_dot_for_digraph(self):
        gr = new_digraph(25, 120)
        dotstr = write(gr)
        gr1 = read(dotstr)
        dotstr = write(gr1)
        gr2 = read(dotstr)
        graph_equality(gr1, gr2)
        assert len(gr.nodes()) == len(gr1.nodes())
        assert len(gr.edges()) == len(gr1.edges())

    def test_output_names_in_dot(self):
        gr1 = new_graph(25, 120)
        gr1.name = "TestGraph"
        gr2 = new_digraph(25, 120)
        gr2.name = "TestDiGraph"
        assert "TestGraph" in write(gr1)
        assert "TestDiGraph" in write(gr2)


if __name__ == "__main__":
    unittest.main()
