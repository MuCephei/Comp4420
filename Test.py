from Generate import Graph
from Christofides import christofides_alg

test_graph = Graph(5, 6)
test_graph.all_edges = [[], [0], [00], [000], [0000]]
test_graph.number_of_broken_edge = 0

test_graph.vertices = [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]]

print(christofides_alg(test_graph))
