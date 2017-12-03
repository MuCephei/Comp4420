from Generate import Traversal

class HybridNN(Traversal):
    def __init__(self, graph, route, paths):
        Traversal.__init__(self, graph)
        self.route = route
        self.paths = paths
        self.to_visit = {m for m in range(1, len(self.graph.vertices))}
        self.next_target = {}
        self.mini_path = []
        for point in self.route:
            if point.a not in self.next_target:
                self.next_target[point.a] = point.b

        self.compute()

    def try_go_to_target(self, target):
        x = max(self.current_node, target)
        y = min(self.current_node, target)

        if target != -1 and target in self.seen and self.edges[x][y]:
            self.path += self.distance_table.paths[self.current_node][target]
            self.current_node = target
        else:
            self.go_to_closest_unvisited(self.to_visit)
            self.mini_path = []

        if self.current_node and self.current_node in self.to_visit:
            self.to_visit.remove(self.current_node)

    def compute(self):
        self.look_around()
        while len(self.to_visit):
            self.do_next()
            self.look_around()

        self.to_visit.add(0)
        self.go_to_closest_unvisited(self.to_visit)

    def do_next(self):
        if not self.mini_path:
            self.mini_path = []
            if self.next_target[self.current_node] in self.to_visit:
                for edge in self.paths[self.current_node][self.next_target[self.current_node]]:
                    self.mini_path.append(edge.b)
            else:
                self.mini_path.append(-1)
        target = self.mini_path.pop(0)
        self.try_go_to_target(target)

def hybrid_nn(graph, route, paths):
    traversal = HybridNN(graph, route, paths)
    return traversal.path, traversal.get_distance()