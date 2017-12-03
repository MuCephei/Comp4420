import random
import math
import constants as k
import numpy as np
from collections import defaultdict
from Christofides import christofides
from Edge import Edge
import os

def euclidean_distance(a, b):
    return math.sqrt((a[1] - b[1]) ** 2 + (a[0] - b[0]) ** 2)

class DistanceTable:
    
    def __init__(self, vertices, edges=None):
        size = len(vertices)
        self.vertices = vertices
        self.edges = edges
        if not self.edges:
            self.edges = [[1 for n in range(m)] for m in range(size)]

        self.paths = [[[Edge(x, y)] for x in range(size)] for y in range(size)]
        self.distances = [[0 if x == y else float("inf") for x in range(size)] for y in range(size)]

        self._update()

    def _update(self, changed_edges=None):
        if changed_edges:
            changed = changed_edges
            for c in changed_edges:
                point_a = self.vertices[c.a]
                point_b = self.vertices[c.b]
                d = euclidean_distance(point_a, point_b)
                self.distances[c.a][c.b] = d
                self.distances[c.b][c.a] = d

                self.paths[c.a][c.b] = [Edge(c.a, c.b)]
                self.paths[c.b][c.a] = [Edge(c.b, c.a)]
        else:
            changed = []
            self.old_changed = []
            for i1, v1 in enumerate(self.vertices):
                for i2, v2 in enumerate(self.vertices[:i1]):
                    if self.edges[max(i1, i2)][min(i1, i2)]:
                        d = euclidean_distance(v1, v2)
                        self.distances[i1][i2] = d
                        self.distances[i2][i1] = d

                        self.paths[i1][i2] = [Edge(i1, i2)]
                        self.paths[i2][i1] = [Edge(i2, i1)]

                        changed.append(Edge(i1, i2))
        while changed:
            recently_changed = changed
            self.old_changed += recently_changed
            changed = []
            for change1 in recently_changed:
                for change2 in self.old_changed:
                    do = False
                    if change1.a == change2.a:
                        a = max(change1.b, change2.b)
                        b = min(change1.b, change2.b)
                        c = change1.a
                        do = True
                    elif change1.b == change2.a:
                        a = change1.a
                        b = change2.b
                        c = change1.b
                        do = True
                    elif change1.a == change2.b:
                        a = change2.a
                        b = change1.b
                        c = change1.a
                        do = True
                    if change1.b == change2.b:
                        a = max(change1.a, change2.a)
                        b = min(change1.a, change2.a)
                        c = change1.b
                        do = True
                    if do:
                        new_d = self.distances[a][c] + self.distances[c][b]
                        if new_d < self.distances[a][b]:
                            self.distances[a][b] = new_d
                            self.distances[b][a] = new_d

                            self.paths[a][b] = self.paths[a][c] + self.paths[c][b]
                            self.paths[b][a] = self.paths[b][c] + self.paths[c][a]
                            changed.append(Edge(a, b))

    def add_edges(self, new_edges):
        for edge in new_edges:
            large = max(edge.a, edge.b)
            small = min(edge.a, edge.b)
            self.edges[large][small] = 1

        self._update(changed_edges = new_edges)

    def __str__(self):
        return str(self.distances)

def get_minimum_spanning_distance(distance_matrix, size):
    unconnected = {}
    for i in range(1, size):
        unconnected[i] = 0
    max_distance = 0

    def get_distance(x):
        y = unconnected[x]
        return distance_matrix[x][y]

    while unconnected:
        closest = min(unconnected, key=lambda x: get_distance(x))
        max_distance = max(max_distance, get_distance(closest))
        del unconnected[closest]
        for i in unconnected:
            if distance_matrix[i][closest] < distance_matrix[i][unconnected[i]]:
                unconnected[i] = closest
    return max_distance

class Graph:
    max_x = 100
    max_y = 100

    # Note that Vertices are [Y coords, X coords]
    def __init__(self, number_of_vertices, number_of_edges, vertices=None):
        self.n = number_of_vertices
        self.e = number_of_edges

        self.create_vertices(vertices)
        self.edges = self.create_edges()
        self.distance_table = None

    def create_vertex(self):
        return random.random() * self.max_x, random.random() * self.max_y

    @staticmethod
    def name():
        return 'Rectangular Graph'

    @staticmethod
    def prefix():
        return ''

    def create_vertices(self, vertices):
        if vertices:
            self.vertices = vertices
        else:
            self.vertices = [self.create_vertex() for n in range(self.n)]

    def get_paths(self):
        self.calculate_distances()
        return self.distance_table.paths

    def get_distance_table(self):
        self.calculate_distances()
        return self.distance_table.distances

    def calculate_distances(self):
        if not self.distance_table:
            self.distance_table = DistanceTable(self.vertices, self.edges)

    def edge_distance(self, edge):
        self.calculate_distances()
        return self.get_distance_table()[edge.a][edge.b]

    def distance(self, a, b):
        self.calculate_distances()
        return self.get_paths()[a][b]

    def __str__(self):
        return str(self.vertices) + '\n' + str(self.edges)

    def __repr__(self):
        return str(self)

    def create_edges(self):
        unused_edges = set(sum(map(lambda b: [Edge(a, b) for a in range(b + 1, self.n)], range(self.n)), []))
        edge_set = set()
        #first connect the unconnected edges
        for node in range(1, self.n):
            rand = random.randint(0, node - 1)
            a = max(rand, node)
            b = min(rand, node)
            new_edge = Edge(a, b)
            edge_set.add(new_edge)
            unused_edges.remove(new_edge)

        while len(edge_set) < self.e:
            new_edge = random.sample(unused_edges, 1)[0]
            edge_set.add(new_edge)
            unused_edges.remove(new_edge)

        edges = [[0] * m for m in range(self.n)]

        for e in edge_set:
            edges[e.a][e.b] = 1

        return edges

    def copy(self, number_of_edges):
        graph_copy = Graph(self.n, number_of_edges, self.vertices)

        return graph_copy

    def make_christofides_route(self):
        self.calculate_distances()
        result = christofides.compute(self.distance_table.distances)
        solution = result['Christofides_Solution']
        path = []
        for index in range(1, len(solution)):
            path += [Edge(solution[index - 1], solution[index])]
        return path, self.get_paths()

    def make_optimal_route(self):
        self.calculate_distances()
        solution = OfflineBruteForce(self, self.n).path
        return solution, self.get_paths()

    @staticmethod
    def init_intervals(num_ver):
        return (num_ver * (num_ver - 1))/2

    @staticmethod
    def bonus_intervals():
        return 1

    @staticmethod
    def intervals(num_ver):
        max_num_present = k.max_num(num_ver)
        min_num_present = k.min_num(num_ver)
        max_range = max_num_present - min_num_present
        return [min_num_present + (num_ver - 2)] + \
               [((max_range * i) / (k.num_intervals - 1)) + min_num_present for i in range(k.num_intervals)]

class UnitDiskGraph(Graph):

    def __init__(self, number_of_vertices, percent_edges, vertices=None, max_distance=0):
        if percent_edges > 1:
            percent_edges = 1
        self.max_distance = max_distance
        Graph.__init__(self, number_of_vertices, percent_edges, vertices=vertices)

    def create_edges(self):
        edge_distance_table = DistanceTable(self.vertices)
        dm = edge_distance_table.distances
        if not self.max_distance:
            self.max_distance = get_minimum_spanning_distance(dm, self.n)
        self.full_edges = [[0 for n in range(m)] for m in range(self.n)]
        unused_edges = []
        for x, v1 in enumerate(self.vertices):
            for y, v2 in enumerate(self.vertices[:x]):
                edge = euclidean_distance(v1, v2) <= self.max_distance
                if edge:
                    self.full_edges[x][y] = 1
                    unused_edges.append((x, y))

        self.edges = [[0] * m for m in range(self.n)]
        edge_count = 0
        unconnected = set(range(1, self.n))
        connected = {0}

        count = 0
        while unconnected:
            count += 1
            for u in random.sample(list(unconnected), len(unconnected)):
                possible_connections = []
                for c in connected:
                    a = max(u, c)
                    b = min(u, c)
                    if self.full_edges[a][b]:
                        possible_connections.append(c)
                if possible_connections:
                    c = random.choice(possible_connections)
                    connected.add(u)
                    unconnected.remove(u)
                    a = max(u, c)
                    b = min(u, c)
                    unused_edges.remove((a, b))
                    self.edges[a][b] = 1
                    edge_count += 1

        num_edges_to_use = int(len(unused_edges) * self.e)

        if num_edges_to_use:
            new_edges = random.sample(unused_edges, num_edges_to_use)
            for e in new_edges:
                self.edges[e[0]][e[1]] = 1

        return self.edges

    @staticmethod
    def prefix():
        return 'Unit_'

    @staticmethod
    def name():
        return 'Unit Disk Graph'

    def copy(self, percent_edges):
        graph_copy = UnitDiskGraph(self.n, percent_edges, vertices = self.vertices, max_distance = self.max_distance)
        return graph_copy

    @staticmethod
    def init_intervals(num_ver):
        return 1.0

    @staticmethod
    def bonus_intervals():
        return 0

    @staticmethod
    def intervals(num_ver):
        return np.linspace(1.0, 0.0, num=k.num_intervals)

class GridGraph(Graph):

    def __init__(self, number_of_vertices, percent_edges, vertices=None, max_distance=0):
        if percent_edges > 1:
            percent_edges = 1
        self.max_distance = max_distance
        Graph.__init__(self, number_of_vertices, percent_edges, vertices=vertices)

    def nearby_spots(self, spot):
        for around in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x = spot[0] + around[0]
            y = spot[1] + around[1]
            if 0 <= x < self.max_x and 0 <= y < self.max_y:
                yield x, y

    def update_spots(self, spot):
        for s in self.nearby_spots(spot):
            if not self.spots[s[0]][s[1]]:
                self.spots[s[0]][s[1]] = 1
                self.possible_spots.add(s)

    def create_vertex(self):
        try:
            return random.sample(self.possible_spots, 1)[0]
        except:
            print('possible_spots')
            print('v', self.vertices)
            print('spots', self.spots)
            raise Exception

    def create_vertices(self, vertices):
        if vertices:
            self.vertices = vertices
            return

        self.spots = defaultdict(lambda: defaultdict(int))
        self.possible_spots = set()

        v = (random.randint(0, self.max_x), random.randint(0, self.max_y))
        self.spots[v[0]][v[1]] = 2
        self.vertices = [v]
        self.update_spots(v)

        while len(self.vertices) < self.n:
            v = self.create_vertex()
            self.possible_spots.remove(v)
            self.spots[v[0]][v[1]] = 2
            self.vertices.append(v)
            self.update_spots(v)


    def create_edges(self):
        edge_distance_table = DistanceTable(self.vertices)
        dm = edge_distance_table.distances
        if not self.max_distance:
            self.max_distance = get_minimum_spanning_distance(dm, self.n)
        self.full_edges = [[0 for n in range(m)] for m in range(self.n)]
        unused_edges = []
        for x, v1 in enumerate(self.vertices):
            for y, v2 in enumerate(self.vertices[:x]):
                edge = euclidean_distance(v1, v2) <= self.max_distance
                if edge:
                    self.full_edges[x][y] = 1
                    unused_edges.append((x, y))

        self.edges = [[0] * m for m in range(self.n)]
        edge_count = 0
        unconnected = set(range(1, self.n))
        connected = {0}

        count = 0
        while unconnected:
            count += 1
            for u in random.sample(list(unconnected), len(unconnected)):
                possible_connections = []
                for c in connected:
                    a = max(u, c)
                    b = min(u, c)
                    if self.full_edges[a][b]:
                        possible_connections.append(c)
                if possible_connections:
                    c = random.choice(possible_connections)
                    connected.add(u)
                    unconnected.remove(u)
                    a = max(u, c)
                    b = min(u, c)
                    unused_edges.remove((a, b))
                    self.edges[a][b] = 1
                    edge_count += 1

        num_edges_to_use = int(len(unused_edges) * self.e)

        if num_edges_to_use:
            new_edges = random.sample(unused_edges, num_edges_to_use)
            for e in new_edges:
                self.edges[e[0]][e[1]] = 1

        return self.edges

    @staticmethod
    def prefix():
        return 'Grid_'

    @staticmethod
    def name():
        return 'Grid Graph'

    def copy(self, percent_edges):
        graph_copy = GridGraph(self.n, percent_edges, vertices = self.vertices, max_distance = self.max_distance)
        return graph_copy

    @staticmethod
    def init_intervals(num_ver):
        return 1.0

    @staticmethod
    def bonus_intervals():
        return 0

    @staticmethod
    def intervals(num_ver):
        return np.linspace(1.0, 0.0, num=k.num_intervals)

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
        temp_edges = [[0 for n in range(m)] for m in range(self.size)]
        self.distance_table = DistanceTable(graph.vertices, edges = temp_edges)
        self.look_around()

    def see(self, spot):
        large = max(self.current_node, spot)
        small = min(self.current_node, spot)
        if self.graph_edges[large][small] == 1:
            self.seen.add(spot)
            self.edges[large][small] = 1
            self.distance_table.add_edges([Edge(large, small)])

    def look_around(self):
        for x in range(0, self.size):
            if x != self.current_node:
                self.see(x)

    def go_to_closest_unvisited(self, to_visit):
        targets = list(filter(lambda t: t in self.seen, to_visit))
        distances = self.distance_table.distances

        closest_target = min(targets, key=lambda t: distances[self.current_node][t])
        shortest_route = self.distance_table.paths[self.current_node][closest_target]

        self.path = self.path + shortest_route
        self.current_node = closest_target

    def get_distance(self):
        distance = 0
        for edge in self.path:
            distance += self.graph.edge_distance(edge)
        return distance

class OfflineBruteForce:
    template = """NAME: {name}
TYPE: TSP
COMMENT: {name}
DIMENSION: {n_cities}
EDGE_WEIGHT_TYPE: EXPLICIT
EDGE_WEIGHT_FORMAT: LOWER_DIAG_ROW
EDGE_WEIGHT_SECTION
{matrix_s}EOF"""

    in_file = '/tmp/temp.tsp'
    out_file = '/tmp/out.txt'
    concorde = '/Library/Concorde/concorde/TSP/concorde'


    @staticmethod
    def dumps_matrix(matrix, name="route"):
        #Credit to jvkersch

        arr = np.array(matrix)
        n_cities = arr.shape[0]
        width = len(str(arr.max())) + 1

        assert arr.shape[0] == arr.shape[1]
        assert len(arr.shape) == 2

        # space delimited string
        matrix_s = ""
        for i, row in enumerate(arr.tolist()):
            matrix_s += " ".join(["{0:>{1}}".format((int(elem)), width)
                                  for elem in row[:i + 1]])
            matrix_s += "\n"

        return OfflineBruteForce.template.format(**{'name': name,
                                                    'n_cities': n_cities,
                                                    'matrix_s': matrix_s})

    def __init__(self, graph, id):
        id = str(id)
        self.graph = graph
        self.distance_table = DistanceTable(graph.vertices, graph.edges)

        with open(self.in_file + id, 'w') as dest:
            dest.write(self.dumps_matrix(self.distance_table.distances))

        os.system(self.concorde + ' -o ' + self.out_file + id + ' ' + self.in_file + id)

        with open(self.out_file + id, 'r') as out:
            high_level_path = map(int, out.read().strip().split()[1:]) + [0]

        self.path = []
        for i in range(len(high_level_path) - 1):
            self.path.append(Edge(high_level_path[i], high_level_path[i + 1]))

        self.distance = self.get_distance()

    def get_distance(self):
        distance = 0

        for edge in self.path:
            distance = distance + self.graph.edge_distance(edge)
        return distance

    def get_low_level_distance(self):
        low_path = self.get_low_level_path()
        distance = 0

        for edge in low_path:
            distance = distance + self.graph.edge_distance(edge)
        return distance

    def get_low_level_path(self):
        low_path = []
        for e in self.path:
            low_path += self.distance_table.paths[e.a][e.b]
        return low_path


graph_type = GridGraph
