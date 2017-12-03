import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import pandas as pd
import constants as k
from Generate import graph_type

prefix = graph_type.prefix()

nn_name, nn_colour = "NN", "blue"
cnn_name, cnn_colour = "CNN", "green"
opt_nn_name, opt_nn_colour = "OPT NN", "orange"
offline_name, offline_colour = "OFFLINE", "black"

num_ver_range = k.nums

num_intervals = range(k.num_intervals + graph_type.bonus_intervals())

nn_df = []
if not prefix:
    cyclic_df = []
offline_df = []
cnn_df = []
opt_nn_df = []
for num_ver in num_ver_range:
    nn_df.append(pd.read_csv(prefix + k.get_nn_name(num_ver)))
    opt_nn_df.append(pd.read_csv(prefix + k.get_opt_nn_name(num_ver)))
    offline_df.append(pd.read_csv(prefix + k.get_BFI_name(num_ver)))
    cnn_df.append(pd.read_csv(prefix + k.get_cnn_name(num_ver)))


sizes = []
nn_mean = []
offline_mean = []
cnn_mean = []
opt_nn_mean = []

for index, num_ver in enumerate(num_ver_range):
    sizes.append(list(map(lambda x: x[0], list(nn_df[index][['num_ver']].values))))
    nn_mean.append(list(map(lambda x: x[0], list(nn_df[index][['mean']].values))))
    offline_mean.append(list(map(lambda x: x[0], list(offline_df[index][['mean']].values))))
    cnn_mean.append(list(map(lambda x: x[0], list(cnn_df[index][['mean']].values))))
    opt_nn_mean.append(list(map(lambda x: x[0], list(opt_nn_df[index][['mean']].values))))

for index, num_ver in enumerate(num_ver_range):
    temp_fig = plt.figure(index)

    ax = temp_fig.add_subplot(111)
    ax.invert_xaxis()
    plt.title('n = ' + str(num_ver) + ' ' + graph_type.name())
    ax.plot(sizes[index], nn_mean[index], color = nn_colour, label = nn_name)
    ax.plot(sizes[index], offline_mean[index], color = offline_colour, label = offline_name)
    ax.plot(sizes[index], cnn_mean[index], color = cnn_colour, label = cnn_name)
    ax.plot(sizes[index], opt_nn_mean[index], color = opt_nn_colour, label = opt_nn_name)
    plt.legend(loc=2)

nn_max_ratio = []
cnn_max_ratio = []
opt_nn_max_ratio = []

for index, num_ver in enumerate(num_ver_range):
    nn_max_ratio.append(list(map(lambda x: x[0], list(nn_df[index][['max_ratio']].values))))
    cnn_max_ratio.append(list(map(lambda x: x[0], list(cnn_df[index][['max_ratio']].values))))
    opt_nn_max_ratio.append(list(map(lambda x: x[0], list(opt_nn_df[index][['max_ratio']].values))))

nn_ratio = []
cnn_ratio = []
opt_nn_ratio = []

for index, num_ver in enumerate(num_ver_range):
    nn_ratio.append([nn_mean[index][i]/offline_mean[index][i] for i in range(len(offline_mean[index]))])
    cnn_ratio.append([cnn_mean[index][i]/offline_mean[index][i] for i in range(len(offline_mean[index]))])
    opt_nn_ratio.append([opt_nn_mean[index][i]/offline_mean[index][i] for i in range(len(offline_mean[index]))])

for index, num_ver in enumerate(num_ver_range):
    temp_fig = plt.figure(index + len(num_ver_range))

    ax = temp_fig.add_subplot(111)
    ax.invert_xaxis()
    plt.title('n = ' + str(num_ver) + ' ' + graph_type.name())
    ax.plot(sizes[index], nn_max_ratio[index], color = nn_colour, label = nn_name, ls = '--')
    ax.plot(sizes[index], cnn_max_ratio[index], color = cnn_colour, label = cnn_name, ls = '--')
    ax.plot(sizes[index], opt_nn_max_ratio[index], color = opt_nn_colour, label = opt_nn_name, ls = '--')

    ax.plot(sizes[index], nn_ratio[index], color = nn_colour, label = nn_name, ls = '-')
    ax.plot(sizes[index], cnn_ratio[index], color = cnn_colour, label = cnn_name, ls = '-')
    ax.plot(sizes[index], opt_nn_ratio[index], color = opt_nn_colour, label = opt_nn_name, ls = '-')
    plt.legend(loc=2)

plt.show()
