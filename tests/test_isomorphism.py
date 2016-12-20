from pygraph.digraph import *
from pygraph.graph import *
from pygraph.algorithms.isomorphism import *
import random
import unittest


class TestIso(unittest.TestCase):
    def test_for_gr(self):
        def gen_graphs(length: int):
            gr1 = Graph('test1')
            gr2 = Graph('test2')
            lal = [x for x in range(length)]
            random.shuffle(lal)
            for i in range(length):
                gr1.add_node(str(i))
                gr2.add_node(str(lal[i]))

            for i in range(length):
                for j in range(length):
                    if i != j and random.random() < 0.3 and \
                                    (str(i), str(j)) not in gr1.edges():
                        gr1.add_edge((str(i), str(j)))
                        gr2.add_edge((str(lal[i]), str(lal[j])))

            table = dict()
            for x in range(length):
                table[str(x)] = str(lal[x])
            return gr1, gr2, table

        g1, g2, t = gen_graphs(100)

        assert isomorphism(g1, g2) == t

    def test_for_digr(self):
        def gen_graphs(length: int):
            gr1 = DiGraph('test1')
            gr2 = DiGraph('test2')
            lal = [x for x in range(length)]
            random.shuffle(lal)
            for i in range(length):
                gr1.add_node(str(i))
                gr2.add_node(str(lal[i]))

            for i in range(length):
                for j in range(length):
                    if i != j and random.random() < 0.3 and \
                                    (str(i), str(j)) not in gr1.edges():
                        gr1.add_edge((str(i), str(j)))
                        gr2.add_edge((str(lal[i]), str(lal[j])))

            table = dict()
            for x in range(length):
                table[str(x)] = str(lal[x])
            return gr1, gr2, table

        g1, g2, t = gen_graphs(100)

        assert isomorphism(g1, g2) == t

if __name__ == "__main__":
    unittest.main()
