import CCTP
import christofides_BFI
import matplotlib.pyplot as plt
import numpy as np
import time
from Generate import Graph
from christofides import christofides_alg
from BFI import find_shortest_path, bfi

num_ver = 21
min_num_edges = num_ver - 1
max_num_edges = (num_ver * (num_ver - 1))/2
max_num_deleted = max_num_edges - min_num_edges
intervals = 20
num_tests = 50
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
mean_time_chris =[]
mean_num_brutes = []
std_distances_BFI = []
std_distances_cBFI = []
std_distances_CCTP = []
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
    times_chris = []
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
    print_info(d, t, "ACA")

    for test in tests:
        start = time.clock()
        christofides_route = christofides_alg(test)
        times_chris.append(time.clock() - start)
    t = np.array(times_chris)
    mean_time_chris.append(np.mean(t))

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
    std_num_brutes.append(np.std(n))
    print_info(d, t, "ICR", num_brute=n)

print("")
fig = plt.figure()
ax = plt.subplot(111)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])
ax.errorbar(interval_values, mean_distances_CCTP, std_distances_CCTP, color='green')
ax.errorbar(interval_values, mean_distances_cBFI, std_distances_cBFI, color='blue')
ax.axvline(x=num_ver-2, color="black", linestyle=":")
legend = ['D ICR', 'D ACA', 'n-2']
if do_BFI:
    ax.errorbar(interval_values, mean_distances_BFI, std_distances_BFI, color='red')
    legend.append('D BFI')
ax.legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=len(legend))
ax.set_xlabel('Blocked Paths (k)')
ax.set_ylabel('Distance (units)')
ax.set_title('Distance n = ' + str(num_ver))
ax.set_xlim(interval_values[0] - 1,interval_values[-1] + 1)
plt.show()

fig = plt.figure()
ax = plt.subplot(111)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
ax.errorbar(interval_values, mean_times_CCTP, color='green')
ax.errorbar(interval_values, mean_times_cBFI, color='blue')
ax.errorbar(interval_values, mean_time_chris, color='black')
ax.axvline(x=num_ver-2, color="black", linestyle=":")
legend = ['T ICR', 'T ACA', 'T chris', 'n-2']
if do_BFI:
    ax.plot(interval_values, mean_times_BFI, color='red')
    legend.append('T BFI')
ax.legend(legend, loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=len(legend))
ax.set_xlabel('Blocked Paths (k)')
ax.set_ylabel('Time (s)')
ax.set_yscale('log')
ax.set_title('Time n = ' + str(num_ver))
ax.set_xlim(interval_values[0] - 1,interval_values[-1] + 1)
plt.show()
