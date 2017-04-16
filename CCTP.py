from Generate import Graph
from christofides import christofides_alg
import copy
from sets import Set

def cyclic_routing(graph):
    graph_edges = graph.all_edges
    edges = []
    vertices = [[],[]]
    tour = []
    christofides_route = christofides_alg(graph)
    for point in christofides_route:
        vertices[0].append(point.a)
        vertices[1].append(point.a)

    for row_index in range(len(graph_edges)):
        edges.append([])
        for col_index in range(row_index):
            tour_row = christofides_route[row_index].a
            tour_col = christofides_route[col_index].a
            _max = max(tour_row, tour_col)
            _min = min(tour_row, tour_col)
            edges[row_index].append(graph_edges[_max][_min])
    print(edges)
    path = []
    s = 0
    m = 1
    print(vertices[m])
    direction = True
    to_visit = [0,vertices[0]]
    to_visit[1].remove(s)
    while to_visit > 0:
        if m == 1 or vertices[m][0] == vertices[m-1][len(vertices[m-1]) - 1]:
            path, to_visit = shortcut(direction, m, vertices, edges, path, vertices[0], to_visit)
            if vertices[m+1] == vertices[m]:
                #if nothing happened
                path, to_visit = shortcut(not direction, m, vertices, edges, path, vertices[0], to_visit)
        else:
            direction = not direction
            path, to_visit = shortcut(direction, m, vertices, edges, path, vertices[0], to_visit)
        m += 1
    return path

def shortcut(direction, m, vertices, edges, path, all_vertices, to_visit):
    #foreward direction is true, backwards is false
    if not direction:
        vertices[m] = vertices[m][::-1]
    i = 0
    j = 1
    vertices.append(copy.deepcopy(vertices[m]))
    while j < len(vertices[m]):
        print(i,j)
        ij_min = min(i, j)
        ij_max = max(i, j)
        if edges[ij_max][ij_min]:
            print(vertices[m+1])
            print("removing", direction)
            vertices[m+1].remove(vertices[m][j])
            to_visit.remove(vertices[m][j])
            print(vertices[m+1])
            path = path + [(vertices[m][i], vertices[m][j])]
            print((vertices[m][i],vertices[m][j]))
            i = j
            j = i + 1
        else:
            l = i + 1
            li_min = min(l, i)
            li_max = max(l, i)
            lj_min = min(l, j)
            lj_max = max(l, j)
            while l < len(all_vertices) and all_vertices[l] != vertices[m][j] and (not edges[li_max][li_min] or not edges[lj_max][lj_min]):
                l = l + 1
                li_min = min(l, i)
                li_max = max(l, i)
                lj_min = min(l, j)
                lj_max = max(l, j)
            if l < len(all_vertices) and all_vertices[l] != vertices[m][j]:
                print(vertices[m+1])
                print("removing", direction)
                vertices[m+1].remove(vertices[m][j])
                to_visit.remove(vertices[m][j])
                print(vertices[m+1])
                path = path + [(vertices[m][i], l), (l, vertices[m][j])]
                print((vertices[m][i],l), (l,vertices[m][j]))
                i = j
                j = i + 1
            else:
                j = j + 1
    return path, to_visit

def _get_index(vertex, all_vertices):
    return all_vertices.index(vertex)