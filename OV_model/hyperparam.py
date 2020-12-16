# _*_ coding：utf-8_*_
# 开发团队：张萌
# 开发人员：lenovo
# 开发时间：21:36
# 文件名：hyperparam.py
# 开发工具：PyCharm
import numpy as np
# 下面为模型的一些参数选取，具体意义看PPT
N = 100  # 车辆数
v_max = 2  # 最大速度
h_c = 2  #
b = 2.5  # 初始车头间距
a = 1.5  # 敏感强度，为反应时间的倒数
L = b * N  # 环形路的长度
T = 1 / a  # 反应时间
y = 0.1
tao = 0.1
start_time = 0
end_time = 1000
t = np.linspace(start_time, end_time, int((end_time - start_time) / tao + 1))  # 时间
t_gap = t[1] - t[0]  # 时间间隔，步长

