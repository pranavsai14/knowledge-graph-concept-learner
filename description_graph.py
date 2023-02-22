from rdflib import Graph, URIRef
from rdflib.util import guess_format
from collections import defaultdict
from description_tree import DescriptionTree

RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_THING = URIRef("http://www.w3.org/2002/07/owl#thing")


class DescriptionGraph:
    def __init__(self, URI):
        """ creates a graph from a given URI """
        self.graph = Graph()
        self.graph.parse(URI, format=guess_format(URI))

    def unravel(self, node, depth):
        """ Unravels the RDF-Graph at the given node until the given depth. """
        labels = set()
        edges = defaultdict(set)

        if depth == 0:
            for object in self.graph.objects(node, RDF_TYPE, unique=True):
                labels.add(object)
            labels.add(OWL_THING)
            return DescriptionTree(self, labels, edges)
        else:
            for predicate, object in self.graph.predicate_objects(node, unique=True):
                if predicate == RDF_TYPE:
                    labels.add(object)
                else:
                    edges[predicate].add(self.unravel(object, depth - 1))
            labels.add(OWL_THING)
            return DescriptionTree(self, labels, edges)
