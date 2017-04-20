import CCTP
import christofides_BFI
import matplotlib.pyplot as plt
import numpy as np
import time
from Generate import Graph
from christofides import christofides_alg
from BFI import find_shortest_path, bfi

num_ver = 25
min_num_edges = num_ver - 1
max_num_edges = (num_ver * (num_ver - 1))/2
max_num_deleted = max_num_edges - min_num_edges
intervals = 50
num_tests = 10
do_BFI = False

def print_info(distances, times, title, num_brute=[]):
    print("-------------------" + title + "----------------------")
    n = num_brute
    contents = ("            Distance\n" +
        "Mean                             {0}\n" +
        "Standard deviation               {1}\n\n" +
        "           Time\n" +
        "Mean                             {2}\n" +
        "Standard deviation               {3}"
        ).format(np.mean(d), np.std(d), np.mean(t), np.std(t))
    if len(n):
        contents = contents + ("\n\n           Num Brute\n" +
        "Mean                             {0}\n" +
        "Standard deviation               {1}"
        ).format(np.mean(n), np.std(n))
    print(contents)
    print("-----------------------------------------")


print("Summary")

mean_distances_BFI = []
mean_times_BFI = []
mean_distances_cBFI = []
mean_times_cBFI = []
mean_distances_CCTP = []
mean_times_CCTP = []
mean_num_brutes = []
std_distances_BFI = []
std_times_BFI = []
std_distances_cBFI = []
std_times_cBFI = []
std_distances_CCTP = []
std_times_CCTP = []
std_num_brutes = []
interval_values = []

for i in range(intervals):
    num_deleted = (max_num_deleted * i)/(intervals - 1)
    interval_values.append(num_deleted)
    total_distances_BFI = []
    times_BFI = []
    total_distances_cBFI = []
    times_cBFI = []
    total_distances_CCTP = []
    times_CCTP = []
    num_brutes = []

    print(("\nVertices={0} k={1} Edges={2}\n").format(num_ver, num_deleted, max_num_edges - num_deleted))
    tests = [Graph(num_ver, num_deleted) for n in range(num_tests)]
    if do_BFI:
        for test in tests:
            start = time.clock()
            path, distance = bfi(test)
            times_BFI.append(time.clock() - start)
            total_distances_BFI.append(distance)
        d = np.array(total_distances_BFI)
        t = np.array(times_BFI)
        mean_distances_BFI.append(np.mean(d))
        mean_times_BFI.append(np.mean(t))
        std_distances_BFI.append(np.std(d))
        std_times_BFI.append(np.std(t))
        print_info(d, t, "BFI")

    for test in tests:
        start = time.clock()
        path, distance = christofides_BFI.christofides_BFI(test)
        times_cBFI.append(time.clock() - start)
        total_distances_cBFI.append(distance)
    d = np.array(total_distances_cBFI)
    t = np.array(times_cBFI)
    mean_distances_cBFI.append(np.mean(d))
    mean_times_cBFI.append(np.mean(t))
    std_distances_cBFI.append(np.std(d))
    std_times_cBFI.append(np.std(t))
    print_info(d, t, "cBFI")

    for test in tests:
        start = time.clock()
        path, distance, num_brute = CCTP.cyclic_routing(test)
        times_CCTP.append(time.clock() - start)
        total_distances_CCTP.append(distance)
        num_brutes.append(num_brute)
    d = np.array(total_distances_CCTP)
    t = np.array(times_CCTP)
    n = np.array(num_brutes)
    mean_distances_CCTP.append(np.mean(d))
    mean_times_CCTP.append(np.mean(t))
    mean_num_brutes.append(np.mean(n))
    std_distances_CCTP.append(np.std(d))
    std_times_CCTP.append(np.std(t))
    std_num_brutes.append(np.std(n))
    print_info(d, t, "CCTP", num_brute=n)

print("")
plt.errorbar(interval_values, mean_distances_CCTP, std_distances_CCTP, color='green')
plt.errorbar(interval_values, mean_distances_cBFI, std_distances_cBFI)
legend = ['n-2','Distance CCTP', 'Distance cBFI']
if do_BFI:
    plt.errorbar(interval_values, mean_distances_BFI, std_distances_BFI)
    legend.append('Distance BFI')
plt.axvline(x=num_ver-2, color="black")
plt.legend(legend, loc='upper left')
plt.xlabel('Blocked Paths')
plt.ylabel('Distance (units)')
plt.title('n = ' + str(num_ver))
plt.xlim(interval_values[0],interval_values[-1])
plt.show()

plt.errorbar(interval_values, mean_times_CCTP, color='green')
plt.errorbar(interval_values, mean_times_cBFI)
legend = ['n-2','Time CCTP', 'Time cBFI']
if do_BFI:
    plt.plot(interval_values, mean_times_BFI)
    legend.append('Time BFI')
plt.axvline(x=num_ver-2, color="black")
plt.legend(legend, loc='upper left')
plt.xlabel('Blocked Paths')
plt.ylabel('Time (s)')
plt.yscale('log')
plt.title('n = ' + str(num_ver))
plt.xlim(interval_values[0],interval_values[-1])
plt.show()
