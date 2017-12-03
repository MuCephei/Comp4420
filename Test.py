import pickle
import constants as k
from Generate import OfflineBruteForce, graph_type
from hybrid_nn import hybrid_nn
from nearest_neighbour_pessimist import NNPessimist

num_intervals = k.num_intervals + 1

prefix = graph_type.prefix()

for num_ver in k.nums:

    total_distances_offline = [0] * num_intervals
    averages_offline = [0] * num_intervals

    total_distances_nn = [0] * num_intervals
    averages_nn = [0] * num_intervals
    max_ratio_nn = [0] * num_intervals

    total_distances_cnn = [0] * num_intervals
    averages_cnn = [0] * num_intervals
    max_ratio_cnn = [0] * num_intervals

    total_distances_opt_nn = [0] * num_intervals
    averages_opt_nn = [0] * num_intervals
    max_ratio_opt_nn = [0] * num_intervals

    with open(prefix + k.get_BFI_name(num_ver), 'w') as BFI_out:
        with open(prefix + k.get_nn_name(num_ver), 'w') as nn_out:
            with open(prefix + k.get_cnn_name(num_ver), 'w') as cnn_out:
                with open(prefix + k.get_opt_nn_name(num_ver), 'w') as opt_nn:
                    for index, i in enumerate(sorted(graph_type.intervals(num_ver))):
                        with open(prefix + k.get_graph_name(i, num_ver)) as f:
                            tests = pickle.load(f)

                        with open(prefix + k.get_path_name(num_ver)) as f:
                            paths = pickle.load(f)

                        with open(prefix + k.get_opt_path_name(num_ver)) as f:
                            opt_paths = pickle.load(f)

                        for q, test in enumerate(tests):
                            path = paths[q]
                            opt_path = opt_paths[q]

                            offline = OfflineBruteForce(test, num_ver)
                            offline_path = offline.path
                            distance_offline = offline.distance
                            total_distances_offline[index] += distance_offline

                            CNN_path, distance_cnn = hybrid_nn(test, path[0], path[1])
                            total_distances_cnn[index] += distance_cnn
                            max_ratio_cnn[index] = max(max_ratio_cnn[index], distance_cnn/distance_offline)

                            opt_nn_path, distance_opt_nn = hybrid_nn(test, opt_path[0], opt_path[1])
                            total_distances_opt_nn[index] += distance_opt_nn
                            max_ratio_opt_nn[index] = max(max_ratio_opt_nn[index], distance_opt_nn/distance_offline)

                            nn = NNPessimist(test)
                            nn.compute()
                            nn_path, distance_nn = nn.path, nn.get_distance()
                            total_distances_nn[index] += distance_nn
                            max_ratio_nn[index] = max(max_ratio_nn[index], distance_nn/distance_offline)


                        averages_offline[index] = total_distances_offline[index] / k.num_tests

                        averages_cnn[index] = total_distances_cnn[index] / k.num_tests

                        averages_opt_nn[index] = total_distances_opt_nn[index] / k.num_tests

                        averages_nn[index] = total_distances_nn[index] / k.num_tests

                    nn_out.write('num_ver,max_ratio,mean\n')
                    BFI_out.write('num_ver,max_ratio,mean\n')
                    cnn_out.write('num_ver,max_ratio,mean\n')
                    opt_nn.write('num_ver,max_ratio,mean\n')

                    for index, i in enumerate(sorted(graph_type.intervals(num_ver))):
                        nn_out.write(','.join(
                            map(str, [i, max_ratio_nn[index], averages_nn[index]])) + '\n')
                        BFI_out.write(','.join(
                            map(str, [i, 1, averages_offline[index]])) + '\n')
                        cnn_out.write(','.join(
                            map(str, [i, max_ratio_cnn[index], averages_cnn[index]])) + '\n')
                        opt_nn.write(','.join(
                            map(str, [i, max_ratio_opt_nn[index], averages_opt_nn[index]])) + '\n')

