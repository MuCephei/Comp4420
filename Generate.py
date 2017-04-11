import random
import math
from sets import Set


class Graph:
    max_x = 100
    max_y = 100

    # Note that Vertices are [Y coords, X coords]
    def __init__(self, number_of_vertices, number_to_remove):
        self.number_of_vertices = number_of_vertices
        self.number_of_broken_edges = number_to_remove

        self.vertices = [[random.random() * Graph.max_y, random.random() * Graph.max_x] for n in range(self.number_of_vertices)]
        self.all_edges = remove_edges(self.number_of_broken_edges, self.number_of_vertices)

    def distance(self, a, b):
        return math.sqrt((a[1] - b[1])**2 + (a[0] - b[0])**2)

    def __str__(self):
        print(self.vertices)
        print(self.all_edges)
        return ""


class Edge:
    """A connection from the vertex at index a, to the vertex at index b."""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return str(self.a) + " - " + str(self.b)

    __repr__ = __str__


# TODO: We might want to copmute the distances between all edges only onece.
def get_min_connecting_edge(graph, vertices):
    minDistance = -1
    minEdge = None

    for i in range(len(vertices)):
        if vertices[i]:  # If the vertex is in our tree do:
            for j in range(len(graph.vertices)):
                if not vertices[j]:  # If the vertex is not in our tree:
                    distance = graph.distance(graph.vertices[i], graph.vertices[j])
                    if (minDistance == -1) or (distance < minDistance):
                        minDistance = distance
                        minEdge = Edge(i, j)

    return minEdge


def get_min_spanning_tree(graph):
    vertices = []
    edges = []

    if len(graph.vertices) > 0:
        for i in range(len(graph.vertices)):
            vertices.append(False)

        vertices[0] = True  # Pick and arbitrary vertex and add it to the tree

        for i in range(len(graph.vertices) - 1):
            minEdge = get_min_connecting_edge(graph, vertices)
            if minEdge is not None:
                edges.append(minEdge)
                vertices[minEdge.b] = True
            else:
                print("get_min_cennecting_edge returned nothing!")

    return edges


def is_edge_safe_to_remove(edge, edges, edges_as_matrix, size):
    if edges_as_matrix[edge[0]][edge[1]] == 1:
        vertices = Set()
        new_vertices = Set([0])
        newer_vertices = Set()
        edges_as_matrix[edge[0]][edge[1]] = 0
        while len(new_vertices) > 0:
            vertices = vertices.union(new_vertices)
            newer_vertices.clear()
            for v in new_vertices:
                for x in range(v):
                    if x not in vertices and x not in newer_vertices:
                        if edges_as_matrix[v][x] == 1:
                            newer_vertices.add(x)
                for y in range(v, size):
                    if y not in vertices and y not in newer_vertices:
                        if edges_as_matrix[y][v] == 1:
                            newer_vertices.add(y)
            new_vertices = newer_vertices.copy()
            newer_vertices.clear()

        edges_as_matrix[edge[0]][edge[1]] = 1
        return len(vertices) == size
    else:
        return False


def remove_edges(number_to_remove, number_of_vertices):
    all_edges = [(m, n) for m in range(number_of_vertices) for n in range(m)]
    edges_as_matrix = [[1 for n in range(m)] for m in range(number_of_vertices)]
    for removal in range(number_to_remove):
        edge = random.choice(all_edges)
        while not is_edge_safe_to_remove(edge, all_edges, edges_as_matrix, number_of_vertices):
            edge = random.choice(all_edges)
        all_edges.remove(edge)
        edges_as_matrix[edge[0]][edge[1]] = 0
    return edges_as_matrix


graph = Graph(5, 6)
print(graph)

print(get_min_spanning_tree(graph))
