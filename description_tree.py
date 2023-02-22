from collections import defaultdict
from functools import total_ordering
from rdflib import URIRef


RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_THING = URIRef("http://www.w3.org/2002/07/owl#thing")
OWL_NOTHING = URIRef("http://www.w3.org/2002/07/owl#nothing")


@total_ordering
class DescriptionTree:
    dts = {}

    def __new__(cls, dg, labels, edges):
        key = tuple(sorted(labels)), tuple(sorted(edges.items()))
        if key in cls.dts:
            return cls.dts[key]
        else:
            instance = super().__new__(cls)
            cls.dts[key] = instance
            return instance

    def __init__(self, dg, labels, edges):
        self.dg = dg
        self.labels = set(labels)
        self.edges = defaultdict(set, edges)

    def __lt__(self, other):
        return id(self) < id(other)

    def copy(self):
        return DescriptionTree(self.dg, self.labels, self.edges)

    def binary_product(self, t):
        labels = self.labels & t.labels
        edges = defaultdict(set)
        for e, children in self.edges.items():
            if e in t.edges:
                for c1 in children:
                    for c2 in t.edges[e]:
                        edges[e].add(c1.binary_product(c2))
        return DescriptionTree(self.dg, labels, edges)

    def product(self, trees):
        p = self.copy()
        for t in trees:
            p = p.binary_product(t)
        return p

    def print(self, n=0):
        for i in range(n):
            print("\t", end="")
        print(", ".join(l.n3(self.dg.graph.namespace_manager) for l in self.labels), end="")
        for e, children in self.edges.items():
            print()
            for i in range(n):
                print("\t", end="")
            print(f"{e.n3(self.dg.graph.namespace_manager)}.(", end="")
            for j, t in enumerate(children):
                t.print(n + 1)
                if j < len(children) - 1:
                    print(", ", end="")
            print(")", end="")

    def to_str(self):
        labels = sorted(self.labels, key=lambda l: l != OWL_THING and l != OWL_NOTHING)
        edges = sorted(self.edges.items())
        return " ⊓ ".join(
            l.n3(self.dg.graph.namespace_manager) if l not in (OWL_THING, OWL_NOTHING) else ("⊤" if l == OWL_THING else "⊥")
            for l in labels
        ) + (
            "" if not edges else " ⊓ "
            + " ⊓ ".join)
