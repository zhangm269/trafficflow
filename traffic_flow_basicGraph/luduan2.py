# _*_ coding：utf-8_*_
# 开发团队：张萌
# 开发人员：lenovo
# 开发时间：10:35
# 文件名：luduan2.py
# 开发工具：PyCharm
import matplotlib.pyplot as plt
import random
import numpy as np
import pylab as mpl
time = []
num =[]
speed =[]
f = open("C:\\Users\\lenovo\\Desktop\\路段2.txt",mode="r",encoding="utf-8")
for data in f:
    data =data.split()
    print(data)
    time.append(data[0])
    num.append(eval(data[1]))
    speed.append(eval(data[2]))
# print(num,speed)
k = []
for i in range(len(num)):
    temp = num[i]/random.uniform(0.03,0.05)/0.482/4
    k.append(temp)
# for i in range(len(num)):
#     if  "6:00"<=time[i]<="7:00":
#         temp = num[i]/random.uniform(0.1,0.3)/0.482
#         k.append(temp)
#     elif "7:00"<time[i]<="8:00":
#         if num[i]<3:
#             temp = num[i]/random.uniform(0.03,0.06)/0.482
#         else:
#             temp = num[i] / random.uniform(0.13,0.2)/ 0.482
#         k.append(temp)
#     else:
#         if num[i]<3:
#             temp = num[i]/random.uniform(0.03,0.1)/0.482
#         else:
#             temp = num[i] / random.uniform(0.1, 0.2) / 0.482
#         k.append(temp)
k1 = np.array(k)
# for i in range(len(k1)):
#     if k1[i] >80:
#         k1[i]=24.348+np.random.randint(-5,10)
# print(k1)
speed1 = np.array(speed)
q = k1*speed1/3
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
plt.xlabel("density veh/km",)
plt.ylabel("volume veh/h")
plt.title("路段基本图")
plt.scatter(k1,q)
plt.show()
plt.plot()
plt.show()
