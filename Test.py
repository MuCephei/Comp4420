from CCTP import CCTP
import pickle
import constants as k
from christofides_BFI import christofides_BFI
from nearest_neighbour_pessimist import NNPessimist

num_intervals = k.num_intervals + 1

for num_ver in range(18, 5, -1):
    total_distances_CCTP = [0] * num_intervals
    averages_CCTP = [0] * num_intervals
    total_num_brute = [0] * num_intervals
    averages_num_brute = [0] * num_intervals
    max_distance_CCTP = [0] * num_intervals
    min_distance_CCTP = [float("inf")] * num_intervals

    total_distances_CBFI = [0] * num_intervals
    averages_CBFI = [0] * num_intervals
    max_distance_CBFI = [0] * num_intervals
    min_distance_CBFI = [float("inf")] * num_intervals

    total_distances_nn = [0] * num_intervals
    averages_nn = [0] * num_intervals
    max_distance_nn = [0] * num_intervals
    min_distance_nn = [float("inf")] * num_intervals

    with open(k.get_cbfi_name(num_ver), 'w') as cbfi_out:
        with open(k.get_cctp_name(num_ver), 'w') as cctp_out:
            with open(k.get_nn_name(num_ver), 'w') as nn_out:
                for index, i in enumerate(sorted(k.intervals(num_ver))):
                    with open(k.get_graph_name(i, num_ver)) as f:
                        tests = pickle.load(f)

                    with open(k.get_path_name(num_ver)) as f:
                        paths = pickle.load(f)

                    for q, test in enumerate(tests):
                        path = paths[q]

                        cctp = CCTP(test, path)
                        cctp.compute()
                        path_CCTP, distance, num_brute = cctp.path, cctp.get_distance(), cctp.num_brute
                        total_distances_CCTP[index] += distance
                        total_num_brute[index] = total_num_brute[index] + num_brute
                        max_distance_CCTP[index] = max(max_distance_CCTP[index], distance)
                        min_distance_CCTP[index] = min(min_distance_CCTP[index], distance)

                        CBFI_path, distance_CBFI = christofides_BFI(test, path)
                        total_distances_CBFI[index] += distance_CBFI
                        max_distance_CBFI[index] = max(max_distance_CBFI[index], distance_CBFI)
                        min_distance_CBFI[index] = min(min_distance_CBFI[index], distance_CBFI)

                        nn = NNPessimist(test)
                        nn.compute()
                        nn_path, distance_nn = nn.path, nn.get_distance()
                        total_distances_nn[index] += distance_nn
                        max_distance_nn[index] = max(max_distance_nn[index], distance_nn)
                        min_distance_nn[index] = min(min_distance_nn[index], distance_nn)

                    averages_CCTP[index] = total_distances_CCTP[index] / k.num_tests
                    averages_num_brute[index] = total_num_brute[index] / k.num_tests

                    averages_CBFI[index] = total_distances_CBFI[index] / k.num_tests

                    averages_nn[index] = total_distances_nn[index] / k.num_tests

                nn_out.write('num_ver,max,min,mean\n')
                cctp_out.write('num_ver,max,min,mean\n')
                cbfi_out.write('num_ver,max,min,mean\n')

                for index, i in enumerate(sorted(k.intervals(num_ver))):
                    nn_out.write(','.join(
                        map(str, [i, max_distance_nn[index], min_distance_nn[index], averages_nn[index]])) + '\n')
                    cbfi_out.write(','.join(
                        map(str, [i, max_distance_CBFI[index], min_distance_CBFI[index], averages_CBFI[index]])) + '\n')
                    cctp_out.write(','.join(
                        map(str, [i, max_distance_CCTP[index], min_distance_CCTP[index], averages_CCTP[index]])) + '\n')

