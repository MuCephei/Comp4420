from Generate import Graph
from christofides import christofides_alg
import copy
from sets import Set

def cyclic_routing(graph):
    christofides_route = christofides_alg(graph)
    edges = graph.all_edges
    tour = []
    to_visit = [Set()]
    s = 0
    m = 1
    best_path = [[]]
    current_node = s
    path = []
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
            path = shortcut(direction, best_path[m], tour[start_index:] + tour[:start_index], to_visit, m, edges, path)
            if to_visit[m+1] is to_visit[m]:
                print("Here")
                path = shortcut(not direction, best_path[m], tour[start_index:] + tour[:start_index], to_visit, m, edges, path)
        else:
            direction = not direction
            path = shortcut(direction, best_path[m], tour[start_index:] + tour[:start_index], to_visit, m, edges, path)
        current_node = path[-1][1]
        m = m + 1
    #now return to s
    if edges[current_node][s]:
        path = path + [(current_node, s)]
    #else:
        #find path home
    return path

def shortcut(direction, best_path, _full_path, to_visit, m, edges, path):
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
            path = path + [(vi, vj)]
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
                path = path + [(vi, vl), (vl, vj)]
                i = j
                j = j + 1
            else:
                j = j + 1
    return path























