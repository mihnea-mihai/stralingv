from graphviz import Digraph
from wikiword import WikiWord


class Etygraph:

    def __init__(self, w):
        dot = Digraph()

        dot.node('O', w.node)

        for asc, label in {'inh': 'inherited', 'bor': 'borrowed',
                           'der': 'derived'}.items():
            ascs = w.get_ascendants(asc)
            for i in range(len(ascs)):
                dot.node(asc.capitalize()+str(i), ascs[i].node)
                dot.edge(asc.capitalize()+str(i), 'O', label)

        descs = list(w.get_descendants())
        for i in range(len(descs)):
            dot.node('DESC'+str(i), descs[i].node)
            dot.edge('O', 'DESC'+str(i), 'descendant')

        dot = dot.unflatten(stagger=5)
        print(dot)
        dot.view()


Etygraph(WikiWord('see', 'en'))
