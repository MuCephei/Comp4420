from Generate import Graph
from christofides import christofides_alg
import copy
from sets import Set

def cyclic_routing(graph):
    edges = graph.all_edges
    vertices = [[],[]]
    tour = []
    for point in christofides_alg(graph):
        vertices[0].append(point.b)
        vertices[1].append(point.b)
    path = []
    s = 0
    m = 1
    vertices[m].remove(vertices[0][s])
    p = [0]
    direction = True
    while len(vertices[m]) > 1:
        shortcut_path = []
        for i in range(len(vertices[m])):
            shortcut_path.append(vertices[m][i])
        p.append(shortcut_path)
        if m == 1 or vertices[m][0] == vertices[m-1][len(vertices[m-1]) - 1]:
            path = shortcut(direction, m, vertices, edges, path, vertices[0])
            if vertices[m+1] == vertices[m]:
                #if nothing happened
                path = shortcut(not direction, m, vertices, edges, path, vertices[0])
        else:
            direction = not direction
            path = shortcut(direction, m, vertices, edges, path, vertices[0])
        m += 1
    return path

def shortcut(direction, m, vertices, edges, path, all_vertices):
    #foreward direction is true, backwards is false
    if not direction:
        vertices[m] = vertices[m][::-1]
    i = 0
    j = 1
    e = Set()
    vertices.append(copy.deepcopy(vertices[m]))
    while j < len(vertices[m]):
        mj = _get_index(vertices[m][j], all_vertices)
        mi = _get_index(vertices[m][i], all_vertices)
        ij_min = min(mi, mj)
        ij_max = max(mi,mj)
        if edges[ij_max][ij_min]:
            vertices[m+1].remove(vertices[m][j])
            path = path + [(mi, mj)]
            i = j
            j = i + 1
        else:
            e.add(((mj, mi)))
            l = mi + 1
            li_min = min(l, mi)
            li_max = max(l, mi)
            lj_min = min(l, mj)
            lj_max = max(l, mj)
            while all_vertices[l] != vertices[m][j] and (not edges[li_max][li_min] or not edges[lj_max][lj_min]):
                if not edges[li_max][li_min]:
                    e.add((l, mi))
                if not edges[lj_max][lj_min]:
                    e.add((mj, l))
                l = l + 1
                li_min = min(l, mi)
                li_max = max(l, mi)
                lj_min = min(l, mj)
                lj_max = max(l, mj)
            if all_vertices[l] == vertices[m][j]:
                vertices[m+1].remove(vertices[m][j])
                path = path + [(mi, l), (l, mj)]
                i = j
                j = i + 1
            else:
                j = j + 1
    return path

def _get_index(vertex, all_vertices):
    return all_vertices.index(vertex)