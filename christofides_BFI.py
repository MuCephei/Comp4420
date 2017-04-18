from christofides import christofides_alg
from Generate import Edge
import BFI
import copy
from sets import Set

def christofides_BFI(graph):
    #Do not use this right now, it's not quite a solution to the problem we are facing
    christofides_route = christofides_alg(graph)
    edges = [[0 for n in range(m)] for m in range(len(graph.vertices))]
    total_distance = 0
    path = []
    to_visit = []
    for point in christofides_route:
        to_visit.append(point.a)
    s = 0
    finished = False
    seen = Set()
    seen.add(s)
    current_node = s
    while len(to_visit):
        target_node = to_visit[0]
        for x in range(current_node):
            if graph.all_edges[current_node][x] == 1 and x not in seen:
                seen.add(x)
                edges[current_node][x] = 1
        for y in range(current_node + 1, len(christofides_route)):
            if graph.all_edges[y][current_node] == 1 and y not in seen:
                seen.add(y)
                edges[y][current_node] = 1
        if target_node in seen:
            shortest_route, distance = BFI.find_shortest_path(graph, edges, current_node, target_node)
            path = path + shortest_route
            current_node = target_node
            to_visit.pop(0)
        else:
            to_visit.append(to_visit.pop(0))
        if not len(to_visit) and not finished:
            to_visit.append(s)
            finished = True
    distance = 0
    vertices = graph.vertices
    for edge in path:
        distance = distance + graph.distance(vertices[edge.a], vertices[edge.b])
    return path, distance
