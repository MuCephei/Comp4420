import CCTP
import christofides_BFI
from Generate import Graph
from christofides import christofides_alg
from BFI import find_shortest_path, bfi

test_graph = Graph(5,6)
print(test_graph)
print(christofides_alg(test_graph))
print("---CCTP----")
path, distance = CCTP.cyclic_routing(test_graph)
print(path, distance)
print("_____christofidesBFI______")
cBFI, distance = christofides_BFI.christofides_BFI(test_graph)
print(cBFI, distance)