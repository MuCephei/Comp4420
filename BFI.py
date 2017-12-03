from Edge import Edge

def helper(graph, start, curr, visited):
    shortest_path = None
    min_distance = -1
    path = None
    found = False

    for i in range(len(visited)):
        if not visited[i]:
            found = True
            path, distance = find_shortest_path(graph, graph.all_edges, curr, i)

            new_visited = visited[:]
            for j in range(len(path)):
                new_visited[path[j].b] = True

            new_path, new_distance = helper(graph, start, i, new_visited)
            if min_distance == -1 or distance + new_distance < min_distance:
                shortest_path = path + new_path
                min_distance = distance + new_distance

    if not found:  # There were no more unvisited vertices
        shortest_path, min_distance = find_shortest_path(graph, graph.all_edges, curr, start)

    return shortest_path, min_distance


def bfi(graph):
    visited = []

    for i in range(len(graph.vertices)):
        visited.append(False)
    visited[0] = True

    return helper(graph, 0, 0, visited)


def find_shortest_path(graph, edges, start, end):
    """A la Dijkstra."""
    distance = []
    visited = []
    prev_vertex = []

    def update_neighbors():
        neighbors = []

        for n in range(len(edges[curr])):
            if edges[curr][n] == 1:
                neighbors.append(n)

        for n in range(curr + 1, len(edges)):
            if edges[n][curr] == 1:
                neighbors.append(n)

        for n in range(len(neighbors)):
            if not visited[neighbors[n]]:
                new_distance = distance[curr] + graph.distance(curr, neighbors[n])

                old_distance = distance[neighbors[n]]
                if new_distance < old_distance or old_distance is None:
                    distance[neighbors[n]] = new_distance
                    prev_vertex[neighbors[n]] = curr

    def find_closest_unvisited():
        min_distance = -1
        smallest = -1

        for m in range(len(visited)):
            if (
                not visited[m] and
                distance[m] is not None and
                (distance[m] < min_distance or min_distance == -1)
            ):
                smallest = m
                min_distance = distance[m]

        return smallest

    for i in range(len(graph.vertices)):
        distance.append(None)
        visited.append(False)
        prev_vertex.append(None)

    distance[start] = 0
    visited[start] = True
    curr = start

    while not visited[end]:
        update_neighbors()
        visited[curr] = True
        curr = find_closest_unvisited()

    prev = end
    path = []

    # Iterate backwards creating the path and edges followed
    while curr != start:
        curr = prev_vertex[prev]
        path.insert(0, Edge(curr, prev))
        prev = curr

    return path, distance[end]
