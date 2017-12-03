import pickle
import constants as k
from Generate import graph_type, OfflineBruteForce
from nearest_neighbour_pessimist import NNPessimist

prefix = graph_type.prefix()
num_ver = 10

# for index, i in enumerate(sorted(graph_type.intervals(num_ver))):
for i in [9]:
    with open(prefix + k.get_graph_name(i, num_ver)) as f:
        tests = pickle.load(f)

    with open(prefix + k.get_path_name(num_ver)) as f:
        paths = pickle.load(f)

    with open(prefix + k.get_opt_path_name(num_ver)) as f:
        opt_paths = pickle.load(f)

    q = 72
    test = tests[q]
    path = paths[q]
    opt_path = opt_paths[q]

    offline = OfflineBruteForce(test, num_ver)
    offline_path = offline.path
    offline_distance = offline.distance

    print('\n\n\n\n\n\n\n\n')

    nn = NNPessimist(test)
    nn.compute()
    nn_path, distance_nn = nn.path, nn.get_distance()

    ratio = distance_nn/offline_distance
    print('\n\n\n\n\n\n\n\n')
    print(distance_nn/offline_distance, distance_nn, offline_distance, offline.get_low_level_distance())
    print('distances', offline.distance_table.distances)
    print('offline', offline_path)
    print('low_offline', offline.get_low_level_path())
    print('nn', nn_path)
    print('graph', test)