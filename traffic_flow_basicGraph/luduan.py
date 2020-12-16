# _*_ coding：utf-8_*_
# 开发团队：张萌
# 开发人员：lenovo
# 开发时间：11:30
# 文件名：luduan.py
# 开发工具：PyCharm
import pandas as pd
import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pylab as mpl     #import matplotlib as mpl

# 画出未加入随机数的流量密度图
f = open("C:\\Users\\lenovo\\Desktop\\luduan.txt","r",encoding="utf-8")
i = 0
q = []
k = []
f.readline()
for str in f:
    strlt = str.split()
    q.append(eval(strlt[1]))
    k.append(eval(strlt[0]))
q1 = np.array(q)
k1 = np.array(k)
#设置汉字格式
# sans-serif就是无衬线字体，是一种通用字体族。
# 常见的无衬线字体有 Trebuchet MS, Tahoma, Verdana, Arial, Helvetica,SimHei 中文的幼圆、隶书等等
mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
plt.scatter(x=k1,y=q1)
plt.xlabel("密度k",)
plt.ylabel("流量q")
plt.show()