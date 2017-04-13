"""Implementation of Christofides Algorithm."""
import sys

from Generate import Graph, Edge


def christofides_alg(graph):
    min_spanning_tree = get_min_spanning_tree
    odd_vertices = find_odd_vertices(graph, min_spanning_tree)
    min_perfect_matching = find_min_perfect_matching(graph, odd_vertices)

    # standardize edges such that a < b (to make removing duplicates easier)
    for i in range(len(min_spanning_tree)):
        edge = min_spanning_tree[i]
        if(edge.a > edge.b):
            temp = edge.a
            edge.a = edge.b
            edge.b = temp

    for i in range(len(min_perfect_matching)):
        edge = min_perfect_matching[i]
        if(edge.a > edge.b):
            temp = edge.a
            edge.a = edge.b
            edge.b = temp

    multigraph = min_spanning_tree
    for i in range(len(min_perfect_matching)):
        if not duplicate_edge(multigraph, min_perfect_matching[i]):
            multigraph.append(min_perfect_matching[i])


def duplicate_edge(edges, edge):
    duplicate = False

    for i in range(len(edges)):
        if edge.a == edges[i].a and edge.b == edges[i].b:
            duplicate = True
            break
    return duplicate


# TODO: We might want to copmute the distances between all edges only once.
def get_min_connecting_edge(graph, vertices):
    minDistance = -1
    minEdge = None

    for i in range(len(vertices)):
        if vertices[i]:  # If the vertex is in our tree do:
            for j in range(len(graph.vertices)):
                if not vertices[j]:  # If the vertex is not in our tree:
                    distance = graph.distance(
                        graph.vertices[i], graph.vertices[j]
                    )
                    if (minDistance == -1) or (distance < minDistance):
                        minDistance = distance
                        minEdge = Edge(i, j)

    return minEdge


# A la Prim's algorithm
def get_min_spanning_tree(graph):
    vertices = []
    edges = []

    if len(graph.vertices) > 0:
        for i in range(len(graph.vertices)):
            vertices.append(False)

        vertices[0] = True  # Pick an arbitrary vertex and add it to the tree

        for i in range(len(graph.vertices) - 1):
            minEdge = get_min_connecting_edge(graph, vertices)
            if minEdge is not None:
                edges.append(minEdge)
                vertices[minEdge.b] = True
            else:
                print("get_min_cennecting_edge returned nothing!")

    return edges


def find_odd_vertices(graph, edges):
    vertexDegree = []
    verticesOfOddDegree = []

    for i in range(len(graph.vertices)):
        vertexDegree.append(0)

    for i in range(len(edges)):
        vertexDegree[edges[i].a] += 1
        vertexDegree[edges[i].b] += 1

    for i in range(len(vertexDegree)):
        if vertexDegree[i] % 2 == 1:
            verticesOfOddDegree.append[i]

    return verticesOfOddDegree


# Important: assumes an edge exists between any two nodes.
def find_min_perfect_matching(graph, vertices):
    matchedVertices = []
    matching = []

    def find_min_weight_match():
        minDistance = -1
        result1 = None
        result2 = None

        for first in range(len(vertices)):
            if not matchedVertices[first]:
                for second in range(len(vertices)):
                    if (not matchedVertices[second]) and first != second:
                        distance = graph.distance(
                            graph.vertices[vertices[first]],
                            graph.vertices[vertices[second]]
                        )
                        if minDistance == -1 or distance < minDistance:
                            minDistance = distance
                            result1 = first
                            result2 = second

        return result1, result2

    for i in range(len(vertices)):
        matchedVertices.append(False)

    for i in range(len(vertices) / 2):
        vertex1, vertex2 = find_min_weight_match()
        matchedVertices[vertex1] = True
        matchedVertices[vertex2] = True
        newEdge = Edge(vertices[vertex1], vertices[vertex2])
        matching.append(newEdge)

    return matching


def make_eulerian_circuit(graph, edges):
    verticesInTour = []
    edgesInTour = []
    circuit = []

    def find_vertex_with_edges_not_in_tour():
        found = False
        resultVertex = -1
        resultEdge = -1

        for n in range(len(verticesInTour)):
            if(verticesInTour[n]):
                for m in range(len(edges)):
                    if (
                        (edges[m].a == n or edges[m].b == n) and
                        not edgesInTour[m]
                    ):
                        found = True
                        resultVertex = n
                        resultEdge = m
                        break

                if found:
                    break
        return resultVertex, resultEdge

    for i in range(len(edgesInTour)):
        edgesInTour.append(False)

    for i in range(len(graph.vertices)):
        verticesInTour.append(False)

    verticesInTour[i] = True

    while len(circuit) < len(edges):
        start, edgeToFollow = find_vertex_with_edges_not_in_tour()
        if start == -1:
            print("Could not find vertex with unused edge.")
            sys.exit()

        circuit.append(edgeToFollow)

