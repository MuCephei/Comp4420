import CCTP
from Generate import Graph
from christofides import christofides_alg
from BFI import find_shortest_path, bfi

test_graph = Graph(5,6)
print(test_graph)
print(christofides_alg(test_graph))
# print("-------")
# print(test_graph)
print("-------")
path = CCTP.cyclic_routing(test_graph)
# print("-------")
print(path)
