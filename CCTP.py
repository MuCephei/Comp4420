from christofides import christofides_alg
from Generate import Edge
import copy
import BFI
from sets import Set

def cyclic_routing(graph):
    christofides_route = christofides_alg(graph)
    edges = graph.all_edges
    seen_edges = [[0 for n in range(m)] for m in range(len(graph.vertices))]
    tour = []
    to_visit = [Set()]
    s = 0
    m = 1
    num_brute = 0.0
    best_path = [[]]
    current_node = s
    path = []
    seen = Set()
    seen.add(s)
    see(s, edges, seen, seen_edges)
    direction = True
    for point in christofides_route:
        tour.append(point.a)
        to_visit[0].add(point.a)
    to_visit[0].remove(current_node)
    to_visit.append(copy.deepcopy(to_visit[0]))
    while len(to_visit[m]):
        best_path.append([])
        start_index = tour.index(current_node)
        best_path[m].append(current_node)
        for point in tour[start_index:] + tour[:start_index]:
            if point in to_visit[m]:
                best_path[m].append(point)

        if m == 1 or best_path[m][0] == best_path[m-1][len(to_visit[m-1])]:
            path = shortcut(direction, best_path[m], tour[start_index:] + tour[:start_index], to_visit, m, edges, path, seen, seen_edges)
            if len(to_visit[m+1]) == len(to_visit[m]):
                path = shortcut(not direction, best_path[m], tour[start_index:] + tour[:start_index], to_visit, m, edges, path, seen, seen_edges)
                if len(to_visit[m+1]) == len(to_visit[m]):
                    target = 1
                    while best_path[m][target] not in seen:
                        target = target + 1
                    path = brute_force(graph, seen_edges, current_node, best_path[m][1], path, to_visit, m, edges, seen)
                    num_brute = num_brute + 1
        else:
            direction = not direction
            path = shortcut(direction, best_path[m], tour[start_index:] + tour[:start_index], to_visit, m, edges, path, seen, seen_edges)
            if len(to_visit[m+1]) == len(to_visit[m]):
                target = 1
                while best_path[m][target] not in seen:
                    target = target + 1
                path = brute_force(graph, seen_edges, current_node, best_path[m][1], path, to_visit, m, edges, seen)
                num_brute = num_brute + 1
        current_node = path[-1].b
        m = m + 1
    #now return to s
    if edges[current_node][s]:
        path = path + [Edge(current_node, s)]
    else:
        to_visit[m] = Set()
        to_visit[m].add(s)
        start_index = tour.index(current_node)
        to_visit.append(copy.deepcopy(to_visit[m]))
        path = brute_force(graph, seen_edges, current_node, s, path, to_visit, m, edges, seen)
    distance = 0
    vertices = graph.vertices
    for edge in path:
        distance = distance + graph.distance(vertices[edge.a], vertices[edge.b])
    return path, distance, num_brute

def see(current_node, edges, seen, seen_edges):
        for x in range(current_node):
            if edges[current_node][x] == 1 and x not in seen:
                seen.add(x)
                seen_edges[current_node][x] = 1
        for y in range(current_node + 1, len(edges[-1]) + 1):
            if edges[y][current_node] == 1 and y not in seen:
                seen.add(y)
                seen_edges[y][current_node] = 1

def shortcut(direction, best_path, _full_path, to_visit, m, edges, path, seen, seen_edges):
    if len(to_visit) == m + 1:
        to_visit.append(copy.deepcopy(to_visit[m]))
    if not direction:
        best_path = [best_path[0]] + best_path[::-1][:-1]
        full_path = [_full_path[0]] + _full_path[::-1][:-1]
    else:
        full_path = _full_path
    i = 0
    j = 1
    while j < len(best_path):
        vi = best_path[i]
        vj = best_path[j]
        min_ij = min(vi,vj)
        max_ij = max(vi,vj)
        if edges[max_ij][min_ij]:
            to_visit[m+1].remove(vj)
            path = path + [Edge(vi, vj)]
            see(vj, edges, seen, seen_edges)
            i = j
            j = j + 1
        else:
            l = full_path.index(best_path[i]) + 1
            vl = full_path[l]
            min_li = min(vl, vi)
            max_li = max(vl, vi)
            min_lj = min(vl, vj)
            max_lj = max(vl, vj)
            while vl != vj and (not edges[max_li][min_li] or not edges[max_lj][min_lj]):
                l = l + 1
                vl = full_path[l]
                min_li = min(vl, vi)
                max_li = max(vl, vi)
                min_lj = min(vl, vj)
                max_lj = max(vl, vj)
            if vl != vj:
                to_visit[m+1].remove(vj)
                path = path + [Edge(vi, vl), Edge(vl, vj)]
                see(vj, edges, seen, seen_edges)
                i = j
                j = j + 1
            else:
                j = j + 1
    return path

def brute_force(graph, seen_edges, current_node, target_node, path, to_visit, m, edges, seen):
    shortest_route, distance = BFI.find_shortest_path(graph, seen_edges, current_node, target_node)
    path = path + shortest_route
    to_visit[m+1].remove(target_node)
    see(target_node, edges, seen, seen_edges)
    return path