import CCTP
import christofides_BFI
from Generate import Graph
from christofides import christofides_alg
from BFI import find_shortest_path, bfi

test_graph = Graph(10,8)
print(test_graph)
print(christofides_alg(test_graph))
print("-----CCTP-----")
path, distance = CCTP.cyclic_routing(test_graph)
print(path, distance)
print("-----christofidesBFI-----")
cBFI, distance = christofides_BFI.christofides_BFI(test_graph)
print(cBFI, distance)
print("-----BFI-----")
shortest_path, min_distance = bfi(test_graph)
print(shortest_path, min_distance)
distance = 0
vertices = test_graph.vertices
for edge in shortest_path:
    distance = distance + test_graph.distance(vertices[edge.a], vertices[edge.b])
print(distance)