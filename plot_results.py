import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d.axes3d import Axes3D
import pandas as pd
import numpy as np
import constants as k
from Generate import graph_type, GridGraph

prefix = graph_type.prefix()

nn_name, nn_colour, nn_worst = "Nearest Neighbour Average", "blue", "NN Worst"
cnn_name, cnn_colour, cnn_worst = "Hybrid Average", "green", 'Hybrid Worst'
opt_nn_name, opt_nn_colour, opt_nn_worst = "OPT Seeded Hybrid Average", "orange", 'OPT Hybrid Worst'
offline_name, offline_colour = "Offline OPT Average", "black"

x_label = '% Blocked Edges'

num_ver_range = k.nums

num_intervals = range(k.num_intervals)

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

best_nn_mean = []
best_mean_color_map = []

for index, num_ver in enumerate(num_ver_range):
    sizes.append(list(map(lambda x: x * 100, GridGraph.intervals(num_ver))))
    nn_mean.append(list(map(lambda x: x[0], list(nn_df[index][['mean']].values))))
    offline_mean.append(list(map(lambda x: x[0], list(offline_df[index][['mean']].values))))
    cnn_mean.append(list(map(lambda x: x[0], list(cnn_df[index][['mean']].values))))
    opt_nn_mean.append(list(map(lambda x: x[0], list(opt_nn_df[index][['mean']].values))))

temp_fig = plt.figure(0)
ax = temp_fig.add_subplot(111, projection='3d')
plt.suptitle(graph_type.name())

shapes = ['^', 'o', '*', 'x', 'v']

for index, num_ver in enumerate(num_ver_range):
    cnn_value = []
    cnn_size = []
    cnn_num_ver = []

    nn_value = []
    nn_size = []
    nn_num_ver = []

    for nn, cnn, size in zip(nn_mean[index], cnn_mean[index], sizes[index]):
        if nn > cnn:
            cnn_value.append(cnn)
            cnn_size.append(size)
            cnn_num_ver.append(num_ver)
        else:
            nn_value.append(cnn)
            nn_size.append(size)
            nn_num_ver.append(num_ver)

    if not index:
        ax.scatter(cnn_size, cnn_num_ver, cnn_value, c = cnn_colour, marker = shapes[index], label = cnn_name, depthshade = False)
        ax.scatter(nn_size, nn_num_ver, nn_value, c = nn_colour, marker = shapes[index], label = nn_name, depthshade = False)
    else:
        ax.scatter(cnn_size, cnn_num_ver, cnn_value, c = cnn_colour, marker = shapes[index], depthshade = False)
        ax.scatter(nn_size, nn_num_ver, nn_value, c = nn_colour, marker = shapes[index], depthshade = False)

ax.set_yticks(num_ver_range)

ax.set_zlabel('Distance')
ax.set_ylabel('N')
ax.set_xlabel(x_label)

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.15,
                 box.width, box.height * 0.85])

ax.legend(loc = 'upper left', bbox_to_anchor = (0.0, -0.15),
          fancybox = True, shadow = True, ncol = 2)

ax.view_init(azim = -80)

# for index, num_ver in enumerate(num_ver_range):
#     temp_fig = plt.figure(index)
#
#     ax = temp_fig.add_subplot(111)
#     plt.suptitle(graph_type.name(), y=0.98, fontsize=14)
#     plt.title('n = ' + str(num_ver), fontsize=11)
#     ax.plot(sizes[index], nn_mean[index], color = nn_colour, label = nn_name)
#     ax.plot(sizes[index], offline_mean[index], color = offline_colour, label = offline_name)
#     ax.plot(sizes[index], cnn_mean[index], color = cnn_colour, label = cnn_name)
#     ax.plot(sizes[index], opt_nn_mean[index], color = opt_nn_colour, label = opt_nn_name)
#
#     plt.ylabel('Distance')
#     plt.xlabel(x_label)
#
#     box = ax.get_position()
#     ax.set_position([box.x0, box.y0 + box.height * 0.15,
#                      box.width, box.height * 0.85])
#
#     ax.legend(loc = 'upper left', bbox_to_anchor = (0.0, -0.15),
#               fancybox = True, shadow = True, ncol = 2)

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

# for index, num_ver in enumerate(num_ver_range):
#     temp_fig = plt.figure(index + len(num_ver_range))
#
#     ax = temp_fig.add_subplot(111)
#     plt.suptitle(graph_type.name(), y=0.98, fontsize=14)
#     plt.title('n = ' + str(num_ver), fontsize=11)
#     ax.plot(sizes[index], nn_max_ratio[index], color = nn_colour, label = nn_worst, ls = '--')
#     ax.plot(sizes[index], cnn_max_ratio[index], color = cnn_colour, label = cnn_worst, ls = '--')
#     ax.plot(sizes[index], opt_nn_max_ratio[index], color = opt_nn_colour, label = opt_nn_worst, ls = '--')
#
#     ax.plot(sizes[index], nn_ratio[index], color = nn_colour, label = nn_name, ls = '-')
#     ax.plot(sizes[index], cnn_ratio[index], color = cnn_colour, label = cnn_name, ls = '-')
#     ax.plot(sizes[index], opt_nn_ratio[index], color = opt_nn_colour, label = opt_nn_name, ls = '-')
#
#     plt.ylabel('Ratio to OPT')
#     plt.xlabel(x_label)
#
#     box = ax.get_position()
#     ax.set_position([box.x0, box.y0 + box.height * 0.2,
#                      box.width, box.height * 0.8])
#
#     ax.legend(loc = 'upper left', bbox_to_anchor = (0.0, -0.15),
#               fancybox = True, shadow = True, ncol = 2)
plt.show()
