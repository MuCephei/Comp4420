from Generate import Traversal

class NNPessimist(Traversal):
    def __init__(self, graph):
        Traversal.__init__(self, graph)

    def compute(self):
        to_visit = {m for m in range(1, len(self.graph.vertices))}
        while len(to_visit):
            self.look_around()
            self.go_to_closest_unvisited(to_visit)
            to_visit.remove(self.current_node)

        to_visit = {0}
        self.go_to_closest_unvisited(to_visit)

