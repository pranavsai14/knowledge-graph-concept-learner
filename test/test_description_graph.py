import sys
from rdflib import Graph, URIRef

sys.path.append('C:/Users/prana/Desktop/Masters Thesis/')
from description_graph import DescriptionGraph


class TestDescriptionGraph:

    def test_unravel(self):
        base_URI = "http://example.org/"
        x1 = URIRef(base_URI + "x1")
        y1 = URIRef(base_URI + "y1")
        z1 = URIRef(base_URI + "z1")

        x2 = URIRef(base_URI + "x2")
        y2 = URIRef(base_URI + "y2")
        z2 = URIRef(base_URI + "z2")

        dg = DescriptionGraph("C:/Users/prana/Desktop/Masters Thesis/test_files/example-product-1.ttl")
        depth = 2
        dt = dg.unravel(x1, depth)
        dt = dt.to_str()
        return dt


result = TestDescriptionGraph()
print(result.test_unravel())
assert True
