import BFI

class Traversal:

    def __init__(self, graph):
        self.graph = graph
        self.current_node = 0
        self.seen = {self.current_node}
        self.size = len(graph.vertices)
        self.edges = [[0] * m for m in range(self.size)]
        self.graph_edges = graph.edges
        self.path = []
        self.finished = False
        self.look_around()

    def see(self, spot):
        large = max(self.current_node, spot)
        small = min(self.current_node, spot)
        if self.graph_edges[large][small] == 1:
            self.seen.add(spot)
            self.edges[large][small] = 1

    def look_around(self):
        for x in range(0, self.size):
            if x != self.current_node:
                self.see(x)

    def go_to_closest_unvisted(self, to_visit):
        targets = list(filter(lambda t: t in self.seen, to_visit))
        distances = [float("inf")] * len(targets)
        shortest_routes = [[]] * len(targets)
        for index, t in enumerate(targets):
            shortest_routes[index], distances[index] = BFI.find_shortest_path(self.graph, self.edges, self.current_node, t)

        next_index = distances.index(min(distances))
        self.path += shortest_routes[next_index]
        self.current_node = targets[next_index]

    def get_distance(self):
        distance = 0
        for edge in self.path:
            distance = distance + self.graph.distance(self.graph.vertices[edge.a], self.graph.vertices[edge.b])
        return distance
