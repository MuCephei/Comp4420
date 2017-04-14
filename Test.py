from Generate import Graph
from Christofides import christofides_alg
from BFI import find_shortest_path, bfi

test_graph = Graph(5, 6)

test_graph.vertices = [[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1]]
test_graph.all_edges = [[], [0], [0, 0], [0, 1, 0], [1, 0, 1, 1]]

start = 0
end = 1
print("Finding shortest path from " + str(start) + " to " + str(end) + ":")
print(find_shortest_path(test_graph, start, end))

print("\nFinding BFI CCTP cycle:")
print(bfi(test_graph))

print("\nFinding TSP Chrsitofides solution:")
print(christofides_alg(test_graph))
