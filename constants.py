num_intervals = 9
num_tests = 50

nums = [40]

def min_num(num_ver):
    return num_ver - 1

def max_num(num_ver):
    return (num_ver * (num_ver - 1)) / 2

def intervals(num_ver):
    max_num_present = max_num(num_ver)
    min_num_present = min_num(num_ver)
    max_range = max_num_present - min_num_present
    return [((max_range * i) / (num_intervals - 1)) + min_num_present for i in range(num_intervals)] + \
        [min_num_present + (num_ver - 2)]

def get_graph_name(number, n):
    return 'graphs/graph' + str(number) + '_' + str(n) + '.pkl'

def get_path_name(n):
    return 'path/path' + str(n) + '.pkl'

def get_opt_path_name(n):
    return 'path/opt_path' + str(n) + '.pkl'

def get_BFI_name(number):
    return 'out/BFI' + str(number) + '.txt'

def get_cyclic_name(number):
    return 'out/cctp' + str(number) + '.txt'

def get_cbfi_name(number):
    return 'out/cbfi' + str(number) + '.txt'

def get_nn_name(number):
    return 'out/nn' + str(number) + '.txt'

def get_cnn_name(number):
    return 'out/cnn' + str(number) + '.txt'

def get_opt_nn_name(number):
    return 'out/opt_nn' + str(number) + '.txt'