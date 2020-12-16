'''
这是对考察路段及其前后路段采用CTM模型的结果
'''
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

k_j = 70  # 拥堵密度
Q_max = 1450  # 单车道最大通行流量
P_j = 5 / 8  # 主干道优先级系数
P_jj = 3 / 8  # 匝道优先级系数
# 以下为各路段的长度、能够容纳的最大车辆数、5min时段各路段的最大流量
load1 = 527.386131  # 路段1（干道）长度
load2 = 274.635256  # 路段2（入口匝道）长度
load3 = 230.382884  # 路段3（考察干道）长度
load4 = 456.274547  # 路段4（干道）长度
load5 = 456.273355  # 路段5（出口匝道）长度

n1 = int(k_j * load1 * 3 / 1000)
n2 = int(k_j * load2 * 2 / 1000)
n3 = int(k_j * load3 * 5 / 1000)
n4 = int(k_j * load4 * 3 / 1000)
n5 = int(k_j * load5 * 2 / 1000)

Q1_5min = int(Q_max / 12 * 3)
Q2_5min = int(Q_max / 12 * 2)
Q3_5min = int(Q_max / 12 * 5)
Q4_5min = int(Q_max / 12 * 3)
Q5_5min = int(Q_max / 12 * 2)
############################
# 记录CTM模型运算数据
q_ctm_7_9 = np.zeros([5, 24])
n_ctm_7_9 = np.zeros([5, 24])
y_i_7_9 = np.zeros([2, 24])  # y_i
y_ii_7_9 = np.zeros([2, 24])  # y_(i+1)

q_ctm_18_20 = np.zeros([5, 24])
n_ctm_18_20 = np.zeros([5, 24])
y_i_18_20 = np.zeros([2, 24])  # y_i
y_ii_18_20 = np.zeros([2, 24])  # y_(i+1)

q_ctm_12_14 = np.zeros([5, 24])
n_ctm_12_14 = np.zeros([5, 24])
y_i_12_14 = np.zeros([2, 24])  # y_i
y_ii_12_14 = np.zeros([2, 24])  # y_(i+1)

###################
# 记录真实的数据
# 早高峰，7点到9点
q_7_9 = np.zeros([5, 24])
n_7_9 = np.zeros([5, 24])
v_7_9 = np.zeros([5, 24])
load_in_7_9 = np.zeros([5, 24])
load_out_7_9 = np.zeros([5, 24])
s_7_9 = np.zeros([5, 24])
# 晚高峰，18点到20点
q_18_20 = np.zeros([5, 24])
n_18_20 = np.zeros([5, 24])
v_18_20 = np.zeros([5, 24])
load_in_18_20 = np.zeros([5, 24])
load_out_18_20 = np.zeros([5, 24])
s_18_20 = np.zeros([5, 24])
# 平峰，12点到14点
q_12_14 = np.zeros([5, 24])
n_12_14 = np.zeros([5, 24])
v_12_14 = np.zeros([5, 24])
load_in_12_14 = np.zeros([5, 24])
load_out_12_14 = np.zeros([5, 24])
s_12_14 = np.zeros([5, 24])
# 开始统计前一个时间段数据记录
nn_7_9 = np.zeros(5)
in_7_9 = np.zeros(5)
out_7_9 = np.zeros(5)
nn_18_20 = np.zeros(5)
in_18_20 = np.zeros(5)
out_18_20 = np.zeros(5)
nn_12_14 = np.zeros(5)
in_12_14 = np.zeros(5)
out_12_14 = np.zeros(5)

# 获取真实的数据
with open(r'C:\Users\yezhihui\Desktop\交通流理论期末大作业\期末报告要求及数据\CTM_SH_191204.csv', 'r') as f:
    reader = csv.reader(f)
    #    print(type(reader))
    result = list(reader)
    for i in range(1, len(result)):
        time = result[i][0].split(' ')
        hour = time[1].split(':')
        fnode = result[i][2]
        tnode = result[i][3]
        if (float(hour[0]) == 6 and float(hour[1]) == 55):
            if (int(fnode) == 31010100000018 and int(tnode) == 31010100000119):
                nn_7_9[0] = float(result[i][6])  # 记录6：55时刻的路段1车辆数
                in_7_9[0] = float(result[i][7])
                out_7_9[0] = float(result[i][8])
            if (int(fnode) == 31010100000118 and int(tnode) == 31010100000119):
                nn_7_9[1] = float(result[i][6])  # 记录……
                in_7_9[1] = float(result[i][7])
                out_7_9[1] = float(result[i][8])
            if (int(fnode) == 31010100000119 and int(tnode) == 31010100000086):
                nn_7_9[2] = float(result[i][6])  # 记录……
                in_7_9[2] = float(result[i][7])
                out_7_9[2] = float(result[i][8])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010600000065):
                nn_7_9[3] = float(result[i][6])  # 记录……
                in_7_9[3] = float(result[i][7])
                out_7_9[3] = float(result[i][8])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010100000065):
                nn_7_9[4] = float(result[i][6])  # 记录……
                in_7_9[4] = float(result[i][7])
                out_7_9[4] = float(result[i][8])

        if (float(hour[0]) == 17 and float(hour[1]) == 55):
            if (int(fnode) == 31010100000018 and int(tnode) == 31010100000119):
                nn_18_20[0] = float(result[i][6])  # 记录6：55时刻的路段1车辆数
                in_18_20[0] = float(result[i][7])
                out_18_20[0] = float(result[i][8])
            if (int(fnode) == 31010100000118 and int(tnode) == 31010100000119):
                nn_18_20[1] = float(result[i][6])  # 记录……
                in_18_20[1] = float(result[i][7])
                out_18_20[1] = float(result[i][8])
            if (int(fnode) == 31010100000119 and int(tnode) == 31010100000086):
                nn_18_20[2] = float(result[i][6])  # 记录……
                in_18_20[2] = float(result[i][7])
                out_18_20[2] = float(result[i][8])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010600000065):
                nn_18_20[3] = float(result[i][6])  # 记录……
                in_18_20[3] = float(result[i][7])
                out_18_20[3] = float(result[i][8])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010100000065):
                nn_18_20[4] = float(result[i][6])  # 记录……
                in_18_20[4] = float(result[i][7])
                out_18_20[4] = float(result[i][8])

        if (float(hour[0]) == 11 and float(hour[1]) == 55):
            if (int(fnode) == 31010100000018 and int(tnode) == 31010100000119):
                nn_12_14[0] = float(result[i][6])  # 记录6：55时刻的路段1车辆数
                in_12_14[0] = float(result[i][7])
                out_12_14[0] = float(result[i][8])
            if (int(fnode) == 31010100000118 and int(tnode) == 31010100000119):
                nn_12_14[1] = float(result[i][6])  # 记录……
                in_12_14[1] = float(result[i][7])
                out_12_14[1] = float(result[i][8])
            if (int(fnode) == 31010100000119 and int(tnode) == 31010100000086):
                nn_12_14[2] = float(result[i][6])  # 记录……
                in_12_14[2] = float(result[i][7])
                out_12_14[2] = float(result[i][8])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010600000065):
                nn_12_14[3] = float(result[i][6])  # 记录……
                in_12_14[3] = float(result[i][7])
                out_12_14[3] = float(result[i][8])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010100000065):
                nn_12_14[4] = float(result[i][6])  # 记录……
                in_12_14[4] = float(result[i][7])
                out_12_14[4] = float(result[i][8])

        if (float(hour[0]) == 7):
            if (int(fnode) == 31010100000018 and int(tnode) == 31010100000119):
                n_7_9[0][int(float(hour[1]) / 5)] = float(result[i][6])
                v_7_9[0][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_7_9[0][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_7_9[0][int(float(hour[1]) / 5)] = float(result[i][8])
                s_7_9[0][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000118 and int(tnode) == 31010100000119):
                n_7_9[1][int(float(hour[1]) / 5)] = float(result[i][6])
                v_7_9[1][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_7_9[1][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_7_9[1][int(float(hour[1]) / 5)] = float(result[i][8])
                s_7_9[1][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000119 and int(tnode) == 31010100000086):
                n_7_9[2][int(float(hour[1]) / 5)] = float(result[i][6])
                v_7_9[2][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_7_9[2][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_7_9[2][int(float(hour[1]) / 5)] = float(result[i][8])
                s_7_9[2][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010600000065):
                n_7_9[3][int(float(hour[1]) / 5)] = float(result[i][6])
                v_7_9[3][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_7_9[3][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_7_9[3][int(float(hour[1]) / 5)] = float(result[i][8])
                s_7_9[3][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010100000065):
                n_7_9[4][int(float(hour[1]) / 5)] = float(result[i][6])
                v_7_9[4][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_7_9[4][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_7_9[4][int(float(hour[1]) / 5)] = float(result[i][8])
                s_7_9[4][int(float(hour[1]) / 5)] = float(result[i][4])

        if (float(hour[0]) == 8):
            if (int(fnode) == 31010100000018 and int(tnode) == 31010100000119):
                n_7_9[0][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_7_9[0][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_7_9[0][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_7_9[0][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_7_9[0][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000118 and int(tnode) == 31010100000119):
                n_7_9[1][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_7_9[1][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_7_9[1][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_7_9[1][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_7_9[1][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000119 and int(tnode) == 31010100000086):
                n_7_9[2][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_7_9[2][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_7_9[2][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_7_9[2][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_7_9[2][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010600000065):
                n_7_9[3][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_7_9[3][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_7_9[3][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_7_9[3][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_7_9[3][int(float(hour[1]) / 5) + 12] = float(result[i][4])

            if (int(fnode) == 31010100000086 and int(tnode) == 31010100000065):
                n_7_9[4][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_7_9[4][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_7_9[4][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_7_9[4][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_7_9[4][int(float(hour[1]) / 5) + 12] = float(result[i][4])

        if (float(hour[0]) == 18):
            if (int(fnode) == 31010100000018 and int(tnode) == 31010100000119):
                n_18_20[0][int(float(hour[1]) / 5)] = float(result[i][6])
                v_18_20[0][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_18_20[0][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_18_20[0][int(float(hour[1]) / 5)] = float(result[i][8])
                s_18_20[0][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000118 and int(tnode) == 31010100000119):
                n_18_20[1][int(float(hour[1]) / 5)] = float(result[i][6])
                v_18_20[1][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_18_20[1][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_18_20[1][int(float(hour[1]) / 5)] = float(result[i][8])
                s_18_20[1][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000119 and int(tnode) == 31010100000086):
                n_18_20[2][int(float(hour[1]) / 5)] = float(result[i][6])
                v_18_20[2][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_18_20[2][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_18_20[2][int(float(hour[1]) / 5)] = float(result[i][8])
                s_18_20[2][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010600000065):
                n_18_20[3][int(float(hour[1]) / 5)] = float(result[i][6])
                v_18_20[3][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_18_20[3][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_18_20[3][int(float(hour[1]) / 5)] = float(result[i][8])
                s_18_20[3][int(float(hour[1]) / 5)] = float(result[i][4])

            if (int(fnode) == 31010100000086 and int(tnode) == 31010100000065):
                n_18_20[4][int(float(hour[1]) / 5)] = float(result[i][6])
                v_18_20[4][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_18_20[4][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_18_20[4][int(float(hour[1]) / 5)] = float(result[i][8])
                s_18_20[4][int(float(hour[1]) / 5)] = float(result[i][4])

        if (float(hour[0]) == 19):
            if (int(fnode) == 31010100000018 and int(tnode) == 31010100000119):
                n_18_20[0][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_18_20[0][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_18_20[0][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_18_20[0][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_18_20[0][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000118 and int(tnode) == 31010100000119):
                n_18_20[1][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_18_20[1][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_18_20[1][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_18_20[1][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_18_20[1][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000119 and int(tnode) == 31010100000086):
                n_18_20[2][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_18_20[2][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_18_20[2][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_18_20[2][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_18_20[2][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010600000065):
                n_18_20[3][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_18_20[3][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_18_20[3][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_18_20[3][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_18_20[3][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010100000065):
                n_18_20[4][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_18_20[4][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_18_20[4][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_18_20[4][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_18_20[4][int(float(hour[1]) / 5) + 12] = float(result[i][4])

        if (float(hour[0]) == 12):
            if (int(fnode) == 31010100000018 and int(tnode) == 31010100000119):
                n_12_14[0][int(float(hour[1]) / 5)] = float(result[i][6])
                v_12_14[0][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_12_14[0][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_12_14[0][int(float(hour[1]) / 5)] = float(result[i][8])
                s_12_14[0][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000118 and int(tnode) == 31010100000119):
                n_12_14[1][int(float(hour[1]) / 5)] = float(result[i][6])
                v_12_14[1][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_12_14[1][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_12_14[1][int(float(hour[1]) / 5)] = float(result[i][8])
                s_12_14[1][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000119 and int(tnode) == 31010100000086):
                n_12_14[2][int(float(hour[1]) / 5)] = float(result[i][6])
                v_12_14[2][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_12_14[2][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_12_14[2][int(float(hour[1]) / 5)] = float(result[i][8])
                s_12_14[2][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010600000065):
                n_12_14[3][int(float(hour[1]) / 5)] = float(result[i][6])
                v_12_14[3][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_12_14[3][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_12_14[3][int(float(hour[1]) / 5)] = float(result[i][8])
                s_12_14[3][int(float(hour[1]) / 5)] = float(result[i][4])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010100000065):
                n_12_14[4][int(float(hour[1]) / 5)] = float(result[i][6])
                v_12_14[4][int(float(hour[1]) / 5)] = float(result[i][5])
                load_in_12_14[4][int(float(hour[1]) / 5)] = float(result[i][7])
                load_out_12_14[4][int(float(hour[1]) / 5)] = float(result[i][8])
                s_12_14[4][int(float(hour[1]) / 5)] = float(result[i][4])

        if (float(hour[0]) == 13):
            if (int(fnode) == 31010100000018 and int(tnode) == 31010100000119):
                n_12_14[0][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_12_14[0][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_12_14[0][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_12_14[0][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_12_14[0][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000118 and int(tnode) == 31010100000119):
                n_12_14[1][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_12_14[1][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_12_14[1][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_12_14[1][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_12_14[1][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000119 and int(tnode) == 31010100000086):
                n_12_14[2][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_12_14[2][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_12_14[2][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_12_14[2][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_12_14[2][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010600000065):
                n_12_14[3][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_12_14[3][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_12_14[3][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_12_14[3][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_12_14[3][int(float(hour[1]) / 5) + 12] = float(result[i][4])
            if (int(fnode) == 31010100000086 and int(tnode) == 31010100000065):
                n_12_14[4][int(float(hour[1]) / 5) + 12] = float(result[i][6])
                v_12_14[4][int(float(hour[1]) / 5) + 12] = float(result[i][5])
                load_in_12_14[4][int(float(hour[1]) / 5) + 12] = float(result[i][7])
                load_out_12_14[4][int(float(hour[1]) / 5) + 12] = float(result[i][8])
                s_12_14[4][int(float(hour[1]) / 5) + 12] = float(result[i][4])

###################################################################################################
# 早高峰结果计算
# 格林希尔治模型，求该密度下最大通行流量
Q_1 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_7_9[0] / 3 / load1 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
Q_2 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_7_9[1] / 2 / load2 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))
Q_3 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_7_9[2] / 5 / load3 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 5))
Q_4 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_7_9[3] / 3 / load4 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
Q_5 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_7_9[4] / 2 / load5 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))

y_i_7_9[0][0] = min([nn_7_9[0], min(Q_1, Q_3), (n3 - nn_7_9[2])])  # 计算路段1的流出量
y_i_7_9[1][0] = min([nn_7_9[1], min(Q_2, Q_3), (n3 - nn_7_9[2])])  # 计算路段2的流出量

if (y_i_7_9[0][0] + y_i_7_9[1][0] > n3 - nn_7_9[2]):  # 供应小于需求,考虑优先级
    y_i_7_9[0][0] = int(P_j * (n3 - nn_7_9[2]))
    y_i_7_9[1][0] = (n3 - nn_7_9[2]) - y_i_7_9[0][0]
    if (y_i_7_9[0][0] > nn_7_9[0]):  # 干道分配量过大,重新调整
        y_i_7_9[0][0] = nn_7_9[0]
        y_i_7_9[1][0] = n3 - nn_7_9[2] - nn_7_9[0]
    if (y_i_7_9[1][0] > nn_7_9[1]):  # 支路分配量过大，重新调整分配量
        y_i_7_9[1][0] = nn_7_9[1]
        y_i_7_9[0][0] = n3 - nn_7_9[2] - nn_7_9[1]

# 流出量不用考虑流量的具体流向，只要求知道能够流出的量的多少
y_ii_7_9[0][0] = min([nn_7_9[2], min(Q_3, Q_4), (n4 - nn_7_9[3])])  # 计算路段3流向路段4的流出量
y_ii_7_9[1][0] = min([nn_7_9[2], min(Q_3, Q_5), (n5 - nn_7_9[4])])  # 计算路段3流向路段5的流出量
if (y_ii_7_9[0][0] + y_ii_7_9[1][0] > nn_7_9[2]):  # 当供过于求时，路段3内全部车辆都流出
    y_ii_7_9[0][0] = int(P_j * nn_7_9[2])
    y_ii_7_9[1][0] = nn_7_9[3] - y_ii_7_9[0][0]
    if (y_ii_7_9[0][0] > (n4 - nn_7_9[3])):
        y_ii_7_9[0][0] = n4 - nn_7_9[3]
        y_ii_7_9[1][0] = nn_7_9[2] - y_ii_7_9[0][0]
        pass
    if (y_ii_7_9[1][0] > (n5 - nn_7_9[4])):
        y_ii_7_9[1][0] = n5 - nn_7_9[4]
        y_ii_7_9[0][0] = nn_7_9[2] - y_ii_7_9[1][0]
        pass

# 计算下一时刻各元胞内的车辆数
n_ctm_7_9[0][0] = min(n1, max(0, nn_7_9[0] - y_i_7_9[0][0] + max(0, in_7_9[0] - out_7_9[0])))  # 原有车辆-离开车辆+到达车辆
n_ctm_7_9[1][0] = min(n2, max(0, nn_7_9[1] - y_i_7_9[1][0] + max(0, in_7_9[1] - out_7_9[1])))
n_ctm_7_9[2][0] = min(n3, nn_7_9[2] + y_i_7_9[0][0] + y_i_7_9[1][0] - y_ii_7_9[0][0] - y_ii_7_9[1][0])  # 计算路段3的车辆数
n_ctm_7_9[3][0] = min(n4, max(0, nn_7_9[3] + y_ii_7_9[0][0] - max(0, out_7_9[3] - in_7_9[3])))
n_ctm_7_9[4][0] = min(n5, max(0, nn_7_9[4] + y_ii_7_9[1][0] - max(0, out_7_9[4] + in_7_9[4])))

for i in range(1, 24):
    # 下一时刻的最大通行量与上一时刻的密度有关
    Q_1 = max(0,
              int((-Q_max / (k_j / 2) ** 2 * (n_ctm_7_9[0][i - 1] / 3 / load1 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
    Q_2 = max(0,
              int((-Q_max / (k_j / 2) ** 2 * (n_ctm_7_9[1][i - 1] / 2 / load2 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))
    Q_3 = max(0,
              int((-Q_max / (k_j / 2) ** 2 * (n_ctm_7_9[2][i - 1] / 5 / load3 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 5))
    Q_4 = max(0,
              int((-Q_max / (k_j / 2) ** 2 * (n_ctm_7_9[3][i - 1] / 3 / load4 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
    Q_5 = max(0,
              int((-Q_max / (k_j / 2) ** 2 * (n_ctm_7_9[4][i - 1] / 2 / load5 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))

    y_i_7_9[0][i] = min([n_ctm_7_9[0][i - 1], min(Q_1, Q_3), (n3 - n_ctm_7_9[2][i - 1])])  # 计算路段1的流出量
    y_i_7_9[1][i] = min([n_ctm_7_9[1][i - 1], min(Q_2, Q_3), (n3 - n_ctm_7_9[2][i - 1])])  # 计算路段2的流出量
    if (y_i_7_9[0][i] + y_i_7_9[1][i] > n3 - n_ctm_7_9[2][i - 1]):  # 供应小于需求,考虑优先级
        y_i_7_9[0][i] = int(P_j * (n3 - n_ctm_7_9[2][i - 1]))
        y_i_7_9[1][i] = (n3 - n_ctm_7_9[2][i - 1]) - y_i_7_9[0][i]
        if (y_i_7_9[0][i] > n_ctm_7_9[0][i - 1]):  # 干道分配量过大,重新调整
            y_i_7_9[0][i] = n_ctm_7_9[0][i - 1]
            y_i_7_9[1][i] = n3 - n_ctm_7_9[2][i - 1] - n_ctm_7_9[0][i - 1]
        if (y_i_7_9[1][i] > n_ctm_7_9[1][i - 1]):  # 支路分配量过大，重新调整分配量
            y_i_7_9[1][i] = n_ctm_7_9[1][i - 1]
            y_i_7_9[0][i] = n3 - n_ctm_7_9[2][i - 1] - n_ctm_7_9[1][i - 1]

    y_ii_7_9[0][i] = min([n_ctm_7_9[2][i - 1], min(Q_3, Q_4), (n4 - n_ctm_7_9[3][i - 1])])  # 计算路段3流向路段4的流出量
    y_ii_7_9[1][i] = min([n_ctm_7_9[2][i - 1], min(Q_3, Q_5), (n5 - n_ctm_7_9[4][i - 1])])  # 计算路段3流向路段5的流出量
    if (y_ii_7_9[0][i] + y_ii_7_9[1][i] > n_ctm_7_9[2][i - 1]):  # 当供过于求时，路段3全部车辆都流出
        y_ii_7_9[0][i] = int(P_j * n_ctm_7_9[2][i - 1])
        y_ii_7_9[1][i] = n_ctm_7_9[2][i - 1] - y_ii_7_9[0][i]
        if (y_ii_7_9[0][i] > (n4 - n_ctm_7_9[3][i - 1])):
            y_ii_7_9[0][i] = n4 - n_ctm_7_9[3][i - 1]
            y_ii_7_9[1][i] = n_ctm_7_9[2][i - 1] - y_ii_7_9[0][i]
            pass
        if (y_ii_7_9[1][i] > (n5 - n_ctm_7_9[4][i - 1])):
            y_ii_7_9[1][i] = n5 - n_ctm_7_9[4][i - 1]
            y_ii_7_9[0][i] = n_ctm_7_9[2][i - 1] - y_ii_7_9[1][i]
            pass

    n_ctm_7_9[0][i] = min(n1, max(0, n_ctm_7_9[0][i - 1] - y_i_7_9[0][i] + max(0,
                                                                               load_in_7_9[0][i - 1] - load_out_7_9[0][
                                                                                   i - 1])))
    n_ctm_7_9[1][i] = min(n2, max(0, n_ctm_7_9[1][i - 1] - y_i_7_9[1][i] + max(0,
                                                                               load_in_7_9[1][i - 1] - load_out_7_9[1][
                                                                                   i - 1])))
    n_ctm_7_9[2][i] = min(n3, n_ctm_7_9[2][i - 1] + y_i_7_9[0][i] + y_i_7_9[1][i] - y_ii_7_9[0][i] - y_ii_7_9[1][
        i])  # 计算路段3的车辆数
    n_ctm_7_9[3][i] = min(n4, max(0, n_ctm_7_9[3][i - 1] + y_ii_7_9[0][i] - max(0,
                                                                                load_out_7_9[3][i - 1] - load_in_7_9[3][
                                                                                    i - 1])))
    n_ctm_7_9[4][i] = min(n5, max(0, n_ctm_7_9[4][i - 1] + y_ii_7_9[1][i] - max(0,
                                                                                load_out_7_9[4][i - 1] - load_in_7_9[4][
                                                                                    i - 1])))

print(n_ctm_7_9[2])
print(n_7_9[2])
# print(load_in_7_9[2]-load_out_7_9[2])


t = np.zeros(24)
for i in range(24):
    t[i] = i * 5
    pass
plt.subplots()
plt.plot(t, n_ctm_7_9[2], color='r', label='CTM求解结果')
plt.plot(t, n_7_9[2], color='g', label='实际数据')
plt.xlabel('7：00~9：00早高峰时间段（min）')
plt.ylabel('路段内的车辆数（veh）')
plt.title('早高峰时段结果')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.show()

# 插值法之后的x轴值，表示从0到10间距为0.5的200个数
xnew = np.arange(0, 115, 0.1)
# 实现函数
func = interpolate.interp1d(t, n_ctm_7_9[2], kind='cubic')
func1 = interpolate.interp1d(t, n_7_9[2], kind='cubic')
# 利用xnew和func函数生成ynew,xnew数量等于ynew数量
ynew = func(xnew)
ynew1 = func1(xnew)
plt.subplot()
plt.plot(xnew, ynew, color='r', label='CTM求解结果')
plt.plot(xnew, ynew1, color='g', label='实际数据')
plt.xlabel('7：00~9：00早高峰时间段（min）')
plt.ylabel('路段内的车辆数（veh）')
plt.title('早高峰时段平滑结果')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.show()

plt.subplot()
plt.plot(t, s_7_9[2] / load3 * 1000, color='r', label='load3_serve')
plt.plot(t, ((s_7_9[0] / load1) + (s_7_9[1] / load2)) * 1000, color='g', label='load1_serve+load2_serve')
plt.plot(t, ((s_7_9[3] / load4) + (s_7_9[4] / load5)) * 1000, color='b', label='load4_serve+load5_serve')
plt.xlabel('Time(min)')
plt.ylabel('Q(veh/5min)')
plt.title('7:00~9:00 SERVE')
plt.ylim([0, 600])
plt.legend()
plt.show()

###################################################################################################
# 晚高峰结果计算
# 格林希尔治模型，求该密度下最大通行流量
Q_1 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_18_20[0] / 3 / load1 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
Q_2 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_18_20[1] / 2 / load2 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))
Q_3 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_18_20[2] / 5 / load3 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 5))
Q_4 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_18_20[3] / 3 / load4 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
Q_5 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_18_20[4] / 2 / load5 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))

y_i_18_20[0][0] = min([nn_18_20[0], min(Q_1, Q_3), (n3 - nn_18_20[2])])  # 计算路段1的流出量
y_i_18_20[1][0] = min([nn_18_20[1], min(Q_2, Q_3), (n3 - nn_18_20[2])])  # 计算路段2的流出量

if (y_i_18_20[0][0] + y_i_18_20[1][0] > n3 - nn_18_20[2]):  # 供应小于需求,考虑优先级
    y_i_18_20[0][0] = int(P_j * (n3 - nn_18_20[2]))
    y_i_18_20[1][0] = (n3 - nn_18_20[2]) - y_i_18_20[0][0]
    if (y_i_18_20[0][0] > nn_18_20[0]):  # 干道分配量过大,重新调整
        y_i_18_20[0][0] = nn_18_20[0]
        y_i_18_20[1][0] = n3 - nn_18_20[2] - nn_18_20[0]
    if (y_i_18_20[1][0] > nn_18_20[1]):  # 支路分配量过大，重新调整分配量
        y_i_18_20[1][0] = nn_18_20[1]
        y_i_18_20[0][0] = n3 - nn_18_20[2] - nn_18_20[1]

# 流出量不用考虑流量的具体流向，只要求知道能够流出的量的多少
y_ii_18_20[0][0] = min([nn_18_20[2], min(Q_3, Q_4), (n4 - nn_18_20[3])])  # 计算路段3流向路段4的流出量
y_ii_18_20[1][0] = min([nn_18_20[2], min(Q_3, Q_5), (n5 - nn_18_20[4])])  # 计算路段3流向路段5的流出量
if (y_ii_18_20[0][0] + y_ii_18_20[1][0] > nn_18_20[2]):  # 当供过于求时，路段3内全部车辆都流出
    y_ii_18_20[0][0] = int(P_j * nn_18_20[2])
    y_ii_18_20[1][0] = nn_18_20[3] - y_ii_18_20[0][0]
    if (y_ii_18_20[0][0] > (n4 - nn_18_20[3])):
        y_ii_18_20[0][0] = n4 - nn_18_20[3]
        y_ii_18_20[1][0] = nn_18_20[2] - y_ii_18_20[0][0]
        pass
    if (y_ii_18_20[1][0] > (n5 - nn_18_20[4])):
        y_ii_18_20[1][0] = n5 - nn_18_20[4]
        y_ii_18_20[0][0] = nn_18_20[2] - y_ii_18_20[1][0]
        pass

# 计算下一时刻各元胞内的车辆数
n_ctm_18_20[0][0] = min(n1,
                        max(0, nn_18_20[0] - y_i_18_20[0][0] + max(0, in_18_20[0] - out_18_20[0])))  # 原有车辆-离开车辆+到达车辆
n_ctm_18_20[1][0] = min(n2, max(0, nn_18_20[1] - y_i_18_20[1][0] + max(0, in_18_20[1] - out_18_20[1])))
n_ctm_18_20[2][0] = min(n3, nn_18_20[2] + y_i_18_20[0][0] + y_i_18_20[1][0] - y_ii_18_20[0][0] - y_ii_18_20[1][
    0])  # 计算路段3的车辆数
n_ctm_18_20[3][0] = min(n4, max(0, nn_18_20[3] + y_ii_18_20[0][0] - max(0, out_18_20[3] - in_18_20[3])))
n_ctm_18_20[4][0] = min(n5, max(0, nn_18_20[4] + y_ii_18_20[1][0] - max(0, out_18_20[4] + in_18_20[4])))

for i in range(1, 24):
    # 下一时刻的最大通行量与上一时刻的密度有关
    Q_1 = max(0, int(
        (-Q_max / (k_j / 2) ** 2 * (n_ctm_18_20[0][i - 1] / 3 / load1 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
    Q_2 = max(0, int(
        (-Q_max / (k_j / 2) ** 2 * (n_ctm_18_20[1][i - 1] / 2 / load2 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))
    Q_3 = max(0, int(
        (-Q_max / (k_j / 2) ** 2 * (n_ctm_18_20[2][i - 1] / 5 / load3 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 5))
    Q_4 = max(0, int(
        (-Q_max / (k_j / 2) ** 2 * (n_ctm_18_20[3][i - 1] / 3 / load4 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
    Q_5 = max(0, int(
        (-Q_max / (k_j / 2) ** 2 * (n_ctm_18_20[4][i - 1] / 2 / load5 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))

    y_i_18_20[0][i] = min([n_ctm_18_20[0][i - 1], min(Q_1, Q_3), (n3 - n_ctm_18_20[2][i - 1])])  # 计算路段1的流出量
    y_i_18_20[1][i] = min([n_ctm_18_20[1][i - 1], min(Q_2, Q_3), (n3 - n_ctm_18_20[2][i - 1])])  # 计算路段2的流出量
    if (y_i_18_20[0][i] + y_i_18_20[1][i] > n3 - n_ctm_18_20[2][i - 1]):  # 供应小于需求,考虑优先级
        y_i_18_20[0][i] = int(P_j * (n3 - n_ctm_18_20[2][i - 1]))
        y_i_18_20[1][i] = (n3 - n_ctm_18_20[2][i - 1]) - y_i_18_20[0][i]
        if (y_i_18_20[0][i] > n_ctm_18_20[0][i - 1]):  # 干道分配量过大,重新调整
            y_i_18_20[0][i] = n_ctm_18_20[0][i - 1]
            y_i_18_20[1][i] = n3 - n_ctm_18_20[2][i - 1] - n_ctm_18_20[0][i - 1]
        if (y_i_18_20[1][i] > n_ctm_18_20[1][i - 1]):  # 支路分配量过大，重新调整分配量
            y_i_18_20[1][i] = n_ctm_18_20[1][i - 1]
            y_i_18_20[0][i] = n3 - n_ctm_18_20[2][i - 1] - n_ctm_18_20[1][i - 1]

    y_ii_18_20[0][i] = min([n_ctm_18_20[2][i - 1], min(Q_3, Q_4), (n4 - n_ctm_18_20[3][i - 1])])  # 计算路段3流向路段4的流出量
    y_ii_18_20[1][i] = min([n_ctm_18_20[2][i - 1], min(Q_3, Q_5), (n5 - n_ctm_18_20[4][i - 1])])  # 计算路段3流向路段5的流出量
    if (y_ii_18_20[0][i] + y_ii_18_20[1][i] > n_ctm_18_20[2][i - 1]):  # 当供过于求时，路段3全部车辆都流出
        y_ii_18_20[0][i] = int(P_j * n_ctm_18_20[2][i - 1])
        y_ii_18_20[1][i] = n_ctm_18_20[2][i - 1] - y_ii_18_20[0][i]
        if (y_ii_18_20[0][i] > (n4 - n_ctm_18_20[3][i - 1])):
            y_ii_18_20[0][i] = n4 - n_ctm_18_20[3][i - 1]
            y_ii_18_20[1][i] = n_ctm_18_20[2][i - 1] - y_ii_18_20[0][i]
            pass
        if (y_ii_18_20[1][i] > (n5 - n_ctm_18_20[4][i - 1])):
            y_ii_18_20[1][i] = n5 - n_ctm_18_20[4][i - 1]
            y_ii_18_20[0][i] = n_ctm_18_20[2][i - 1] - y_ii_18_20[1][i]
            pass

    n_ctm_18_20[0][i] = min(n1, max(0, n_ctm_18_20[0][i - 1] - y_i_18_20[0][i] + max(0, load_in_18_20[0][i - 1] -
                                                                                     load_out_18_20[0][i - 1])))
    n_ctm_18_20[1][i] = min(n2, max(0, n_ctm_18_20[1][i - 1] - y_i_18_20[1][i] + max(0, load_in_18_20[1][i - 1] -
                                                                                     load_out_18_20[1][i - 1])))
    n_ctm_18_20[2][i] = min(n3, n_ctm_18_20[2][i - 1] + y_i_18_20[0][i] + y_i_18_20[1][i] - y_ii_18_20[0][i] -
                            y_ii_18_20[1][i])  # 计算路段3的车辆数
    n_ctm_18_20[3][i] = min(n4, max(0, n_ctm_18_20[3][i - 1] + y_ii_18_20[0][i] - max(0, load_out_18_20[3][i - 1] -
                                                                                      load_in_18_20[3][i - 1])))
    n_ctm_18_20[4][i] = min(n5, max(0, n_ctm_18_20[4][i - 1] + y_ii_18_20[1][i] - max(0, load_out_18_20[4][i - 1] -
                                                                                      load_in_18_20[4][i - 1])))

print(n_ctm_18_20[2])
print(n_18_20[2])
# print(load_in_7_9[2]-load_out_7_9[2])


t = np.zeros(24)
for i in range(24):
    t[i] = i * 5
    pass
plt.subplots()
plt.plot(t, n_ctm_18_20[2], color='r', label='CTM求解结果')
plt.plot(t, n_18_20[2], color='g', label='实际数据')
plt.xlabel('18：00~20：00晚高峰时间段（min）')
plt.ylabel('路段内的车辆数（veh）')
plt.title('晚高峰时段结果')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.show()

# 插值法之后的x轴值，表示从0到10间距为0.5的200个数
xnew = np.arange(0, 115, 0.1)
# 实现函数
func = interpolate.interp1d(t, n_ctm_18_20[2], kind='cubic')
func1 = interpolate.interp1d(t, n_18_20[2], kind='cubic')
# 利用xnew和func函数生成ynew,xnew数量等于ynew数量
ynew = func(xnew)
ynew1 = func1(xnew)
plt.subplot()
plt.plot(xnew, ynew, color='r', label='CTM求解结果')
plt.plot(xnew, ynew1, color='g', label='实际数据')
plt.xlabel('18：00~20：00晚高峰时间段（min）')
plt.ylabel('路段内的车辆数（veh）')
plt.title('晚高峰时段平滑结果')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.show()

plt.subplot()
plt.plot(t, s_18_20[2] / load3 * 1000, color='r', label='load3_serve')
plt.plot(t, ((s_18_20[0] / load1) + (s_18_20[1] / load2)) * 1000, color='g', label='load1_serve+load2_serve')
plt.plot(t, ((s_18_20[3] / load4) + (s_18_20[4] / load5)) * 1000, color='b', label='load4_serve+load5_serve')
plt.xlabel('Time(min)')
plt.ylabel('Q(veh/5min)')
plt.title('18:00~20:00 SERVE')
plt.ylim([0, 600])
plt.legend()
plt.show()

###################################################################################################
# 平峰结果计算
# 格林希尔治模型，求该密度下最大通行流量
Q_1 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_12_14[0] / 3 / load1 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
Q_2 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_12_14[1] / 2 / load2 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))
Q_3 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_12_14[2] / 5 / load3 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 5))
Q_4 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_12_14[3] / 3 / load4 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
Q_5 = max(0, int((-Q_max / (k_j / 2) ** 2 * (nn_12_14[4] / 2 / load5 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))

y_i_12_14[0][0] = min([nn_12_14[0], min(Q_1, Q_3), (n3 - nn_12_14[2])])  # 计算路段1的流出量
y_i_12_14[1][0] = min([nn_12_14[1], min(Q_2, Q_3), (n3 - nn_12_14[2])])  # 计算路段2的流出量

if (y_i_12_14[0][0] + y_i_12_14[1][0] > n3 - nn_12_14[2]):  # 供应小于需求,考虑优先级
    y_i_12_14[0][0] = int(P_j * (n3 - nn_12_14[2]))
    y_i_12_14[1][0] = (n3 - nn_12_14[2]) - y_i_12_14[0][0]
    if (y_i_12_14[0][0] > nn_12_14[0]):  # 干道分配量过大,重新调整
        y_i_12_14[0][0] = nn_12_14[0]
        y_i_12_14[1][0] = n3 - nn_12_14[2] - nn_12_14[0]
    if (y_i_12_14[1][0] > nn_12_14[1]):  # 支路分配量过大，重新调整分配量
        y_i_12_14[1][0] = nn_12_14[1]
        y_i_12_14[0][0] = n3 - nn_12_14[2] - nn_12_14[1]

# 流出量不用考虑流量的具体流向，只要求知道能够流出的量的多少
y_ii_12_14[0][0] = min([nn_12_14[2], min(Q_3, Q_4), (n4 - nn_12_14[3])])  # 计算路段3流向路段4的流出量
y_ii_12_14[1][0] = min([nn_12_14[2], min(Q_3, Q_5), (n5 - nn_12_14[4])])  # 计算路段3流向路段5的流出量
if (y_ii_12_14[0][0] + y_ii_12_14[1][0] > nn_12_14[2]):  # 当供过于求时，路段3内全部车辆都流出
    y_ii_12_14[0][0] = int(P_j * nn_12_14[2])
    y_ii_12_14[1][0] = nn_12_14[3] - y_ii_12_14[0][0]
    if (y_ii_12_14[0][0] > (n4 - nn_12_14[3])):
        y_ii_12_14[0][0] = n4 - nn_12_14[3]
        y_ii_12_14[1][0] = nn_12_14[2] - y_ii_12_14[0][0]
        pass
    if (y_ii_12_14[1][0] > (n5 - nn_12_14[4])):
        y_ii_12_14[1][0] = n5 - nn_12_14[4]
        y_ii_12_14[0][0] = nn_12_14[2] - y_ii_12_14[1][0]
        pass

# 计算下一时刻各元胞内的车辆数
n_ctm_12_14[0][0] = min(n1,
                        max(0, nn_12_14[0] - y_i_12_14[0][0] + max(0, in_12_14[0] - out_12_14[0])))  # 原有车辆-离开车辆+到达车辆
n_ctm_12_14[1][0] = min(n2, max(0, nn_12_14[1] - y_i_12_14[1][0] + max(0, in_12_14[1] - out_12_14[1])))
n_ctm_12_14[2][0] = min(n3, nn_12_14[2] + y_i_12_14[0][0] + y_i_12_14[1][0] - y_ii_12_14[0][0] - y_ii_12_14[1][
    0])  # 计算路段3的车辆数
n_ctm_12_14[3][0] = min(n4, max(0, nn_12_14[3] + y_ii_12_14[0][0] - max(0, out_12_14[3] - in_12_14[3])))
n_ctm_12_14[4][0] = min(n5, max(0, nn_12_14[4] + y_ii_12_14[1][0] - max(0, out_12_14[4] + in_12_14[4])))

for i in range(1, 24):
    # 下一时刻的最大通行量与上一时刻的密度有关
    Q_1 = max(0, int(
        (-Q_max / (k_j / 2) ** 2 * (n_ctm_12_14[0][i - 1] / 3 / load1 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
    Q_2 = max(0, int(
        (-Q_max / (k_j / 2) ** 2 * (n_ctm_12_14[1][i - 1] / 2 / load2 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))
    Q_3 = max(0, int(
        (-Q_max / (k_j / 2) ** 2 * (n_ctm_12_14[2][i - 1] / 5 / load3 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 5))
    Q_4 = max(0, int(
        (-Q_max / (k_j / 2) ** 2 * (n_ctm_12_14[3][i - 1] / 3 / load4 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 3))
    Q_5 = max(0, int(
        (-Q_max / (k_j / 2) ** 2 * (n_ctm_12_14[4][i - 1] / 2 / load5 * 1000 - k_j / 2) ** 2 + Q_max) / 12 * 2))

    y_i_12_14[0][i] = min([n_ctm_12_14[0][i - 1], min(Q_1, Q_3), (n3 - n_ctm_12_14[2][i - 1])])  # 计算路段1的流出量
    y_i_12_14[1][i] = min([n_ctm_12_14[1][i - 1], min(Q_2, Q_3), (n3 - n_ctm_12_14[2][i - 1])])  # 计算路段2的流出量
    if (y_i_12_14[0][i] + y_i_12_14[1][i] > n3 - n_ctm_12_14[2][i - 1]):  # 供应小于需求,考虑优先级
        y_i_12_14[0][i] = int(P_j * (n3 - n_ctm_12_14[2][i - 1]))
        y_i_12_14[1][i] = (n3 - n_ctm_12_14[2][i - 1]) - y_i_12_14[0][i]
        if (y_i_12_14[0][i] > n_ctm_12_14[0][i - 1]):  # 干道分配量过大,重新调整
            y_i_12_14[0][i] = n_ctm_12_14[0][i - 1]
            y_i_12_14[1][i] = n3 - n_ctm_12_14[2][i - 1] - n_ctm_12_14[0][i - 1]
        if (y_i_12_14[1][i] > n_ctm_12_14[1][i - 1]):  # 支路分配量过大，重新调整分配量
            y_i_12_14[1][i] = n_ctm_12_14[1][i - 1]
            y_i_12_14[0][i] = n3 - n_ctm_12_14[2][i - 1] - n_ctm_12_14[1][i - 1]

    y_ii_12_14[0][i] = min([n_ctm_12_14[2][i - 1], min(Q_3, Q_4), (n4 - n_ctm_12_14[3][i - 1])])  # 计算路段3流向路段4的流出量
    y_ii_12_14[1][i] = min([n_ctm_12_14[2][i - 1], min(Q_3, Q_5), (n5 - n_ctm_12_14[4][i - 1])])  # 计算路段3流向路段5的流出量
    if (y_ii_12_14[0][i] + y_ii_12_14[1][i] > n_ctm_12_14[2][i - 1]):  # 当供过于求时，路段3全部车辆都流出
        y_ii_12_14[0][i] = int(P_j * n_ctm_12_14[2][i - 1])
        y_ii_12_14[1][i] = n_ctm_12_14[2][i - 1] - y_ii_12_14[0][i]
        if (y_ii_12_14[0][i] > (n4 - n_ctm_12_14[3][i - 1])):
            y_ii_12_14[0][i] = n4 - n_ctm_12_14[3][i - 1]
            y_ii_12_14[1][i] = n_ctm_12_14[2][i - 1] - y_ii_12_14[0][i]
            pass
        if (y_ii_12_14[1][i] > (n5 - n_ctm_12_14[4][i - 1])):
            y_ii_12_14[1][i] = n5 - n_ctm_12_14[4][i - 1]
            y_ii_12_14[0][i] = n_ctm_12_14[2][i - 1] - y_ii_12_14[1][i]
            pass

    n_ctm_12_14[0][i] = min(n1, max(0, n_ctm_12_14[0][i - 1] - y_i_12_14[0][i] + max(0, load_in_12_14[0][i - 1] -
                                                                                     load_out_12_14[0][i - 1])))
    n_ctm_12_14[1][i] = min(n2, max(0, n_ctm_12_14[1][i - 1] - y_i_12_14[1][i] + max(0, load_in_12_14[1][i - 1] -
                                                                                     load_out_12_14[1][i - 1])))
    n_ctm_12_14[2][i] = min(n3, n_ctm_12_14[2][i - 1] + y_i_12_14[0][i] + y_i_12_14[1][i] - y_ii_12_14[0][i] -
                            y_ii_12_14[1][i])  # 计算路段3的车辆数
    n_ctm_12_14[3][i] = min(n4, max(0, n_ctm_12_14[3][i - 1] + y_ii_12_14[0][i] - max(0, load_out_12_14[3][i - 1] -
                                                                                      load_in_12_14[3][i - 1])))
    n_ctm_12_14[4][i] = min(n5, max(0, n_ctm_12_14[4][i - 1] + y_ii_12_14[1][i] - max(0, load_out_12_14[4][i - 1] -
                                                                                      load_in_12_14[4][i - 1])))

print(n_ctm_12_14[2])
print(n_12_14[2])
# print(load_in_7_9[2]-load_out_7_9[2])


t = np.zeros(24)
for i in range(24):
    t[i] = i * 5
    pass
plt.subplots()
plt.plot(t, n_ctm_12_14[2], color='r', label='CTM求解结果')
plt.plot(t, n_12_14[2], color='g', label='实际数据')
plt.xlabel('12：00~14：00平峰时间段（min）')
plt.ylabel('路段内的车辆数（veh）')
plt.title('平峰时段结果')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.show()

# 插值法之后的x轴值，表示从0到10间距为0.5的200个数
xnew = np.arange(0, 115, 0.1)
# 实现函数
func = interpolate.interp1d(t, n_ctm_12_14[2], kind='cubic')
func1 = interpolate.interp1d(t, n_12_14[2], kind='cubic')
# 利用xnew和func函数生成ynew,xnew数量等于ynew数量
ynew = func(xnew)
ynew1 = func1(xnew)
plt.subplot()
plt.plot(xnew, ynew, color='r', label='CTM求解结果')
plt.plot(xnew, ynew1, color='g', label='实际数据')
plt.xlabel('12：00~14：00平峰时间段（min）')
plt.ylabel('路段内的车辆数（veh）')
plt.title('平峰时段平滑结果')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.legend()
plt.show()

plt.subplot()
plt.plot(t, s_12_14[2] / load3 * 1000, color='r', label='load3_serve')
plt.plot(t, ((s_12_14[0] / load1) + (s_12_14[1] / load2)) * 1000, color='g', label='load1_serve+load2_serve')
plt.plot(t, ((s_12_14[3] / load4) + (s_12_14[4] / load5)) * 1000, color='b', label='load4_serve+load5_serve')
plt.xlabel('Time(min)')
plt.ylabel('Q(veh/5min)')
plt.title('12:00~14:00 SERVE')
plt.ylim([0, 600])
plt.legend()
plt.show()
