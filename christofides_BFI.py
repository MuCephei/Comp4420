from christofides import christofides_alg
from Generate import Edge
import BFI
from sets import Set

def christofides_BFI(graph):
    christofides_route = christofides_alg(graph)
    current_node = 0
    total_distance = 0
    path = []
    to_visit = Set()
    for v in range(len(graph.vertices)):
        to_visit.add(v)
    to_visit.remove(current_node)
    for edge in christofides_route:
        if edge.b in to_visit:
            shortest_route, distance = BFI.find_shortest_path(graph, current_node, edge.b)
            path = path + shortest_route
            current_node = edge.b
            for e in shortest_route:
                if e.b in to_visit:
                    to_visit.remove(e.b)
    shortest_route, distance = BFI.find_shortest_path(graph, current_node, 0)
    total_distance = total_distance + distance
    path = path + shortest_route
    distance = 0
    vertices = graph.vertices
    for edge in path:
        distance = distance + graph.distance(vertices[edge.a], vertices[edge.b])
    return path, distance
