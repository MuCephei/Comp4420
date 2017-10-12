import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D, get_test_data
import pandas as pd
import constants as k

num_ver_range = range(18, 5, -1)

nn_df = []
cctp_df = []
cbfi_df = []
for num_ver in num_ver_range:
    nn_df.append(pd.read_csv(k.get_nn_name(num_ver)))
    cctp_df.append(pd.read_csv(k.get_cctp_name(num_ver)))
    cbfi_df.append(pd.read_csv(k.get_cbfi_name(num_ver)))

sizes = []
nn_mean = []
cctp_mean = []
cbfi_mean = []

for index, num_ver in enumerate(num_ver_range):
    sizes.append(list(map(lambda x: x[0], list(nn_df[index][['num_ver']].values))))
    nn_mean.append(list(map(lambda x: x[0], list(nn_df[index][['mean']].values))))
    cctp_mean.append(list(map(lambda x: x[0], list(cctp_df[index][['mean']].values))))
    cbfi_mean.append(list(map(lambda x: x[0], list(cbfi_df[index][['mean']].values))))

fig = plt.figure()
ax_nn_cctp = fig.add_subplot(131, projection='3d')
ax_nn_cbfi = fig.add_subplot(132, projection='3d')
ax_cctp_cbfi = fig.add_subplot(133, projection = '3d')

X = sizes
Y = [[num_ver] * 10 for num_ver in num_ver_range]

ax_nn_cctp.plot_wireframe(X, Y, nn_mean, color='blue')
ax_nn_cctp.plot_wireframe(X, Y, cctp_mean, color='red')

ax_nn_cbfi.plot_wireframe(X, Y, nn_mean, color='blue')
ax_nn_cbfi.plot_wireframe(X, Y, cbfi_mean, color='green')

ax_cctp_cbfi.plot_wireframe(X, Y, cctp_mean, color='red')
ax_cctp_cbfi.plot_wireframe(X, Y, cbfi_mean, color='green')

plt.show()
