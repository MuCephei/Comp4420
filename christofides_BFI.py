import BFI
<<<<<<< HEAD
import copy
from sets import Set

def christofides_BFI(graph):
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
            for point in shortest_route[:-1]:
                if point.b in to_visit:
                    to_visit.remove(point.b)
                    for x in range(point.b):
                        if graph.all_edges[point.b][x] == 1 and x not in seen:
                            seen.add(x)
                            edges[point.b][x] = 1
                    for y in range(point.b + 1, len(christofides_route)):
                        if graph.all_edges[y][point.b] == 1 and y not in seen:
                            seen.add(y)
                            edges[y][point.b] = 1
            current_node = target_node
            to_visit.pop(0)
=======
from Traversal import Traversal

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
>>>>>>> Updated organization and generalized code
        else:
            self.to_visit.append(self.to_visit.pop(0))

        if not len(self.to_visit) and not self.finished:
            self.to_visit.append(0)
            self.go_to_target(0)
            self.finished = True

def christofides_BFI(graph, route):
    traversal = ChristofidesBFI(graph, route)
    return traversal.path, traversal.get_distance()
