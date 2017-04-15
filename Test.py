import CCTP
from Generate import Graph
from christofides import christofides_alg

test_graph = Graph(20, 100)
print(test_graph)
print(christofides_alg(test_graph))
print("-------")
print(test_graph)
print("-------")
path = CCTP.cyclic_routing(test_graph)
print("-------")
print(path)
