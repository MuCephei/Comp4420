"""Implementation of Christofides Algorithm."""
import sys

from Generate import Edge


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

    circuit = make_eulerian_circuit(graph, multigraph)

    result = skip_repeated_vertices(graph, circuit)

    print(result)


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
    """Eulerian circuit generator a la Hierholzer's alg."""
    vertices_in_tour = []
    tour_edges = []
    circuit = []

    def find_vertex_with_edges_not_in_tour():
        found = False
        result_vertex = -1
        result_edge = -1

        for n in range(len(vertices_in_tour)):
            if(vertices_in_tour[n]):
                for m in range(len(edges)):
                    if (
                        (edges[m].a == n or edges[m].b == n) and
                        not tour_edges[m]
                    ):
                        found = True
                        result_vertex = n
                        result_edge = m
                        break

                if found:
                    break
        return result_vertex, result_edge

    def find_incident_unused_edge():
        result = -1

        for n in range(len(edges)):
            if (
                (not tour_edges[n]) and
                (edges[n].a == curr_vertex or edges[n].b == curr_vertex)
            ):
                result = n
                break

        return result

    for i in range(len(tour_edges)):
        tour_edges.append(False)

    for i in range(len(graph.vertices)):
        vertices_in_tour.append(False)

    vertices_in_tour[i] = True

    while len(circuit) < len(edges):
        start, edge_to_follow = find_vertex_with_edges_not_in_tour()
        if start == -1:
            print("Could not find vertex with unused edge.")
            sys.exit()

        circuit.append(edges[edge_to_follow])
        if edge_to_follow.a != start:
            curr_vertex = edges[edge_to_follow].a
        else:
            curr_vertex = edges[edge_to_follow].b
        tour_edges[edge_to_follow] = True
        vertices_in_tour[curr_vertex] = True

        while curr_vertex != start:
            edge_to_follow = find_incident_unused_edge()
            if edge_to_follow == -1:
                print("Could not find unused edge on given vertex.")
                sys.exit()

            if edge_to_follow.a != start:
                curr_vertex = edges[edge_to_follow].a
            else:
                curr_vertex = edges[edge_to_follow].b
            circuit.append(edges[edge_to_follow])
            tour_edges[edge_to_follow] = True
            vertices_in_tour[curr_vertex] = True

    return circuit


def skip_repeated_vertices(graph, circuit):
    vertices_visited = []
    result = []

    for i in range(len(graph.vertices)):
        vertices_visited.append(False)

    result.append(circuit[0])
    vertices_visited[circuit[0].a] = True

    for i in range(1, len(circuit)):
        curr_edge = circuit[i]
        if vertices_visited[curr_edge.a]:
            prev_edge = result.pop()
            skip_edge = Edge(prev_edge.a, curr_edge.b)
            result.append(skip_edge)
        else:
            result.append(curr_edge)
        vertices_visited[curr_edge.a] = True

    return result
