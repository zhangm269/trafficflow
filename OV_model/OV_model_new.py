# _*_ coding：utf-8_*_
# 开发团队：张萌
# 开发人员：lenovo
# 开发时间：16:22
# 文件名：OV_model_new.py
# 开发工具：PyCharm
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D
import math
from .hyperparam import *
e = math.e

# tanh函数，优化速度模型
def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))


def v_opt(x):
    if (x < 1):
        return 0
    elif (x <= 5):
        return 0.5 * (x - 1)
    else:
        return 2


def speed(h_list):
    """
    :param h_list: 传入车间距向量
    :return:
    """
    v = v_max / 2 * (tanh(h_list - h_c) + tanh(h_c))
    return v


def renew_x(h_list, num, r=0.0):
    """
    :param h_list: 传入车间距向量
    :param num: 传入第i次更新的索引i
    :param r: 传入扰动
    :return:
    """
    v = speed(h_list)
    for ii in range(N):
        if r == 0.0:
            x[ii, num] = x[ii, num - 1] + tao * v[ii]
        # 循环路段
            if x[ii, num] > L:
                x[ii, num] = x[ii, num] - L
        if r != 0.0:
            if ii == 0:
                x[ii, num] = x[ii, num - 1] + tao * v[ii] + r
                # 循环路段
                if x[ii, num] > L:
                    x[ii, num] = x[ii, num] - L
            else:
                x[ii, num] = x[ii, num - 1] + tao * v[ii]
                # 循环路段
                if x[ii, num] > L:
                    x[ii, num] = x[ii, num] - L


def renew_hgap(num):
    """
    :param num: 传入第i次更新的索引i
    :return:
    """
    # 更新第一辆车的h_gap和其他辆车的h_gap
    if x[N - 1, num] - x[0, num] < 0:
        h_gap[num, 0] = L - x[0, num] + x[N - 1, num]
    else:
        h_gap[num, 0] = x[N - 1, num] - x[0, num]
    for ii in range(1, N):
        if x[ii - 1, num] - x[ii, num] < 0:
            h_gap[num, ii] = L - x[ii, num] + x[ii - 1, num]
        else:
            h_gap[num, ii] = x[ii - 1, num] - x[ii, num]


def dv_opt(dd, h_c, v_max):
    return v_max / 2 * 4 * np.exp(-2 * (dd - h_c)) / (1 + np.exp(-2 * (dd - h_c))) ** 2


x = np.zeros([N, len(t)])  # 记录各车的行驶距离
xx = np.zeros([N, len(t)])
h_gap = np.zeros([len(t), N])  # 记录车头间距
hh_gap = np.zeros([len(t), N])
# 初始化时刻一的位置和车头间距
x[0, 0] = b * (N - 1)
h_gap[0, 0] = L - x[0, 0]
for i in range(1, N):
    x[i, 0] = b * (N - i - 1)
    h_gap[0, i] = x[i - 1, 0] - x[i, 0]
# 运行tao之后的位置，此时加入扰动
renew_x(h_gap[0, :], num=1, r=y)
renew_hgap(num=1)
# 循环起来，并且需要判断是否达到反应时间
k = 0
h_gap_flag = h_gap[0, :]    # 没到反应时间用到的车间距，用于更新x
for i in range(2, len(t) - 2):
    k += 1
    if k * tao < T:
        renew_x(h_gap_flag, num=i, r=0)
        renew_hgap(num=i)
    else:
        renew_x(h_list=h_gap[i - 2, :],num=i, r=0)
        renew_hgap(num=i)
        h_gap_flag = h_gap[i, :]
        k = 0
# 作图
for i in range(int(N / 50)):
    plt.plot(t, x[i * 50])
plt.show()
fig = plt.figure()
ax = Axes3D(fig)
for i in range(1,int(len(t)/100)):
    X = range(100)
    Y = np.zeros([N])
    for j in range(N):
        Y[j]=t[i*10]
        pass
    Z = h_gap[i*10]
#    print(Z[:100])
    ax.plot(X[:100], Y[:100], Z[:100])
    pass
# ax.set_title("Gap")
ax.set_xlabel("Car Number")
ax.set_ylabel("Time")
ax.set_zlabel("Headway")
ax.set_zlim(2,4)
#ax.set_ylim(0,100)
plt.show()
dd = np.linspace(2, 5, 100)
plt.plot(dd, dv_opt(dd, h_c, v_max), 'y', label='V’(x)')
plt.plot([min(dd), max(dd)], [a / 2, a / 2], 'r', label='a/2')
plt.plot([b, b], [0, 1], 'g', label='b')
plt.scatter(b, dv_opt(b, h_c, v_max), c='r', marker='x', label='V’(b)')
if dv_opt(b, h_c, v_max) < a / 2:
    plt.title('稳定')
    pass
elif dv_opt(b, h_c, v_max) == a / 2:
    plt.title('临界稳定')
    pass
else:
    plt.title('不稳定')
    pass
plt.xlabel("x")
plt.ylabel("V’(x)")
plt.grid()
plt.legend()
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标题
plt.rcParams['axes.unicode_minus'] = False
plt.show()
