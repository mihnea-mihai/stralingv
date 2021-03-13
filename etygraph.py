from graphviz import Digraph
from wikiword import WikiWord
from pprint import pprint

class EtyGraph:


    def __init__(self, wset):
        self.dot = Digraph(
            graph_attr={
                'rankdir': 'LR',
                'nodesep': f'{str(0.2)}',
                'ranksep': f'{str(0.2)}',
            },
            node_attr={
                'shape': 'none',
                },
            engine='dot',
            )
        for w in wset:
            alldescs = w.get_all_descendants()
            allascs = w.get_all_ascendants()
            self.add_nodes(w, alldescs)
            self.add_nodes(w, allascs, '<')
            self.dot.node(w.node, shape='box')
            WikiWord.history = set()
        self.dot = self.dot.unflatten(stagger=5, fanout=True)
        self.dot.format = 'svg'
        self.dot.save(' '.join(str(w) for w in wset), 'demos')
        self.dot.view()
    
    def add_nodes(self, branch, leaves, direction='>'):
        self.dot.node(branch.node)
        for leaf in leaves:
            self.dot.node(leaf.node, url=leaf.url)
            if direction == '>':
                self.dot.edge(branch.node, leaf.node)
            else:
                self.dot.edge(leaf.node, branch.node)
            self.add_nodes(leaf, leaves[leaf], direction)



EtyGraph({
    WikiWord('*ḱer-', 'ine-pro'),
    })