import pickle
import constants as k
from christofides_alg import christofides_alg
from Generate import Graph
from multiprocessing import Pool, cpu_count

def _make_graph(num_ver):
    intervals = k.intervals(num_ver)

    base_graphs = [Graph(num_ver, num_ver - 1)] * k.num_tests
    base_paths = [christofides_alg(graph) for graph in base_graphs]

    with open(k.get_path_name(num_ver), 'w') as f:
        pickle.dump(base_paths, f)

    del base_paths

    for i in intervals:
        graphs = map(lambda x: x.copy(i), base_graphs)
        with open(k.get_graph_name(i, num_ver), 'w') as f:
            pickle.dump(graphs, f)

    print(num_ver)

if __name__ == '__main__':
    p = cpu_count() - 1
    print(p)
    pool = Pool(processes = p)
    pool.map(_make_graph, range(20, 5,  -1))
