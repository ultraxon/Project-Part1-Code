import numpy as np
import re
import datetime
import math
import pandas as pd
from matplotlib import pyplot as plt


def main():
    k_order = 1
    f_datas = open('./Datas/IBM.txt')
    next(f_datas)
    dates = [0]
    prices = [0]
    for line in f_datas:
        data_list = re.split(',', line)
        data_list[0] = datetime.datetime.strptime(data_list[0], '%Y-%m-%d')
        data_list[1] = float(data_list[1][:-1])
        dates.append(data_list[0])
        prices.append(data_list[1])
    f_datas.close()
    diff = [0]
    for i in range(2, len(prices)):
        diff.append(prices[i]-prices[i-1])

    MSE_all = [10000]
    ALL_ESTIMATED_DIFFS = [[0]]
    with open('./Results/res_invGamma_prior.txt', 'r') as f:
        for line in f:
            line = eval(line)
            p = len(line) - 2
            square_error = line[-1]
            estimate_diff = diff[:p + 1]
            while len(estimate_diff) < len(diff):
                # noise = [0]
                next_data = 0
                for i in range(1, p + 1):
                    next_data += line[i] * estimate_diff[len(estimate_diff)- i]
                next_data += line[0]
                noises = np.random.normal(0, math.sqrt(square_error),1)
                next_data += noises[0]
                estimate_diff.append(next_data)
            ALL_ESTIMATED_DIFFS.append(estimate_diff)
    print(MSE_all)
    for single_diff_group in ALL_ESTIMATED_DIFFS[1:]:
        print(len(single_diff_group))
        prices_estimated = prices[:2]
        for i in range(2,len(prices)):
            prices_estimated.append(prices[i-1] + single_diff_group[i-1])
        MSE = sum([(y - x)**2
                       for x, y in zip(prices_estimated[1:], prices[1:])]) / (
                           (len(prices_estimated) - 1))
        MSE_all.append(MSE)
    print(MSE_all)
    best_num = MSE_all.index(min(MSE_all))
    print('BEST MODEL:AR(%s)' % best_num)
    print('MSE:', MSE_all[best_num])
    selected_diff = ALL_ESTIMATED_DIFFS[best_num]
    data_frame = pd.DataFrame(np.array([diff[1:], selected_diff[1:]]).T,
                              columns=['orig_series', 'estimated_series'])
    data_frame.plot(alpha=0.85)
    plt.show()
    plt.clf()
    prices_estimated = prices[:2]
    for i in range(2,len(prices)):
        prices_estimated.append(prices[i-1] + selected_diff[i-1])
#    for single_diff in selected_diff[1:]:
#        prices_estimated.append(prices_estimated[-1] + single_diff)

    data_frame2 = pd.DataFrame(np.array([prices[1:], prices_estimated[1:]]).T,
                              columns=['orig_series', 'estimated_series'])
    data_frame2.plot(alpha=0.85)
    plt.show()
    plt.clf()

    errors = [y - x for x, y in zip(prices[1:], prices_estimated[1:])]
    max_error = max(errors)
    min_error = min(errors)
    ranges = np.linspace(min_error, max_error, 50)
    frequencies = []
    for i in range(0, len(ranges) - 1):
        count = 0
        for data in errors:
            if ranges[i] <= data < ranges[i + 1]:
                count += 1
        frequencies.append(count)
    plt.bar(ranges[:-1],
            frequencies,
            width=ranges[1] - ranges[0],
            edgecolor='black')
    plt.show()


if __name__ == '__main__':
    main()