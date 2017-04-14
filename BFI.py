from Generate import Edge


def bfi(graph):
    print("hahaha nice try")


def find_shortest_path(graph, start, end):
    """A la Dijkstra."""
    distance = []
    visited = []
    prev_vertex = []

    def update_neighbors():
        neighbors = []

        for n in range(len(graph.all_edges[curr])):
            if graph.all_edges[curr][n] == 1:
                neighbors.append(n)

        for n in range(curr + 1, len(graph.all_edges)):
            if graph.all_edges[n][curr] == 1:
                neighbors.append(n)

        for n in range(len(neighbors)):
            if not visited[neighbors[n]]:
                new_distance = distance[curr] + graph.distance(
                    graph.vertices[curr], graph.vertices[n]
                )

                old_distance = distance[neighbors[n]]
                if new_distance < old_distance or old_distance is None:
                    distance[neighbors[n]] = new_distance
                    prev_vertex[neighbors[n]] = curr

    def find_closest_unvisited():
        min_distance = -1
        smallest = -1

        for m in range(len(visited)):
            if not visited[m] and (distance[m] < min_distance or
                                   min_distance == -1):
                smallest = m

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

    return path
