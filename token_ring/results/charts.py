import numpy as np
import matplotlib.pyplot as plt
import csv
import math
import ast

LOG_SCALE = False

data = {}

## open a benchmark file
def open_benchmark(filename, order=(0, 1, 2)):
    global LOG_SCALE

    ndim = len(order)

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')

        dims1 = []
        if ndim >= 2:
            dims2 = []
        if ndim >= 3:
            dims3 = []
        if ndim >= 4:
            raise RuntimeError("Not yet implemented")

        y_cpudata_mean = {}
        y_cpudata_dev = {}
        y_total_time = {}
        y_internal_time = {}

        for i, row in enumerate(spamreader):
            if i == 0:
                dimension_names = [row[i] for i in order]
            else:
                cpudata = ast.literal_eval(row[ndim])
                if cpudata is None:
                    pass
                else:
                    if LOG_SCALE:
                        cpudata_mean = np.average(np.log(cpudata))
                        cpudata_dev = np.std(np.log(cpudata))
                        total_time = math.log(int(row[ndim + 1]))
                        internal_time = math.log(int(row[ndim + 2]))
                    else:
                        cpudata_mean = np.average(cpudata)
                        cpudata_dev = np.std(cpudata)
                        total_time = int(row[ndim+1])
                        internal_time = int(row[ndim+2])

                    dim1 = row[order[0]]
                    if dim1 not in dims1:
                        dims1.append(dim1)
                    if dim1 not in y_cpudata_mean:
                        if ndim == 1:
                            y_cpudata_mean[dim1] = []
                            y_cpudata_dev[dim1] = []
                            y_total_time[dim1] = []
                            y_internal_time[dim1] = []
                        else:
                            y_cpudata_mean[dim1] = {}
                            y_cpudata_dev[dim1] = {}
                            y_total_time[dim1] = {}
                            y_internal_time[dim1] = {}

                    if ndim >= 2:
                        dim2 = row[order[1]]
                        if dim2 not in dims2:
                            dims2.append(dim2)
                        if dim2 not in y_cpudata_mean[dim1]:
                            if ndim == y_cpudata_mean[dim1]:
                                y_cpudata_mean[dim1][dim2] = []
                                y_cpudata_dev[dim1][dim2] = []
                                y_total_time[dim1][dim2] = []
                                y_internal_time[dim1][dim2] = []
                            else:
                                y_cpudata_mean[dim1][dim2] = {}
                                y_cpudata_dev[dim1][dim2] = {}
                                y_total_time[dim1][dim2] = {}
                                y_internal_time[dim1][dim2] = {}

                    if ndim >= 3:
                        dim3 = row[order[2]]
                        if dim3 not in dims3:
                            dims3.append(dim3)

                        if dim3 not in y_cpudata_mean[dim1][dim2]:
                            y_cpudata_mean[dim1][dim2][dim3] = []
                            y_cpudata_dev[dim1][dim2][dim3] = []
                            y_total_time[dim1][dim2][dim3] = []
                            y_internal_time[dim1][dim2][dim3] = []

                    if ndim == 1:
                        y_cpudata_mean[dim1].append(cpudata_mean)
                        y_cpudata_dev[dim1].append(cpudata_dev)
                        y_total_time[dim1].append(total_time)
                        y_internal_time[dim1].append(total_time)
                    elif ndim == 2:
                        y_cpudata_mean[dim1][dim2].append(cpudata_mean)
                        y_cpudata_dev[dim1][dim2].append(cpudata_dev)
                        y_total_time[dim1][dim2].append(total_time)
                        y_internal_time[dim1][dim2].append(total_time)
                    elif ndim == 3:
                        y_cpudata_mean[dim1][dim2][dim3].append(cpudata_mean)
                        y_cpudata_dev[dim1][dim2][dim3].append(cpudata_dev)
                        y_total_time[dim1][dim2][dim3].append(total_time)
                        y_internal_time[dim1][dim2][dim3].append(total_time)

        return dimension_names, y_cpudata_mean, y_cpudata_dev, y_total_time, y_internal_time

## compute the average/stdmin over the available iterations
def compute_averages(y, ndim):
    y_mean = {}
    y_std = {}
    for dim1 in y.keys():
        if ndim == 1:
            y_mean[dim1] = np.average(y[dim1])
            y_std[dim1] = np.std(y[dim1])
        else:
            y_mean[dim1] = {}
            y_std[dim1] = {}
            for dim2 in y[dim1].keys():
                if ndim == 2:
                    y_mean[dim1][dim2] = np.average(y[dim1][dim2])
                    y_std[dim1][dim2] = np.std(y[dim1][dim2])
                else:
                    y_mean[dim1][dim2] = {}
                    y_std[dim1][dim2]  = {}
                    for dim3 in y[dim1][dim2].keys():
                        y_mean[dim1][dim2][dim3] = np.average(y[dim1][dim2][dim3])
                        y_std[dim1][dim2][dim3] = np.std(y[dim1][dim2][dim3])
    return (y_mean, y_std)


def draw_3_dim(y, dimension_names, feature_names):

    for dim1 in y.keys():
        for dim2 in y[dim1].keys():
            xx = []
            yy_mean = []
            yy_dev = []
            for dim3 in y[dim1][dim2].keys():
                xx.append(dim3)
                yy_mean.append(averages[dim1][dim2][dim3])
                yy_dev.append(stds[dim1][dim2][dim3])


            plt.title(label=feature_names[i] + " in function of " + dimension_names[2])
            plt.errorbar(xx, yy_mean, yerr=yy_dev,
                         label=dimension_names[0] + " " + dim1 + ", " + dimension_names[1] + " " + dim2, elinewidth=1,
                         capsize=0)
        plt.legend(loc='upper left')
        plt.show()

dimension_names, \
y_cpudata_mean, y_cpudata_dev, y_total_time, y_internal_time\
    = open_benchmark("benchmark-astra-4096-4096-4096.csv", [2,1,0])

for i, name in enumerate(dimension_names):
    print("dim" + str(i+1) +": "+name)

feature_names = ["outer time (ms)", "inner time (ms)", "cpuload (%) mean", "cpuload (%) stdev"]
for i, y in enumerate([ y_total_time ]): #, y_internal_time, y_cpudata_mean]): # , y_total_time]): # , y_cpudata_mean, y_cpudata_dev]):
    print("############ "+feature_names[i])
    averages, stds = compute_averages(y, 3)
    print(averages)
    print(stds)

    draw_3_dim(y, dimension_names, feature_names)
