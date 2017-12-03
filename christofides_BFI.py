import BFI
from Generate import Traversal

class ChristofidesBFI(Traversal):
    def __init__(self, graph, route):
        Traversal.__init__(self, graph)
        self.route = route
        self.to_visit = []
        for point in self.route[1:]:
            self.to_visit.append(point.a)

        self.compute()

    def go_to_target(self, target):
        shortest_route, distance = \
            BFI.find_shortest_path(self.graph, self.edges, self.current_node, target)
        self.path += shortest_route
        self.current_node = target
        self.to_visit.remove(target)

    def compute(self):
        self.look_around()
        while not self.finished:
            self.do_next()
            self.look_around()

    def do_next(self):
        target = self.to_visit[0]
        if target in self.seen:
            self.go_to_target(target)
        else:
            self.to_visit.append(self.to_visit.pop(0))

        if not len(self.to_visit) and not self.finished:
            self.to_visit.append(0)
            self.go_to_target(0)
            self.finished = True

def christofides_BFI(graph, route):
    traversal = ChristofidesBFI(graph, route)
    return traversal.path, traversal.get_distance()
