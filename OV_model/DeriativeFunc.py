# _*_ coding：utf-8_*_
# 开发团队：张萌
# 开发人员：lenovo
# 开发时间：22:17
# 文件名：DeriativeFunc.py
# 开发工具：PyCharm
import numpy as np
import sympy as sy
import math

def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

y = tanh(2)
print(y)
# def sympy_derivative():
#     # 定义表达式的变量名称
#     x1 = sy.symbols('x1')
#     # 定义表达式内容
#     Y = (sy.exp(x1)-sy.exp(-x1))/(sy.exp(x1)+sy.exp(-x1))
#     # 计算 x2对应的偏导数
#     return sy.diff(Y, x1)
#
#
# func = sympy_derivative()
# print(func)
# print(func.evalf(subs ={'x1':2})) # 把x1 等于6 带入计算 结果 为12