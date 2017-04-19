import CCTP
import christofides_BFI
import matplotlib as plt
from Generate import Graph
from christofides import christofides_alg
from BFI import find_shortest_path, bfi

num_ver = 8
max_num_deleted = 12
intervals = 12
num_tests = 100
total_distances_cBFI = [0 for n in range(intervals)]
averages_cBFI = [0 for n in range(intervals)]
total_distances_CCTP = [0 for n in range(intervals)]
averages_CCTP = [0 for n in range(intervals)]

print("Summary")
for i in range(intervals):
	max_distance_cBFI = 0
	min_distance_cBFI = float("inf")
	max_distance_CCTP = 0
	min_distance_CCTP = float("inf")

	num_deleted = (max_num_deleted * i)/(intervals - 1)

	tests = [Graph(num_ver, num_deleted) for n in range(num_tests)]
	for test in tests:
		path_cBFI, distance = christofides_BFI.christofides_BFI(test)
		total_distances_cBFI[i] = total_distances_cBFI[i] + distance
		max_distance_cBFI = max(max_distance_cBFI, distance)
		min_distance_cBFI = min(min_distance_cBFI, distance)

		path_CCTP, distance = CCTP.cyclic_routing(test)
		total_distances_CCTP[i] = total_distances_CCTP[i] + distance
		max_distance_CCTP = max(max_distance_CCTP, distance)
		min_distance_CCTP = min(min_distance_CCTP, distance)
	averages_cBFI[i] = total_distances_cBFI[i]/num_tests
	averages_CCTP[i] = total_distances_CCTP[i]/num_tests
	print("___________________________")
	print((max_num_deleted * i)/(intervals - 1))
	print("\ncBFI")
	print(max_distance_cBFI)
	print(min_distance_cBFI)
	print(averages_cBFI[i])
	print("\nCCTP")
	print(max_distance_CCTP)
	print(min_distance_CCTP)
	print(averages_CCTP[i])
	print("___________________________")