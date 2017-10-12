import random
import math
import copy

class Graph:
    max_x = 100
    max_y = 100

    # Note that Vertices are [Y coords, X coords]
    def __init__(self, number_of_vertices, number_of_edges, vertices=None):
        self.n = number_of_vertices
        self.e = number_of_edges

        if vertices:
            self.vertices = vertices
        else:
            self.vertices = [[random.random() * Graph.max_y, random.random() * Graph.max_x] for n in range(self.n)]

        self.edges = self.create_edges()

    def distance(self, a, b):
        return math.sqrt((a[1] - b[1])**2 + (a[0] - b[0])**2)

    def __str__(self):
        return str(self.vertices) + '\n' + str(self.edges)

    def create_edges(self):
        unused_edges = set(sum(map(lambda b: [Edge(a, b) for a in range(b + 1, self.n)], range(self.n)), []))
        edge_set = set()
        #first connect the unconnected edges
        for node in range(1, self.n):
            rand = random.randint(0, node - 1)
            a = max(rand, node)
            b = min(rand, node)
            new_edge = Edge(a, b)
            edge_set.add(new_edge)
            unused_edges.remove(new_edge)

        while len(edge_set) < self.e:
            new_edge = random.sample(unused_edges, 1)[0]
            edge_set.add(new_edge)
            unused_edges.remove(new_edge)

        edges = [[0] * m for m in range(self.n)]

        for e in edge_set:
            edges[e.a][e.b] = 1

        return edges

    def copy(self, number_of_edges):
        graph_copy = Graph(self.n, number_of_edges, self.vertices)

        return graph_copy


class Edge:
    """A connection from the vertex at index a, to the vertex at index b."""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return str(self.a) + " - " + str(self.b)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash(self.__str__())

    __repr__ = __str__
