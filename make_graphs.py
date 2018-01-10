import pickle
import constants as k
from Generate import graph_type
from multiprocessing import Pool, cpu_count

def _make_graph(num_ver):

    prefix = graph_type.prefix()

    base_graphs = [graph_type(num_ver, graph_type.init_intervals(num_ver)) for n in range(k.num_tests)]
    intervals = graph_type.intervals(num_ver)
    base_paths = [graph.make_christofides_route() for graph in base_graphs]

    with open(prefix + k.get_path_name(num_ver), 'w') as f:
        pickle.dump(base_paths, f)

    del base_paths

    opt_paths = [graph.make_optimal_route() for graph in base_graphs]

    with open(prefix + k.get_opt_path_name(num_ver), 'w') as f:
        pickle.dump(opt_paths, f)

    del opt_paths

    for i in intervals:
        graphs = map(lambda x: x.copy(i), base_graphs)
        with open(prefix + k.get_graph_name(i, num_ver), 'w') as f:
            pickle.dump(graphs, f)

    print(num_ver)

# if __name__ == '__main__':
#     p = cpu_count() - 1
#     print(p)
#     pool = Pool(processes = p)
#     pool.map(_make_graph, k.nums)

def make_graphs_one_at_a_time(num_ver, prefix, intervals, n):
    base_graph = graph_type(num_ver, graph_type.init_intervals(num_ver))
    print(n, 1)
    base_path = base_graph.make_christofides_route()
    print(n, 2)

    with open(prefix + k.get_path_name(num_ver, n), 'w') as f:
        pickle.dump(base_path, f)

    del base_path

    opt_path = base_graph.make_optimal_route()

    with open(prefix + k.get_opt_path_name(num_ver, n), 'w') as f:
        pickle.dump(opt_path, f)

    del opt_path

    for i in intervals:
        graph = base_graph.copy(i)
        with open(prefix + k.get_graph_name(i, num_ver, n), 'w') as f:
            pickle.dump(graph, f)
        print(n, 3, i)
        del graph

    del base_graph

    print(n)

for n in range(k.num_tests):
    if n > 40:
        make_graphs_one_at_a_time(40, graph_type.prefix(), graph_type.intervals(40), n)
