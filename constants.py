num_intervals = 10
num_tests = 100

nums = [40]#range(30, 5, -5)

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

def get_graph_name(number, n, bonus = ''):
    return 'graphs/graph' + str(number) + '_' + str(n) + ('' if not bonus else '_' + str(bonus)) + '.pkl'

def get_path_name(n, bonus = ''):
    return 'path/path' + str(n) + ('' if not bonus else '_' + str(bonus)) + '.pkl'

def get_opt_path_name(n, bonus = ''):
    return 'path/opt_path' + str(n) + ('' if not bonus else '_' + str(bonus)) + '.pkl'

def get_BFI_name(number, bonus = ''):
    return 'out/BFI' + str(number) + ('' if not bonus else '_' + str(bonus)) + '.txt'

def get_cyclic_name(number, bonus = ''):
    return 'out/cctp' + str(number) + ('' if not bonus else '_' + str(bonus)) + '.txt'

def get_cbfi_name(number, bonus = ''):
    return 'out/cbfi' + str(number) + ('' if not bonus else '_' + str(bonus)) + '.txt'

def get_nn_name(number, bonus = ''):
    return 'out/nn' + str(number) + ('' if not bonus else '_' + str(bonus)) + '.txt'

def get_cnn_name(number, bonus = ''):
    return 'out/cnn' + str(number) + ('' if not bonus else '_' + str(bonus)) + '.txt'

def get_opt_nn_name(number, bonus = ''):
    return 'out/opt_nn' + str(number) + ('' if not bonus else '_' + str(bonus)) + '.txt'