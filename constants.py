num_intervals = 9
num_tests = 50

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

def get_cctp_name(number):
    return 'out/cctp' + str(number) + '.txt'

def get_cbfi_name(number):
    return 'out/cbfi' + str(number) + '.txt'

def get_nn_name(number):
    return 'out/nn' + str(number) + '.txt'