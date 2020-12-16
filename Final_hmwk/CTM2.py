# _*_ coding：utf-8_*_
# 开发团队：张萌
# 开发人员：lenovo
# 开发时间：7:46
# 文件名：CTM2.py
# 开发工具：PyCharm
import numpy as np
import pandas as pd
from datetime import date
from matplotlib import pyplot as plt


def mid(x):
    if x[0] != np.min(x) and x[0] != np.max(x):
        return x[0]
    if x[1] != np.min(x) and x[1] != np.max(x):
        return x[1]
    if x[2] != np.min(x) and x[2] != np.max(x):
        return x[2]


data = pd.read_csv(r'C:\Users\lenovo\Desktop\CTM_SH_191204.csv')
print(type(data))
data['FT_5MIN'] = pd.to_datetime(data['FT_5MIN'])
data['TT_5MIN'] = pd.to_datetime(data['TT_5MIN'])
# 做时间筛选和路段筛选
# 平峰晚高峰早高峰只需要改time
time1 = '2019-12-04 21:55:00'
time2 = "2019-12-04 23:05:00"
data_1_3 = data[(data["FNODE"] == 31010100000018) & (data["TNODE"] == 31010100000119) &
                (time1 <= data["FT_5MIN"]) & (data["FT_5MIN"] <= time2)]
data_2_3 = data[(data["FNODE"] == 31010100000118) & (data["TNODE"] == 31010100000119) &
                (time1 <= data["FT_5MIN"]) & (data["FT_5MIN"] <= time2)]
data_3_4 = data[(data["FNODE"] == 31010100000119) & (data["TNODE"] == 31010100000086) &
                (time1 <= data["FT_5MIN"]) & (data["FT_5MIN"] <= time2)]
data_4_5 = data[(data["FNODE"] == 31010100000086) & (data["TNODE"] == 31010600000065) &
                (time1 <= data["FT_5MIN"]) & (data["FT_5MIN"] <= time2)]
data_4_6 = data[(data["FNODE"] == 31010100000086) & (data["TNODE"] == 31010100000065) &
                (time1 <= data["FT_5MIN"]) & (data["FT_5MIN"] <= time2)]
# print(type(data_1_3))
# 初始化仿真参数和五个元胞的车辆状态
# 元胞为1、2、3、4、5，路段的链接为1-3,2-3,3-4,4-5,4-6，元胞3有3和4两个节点
p1 = 2/3
p2 = 1/3
Kjam = 110
Q = 2000
lane = np.array([3, 2, 5, 3, 2])
length = np.array([527.3861, 274.6353, 230.3829, 456.2745, 456.2734])
t = 5
Nj = lane * Kjam * length / 1000
Qmax = Q * lane * t / 60
print("Nj:{}\nQmax:{}".format(Nj, Qmax))
density_1_3 = list(data_1_3["DENSITY"])
in_flow_1_3 = list(data_1_3["IN_FLOW"])
out_flow_1_3 = list(data_1_3["OUT_FLOW"])
v_1_3 = list(data_1_3["AVG_SPEED"])
density_2_3 = list(data_2_3["DENSITY"])
in_flow_2_3 = list(data_2_3["IN_FLOW"])
out_flow_2_3 = list(data_2_3["OUT_FLOW"])
v_2_3 = list(data_2_3["AVG_SPEED"])
density_3_4 = list(data_3_4["DENSITY"])
v_3_4 = list(data_3_4["AVG_SPEED"])
density_4_5 = list(data_4_5["DENSITY"])
in_flow_4_5 = list(data_4_5["IN_FLOW"])
out_flow_4_5 = list(data_4_5["OUT_FLOW"])
v_4_5 = list(data_4_5["AVG_SPEED"])
density_4_6 = list(data_4_6["DENSITY"])
in_flow_4_6 = list(data_4_6["IN_FLOW"])
out_flow_4_6 = list(data_4_6["OUT_FLOW"])
v_4_6 = list(data_4_6["AVG_SPEED"])
cell = [density_1_3[0], density_2_3[0], density_3_4[0], density_4_5[0], density_4_6[0]]  # 将6：55的车辆状态赋给元胞
print(cell)
y_1_3 = []  # 用于储存1-3输出的流量
y_2_3 = []  # 用于储存2-3输出的流量
y3 = []  # 用于储存输入到元胞3的流量
y4 = []  # 用于储存元胞3输出的流量
y_4_5 = []  # 用于储存4-5输出的流量
y_4_6 = []  # 用于储存4-6输出的流量
print('总个数:{}'.format(len(data_1_3["FT_5MIN"])))
for i in range(1, len(data_1_3["FT_5MIN"]) - 1):
    # 合流
    n1 = (cell[0] + in_flow_1_3[i]) * (5 - length[0] * 3.6 / v_1_3[i] / 60) / 5
    n2 = (cell[1] + in_flow_2_3[i]) * (5 - length[1] * 3.6 / v_2_3[i] / 60) / 5
    S1 = np.min([n1, Qmax[0]])
    print('S1:{}'.format(S1))
    S2 = np.min([n2, Qmax[1]])
    print('S2:{}'.format(S2))
    y_1_3.append(S1)
    y_2_3.append(S2)
    y3.append(S1 + S2)
    n4 = (cell[2] + y3[-1]) * (5 - length[2] * 3.6 / v_3_4[i] / 60) / 5
    S4 = np.min([n4, Qmax[2]])
    y4.append(S4)
    y_4_5.append(S4 * p1)
    y_4_6.append(S4 * p2)
    # 更新所有元胞状态
    n5 = (cell[3] + y_4_5[-1]) * (5 - length[3] * 3.6 / v_4_5[i] / 60) / 5
    n6 = (cell[4] + y_4_6[-1]) * (5 - length[4] * 3.6 / v_4_6[i] / 60) / 5
    cell[0] = max(0, cell[0] + in_flow_1_3[i] - y_1_3[-1])
    cell[1] = max(0, cell[1] + in_flow_2_3[i] - y_2_3[-1])
    cell[2] = max(0, cell[2] + y3[-1] - y4[-1])
    cell[3] = max(0, cell[3] + y_4_5[-1] - n5)
    cell[4] = max(0, cell[4] + y_4_6[-1] - n6)
real_1_3 = out_flow_1_3[1:-1]
real_2_3 = out_flow_2_3[1:-1]
real_4_5 = in_flow_4_5[1:-1]
real_4_6 = in_flow_4_6[1:-1]
real_4 = np.array(real_4_5) + np.array(real_4_6)
print(len(real_4_6))
print(len(y_1_3))
plt.plot(real_1_3, marker="o", label='real')
plt.plot(y_1_3, marker="*", label='CTM')
plt.legend()
plt.show()
plt.plot(real_2_3, marker="o", label='real')
plt.plot(y_2_3, marker="*", label='CTM')
plt.legend()
plt.show()
plt.plot(real_4_5, marker="o", label='real')
plt.plot(y_4_5, marker="*", label='CTM')
plt.legend()
plt.show()
plt.plot(real_4_6, marker="o", label='real')
plt.plot(y_4_6, marker="*", label='CTM')
plt.legend()
plt.show()
plt.plot(real_4, marker="o", label='real')
plt.plot(y4, marker="o", label='CTM')
plt.legend()
plt.show()
