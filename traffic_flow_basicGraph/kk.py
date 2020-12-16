# _*_ coding：utf-8_*_
# 开发团队：张萌
# 开发人员：lenovo
# 开发时间：15:22
# 文件名：kk.py
# 开发工具：PyCharm
import pandas as pd                     # 读取csv文件小能手
import matplotlib.pyplot as plt         # 画图小能手
import numpy as np                      # 计算小能手
import datetime
# 读取文件
data = pd.read_csv("tab_kk.csv")
data.SJ = pd.to_datetime(data.SJ)
# 筛选异常数据
data_new = data[(data.FTNODE == "5021_5012") & (data.LANEID >= 0) & (0 < data.SPEED) & (data.SPEED <= 60)]
print(data_new.shape)
length = len(data_new)
# 将列数据转换为列表
travel_id = list(data_new.TRAVELID)
device_id = list(data_new.DEVICEID)
speed = list(data_new.SPEED)
time = list(data_new.SJ)
# 遍历车辆，找到既有进入又有出去记录的车辆标记为2，只进入的标记为0，只出去的标记为1
# 标记为2的车将会作为试验车
label = np.zeros(length, np.dtype(np.int))
for i in range(length):
    # 如果在前面可以找到这个id 直接标记为2
    if travel_id[i] in travel_id[max(0, i-200):i]:
        label[i] = 2
    # 如果前面没有这个id，则往下寻找
    else:
        for j in range(i+1, min(i+200, len(data_new))):
            # 如果向下的200辆车可以找到，标记为2，并退出循环
            if travel_id[i] == travel_id[j]:
                label[i] = 2
                break
            else:
                continue
        # 如果没有找到即标记为0，判断是进入还是出去，进入标记为0，出去标记为1
        if label[i] == 0:
            if device_id[i] == 915:
                pass
            else:
                label[i] = 1
"""
# 统计一下只进入 只出去 还有既进入又出去的车的数量（只进入和只出去都分了两种情况
# ）即在试验车前只进入的和在试验车后只进入的，在试验车后只进入的不影响对密度的计算，
# 在试验车前面进入的可能导致了对密度的低估(因为他可能真的在路上，在很大概率上是从岔口
# 直接开出路段)，在试验车后面只出去的我们会将其统计在密度计算中，在试验车前面只出去
# 的不影响计算。
"""
cout_only_in = cout_only_out = cout_in_out = 0
for i in label:
    if i == 0:
        cout_only_in += 1
    elif i == 1:
        cout_only_out += 1
    else:
        cout_in_out += 1
print("只进入的有{0}，只出去的有{1}，即进入又出去的有{2}".format(cout_only_in, cout_only_out, cout_in_out))
# 画图初始化
fig = plt.figure()  # 画图初始化，并规定行列标题名称
ax1 = fig.add_subplot(1, 1, 1)
plt.xlabel("density,veh/km")
plt.ylabel("volume,veh/h")
plt.title("Basic Diagram of Traffic Flow")
time1 = datetime.datetime.strptime("2019/7/3  8:00:00", "%Y/%m/%d  %H:%M:%S")   # 设置两个时间节点，用于分割图像
time2 = datetime.datetime.strptime("2019/7/3  10:00:00", "%Y/%m/%d  %H:%M:%S")
"""
对标记的车进行试验,每五分钟调查一次，12*6=72个检测点，
每个检测点随机抽取一辆标记为2的车，
从进入时间开始，对后面的车辆进行统计，设备id为915的加入lt_in 列表，
设备id为916的且不再lt_in列表的加入lt_out列表（即删除了超过试验车的车辆）直到travel_id==试验车id，
记录试验车出去的时刻，向下搜索被试验车超过的原来在路段上的车辆，直到两分钟结束。因为两分钟足以跑完两个卡口。
！！！！！此次没有将只进入的车计算在内，但只出去的车计算在内了
"""
# 算法实现
time_diff = pd.to_timedelta("0 0 1 minute 0 second")    # 设置向下搜索的两分钟和检测间隔和初始时刻
time_interval = pd.to_timedelta("0 0 5 minute 0 second")
car_in = []
car_out = []
car_out_speed = []
k_r = np.zeros(72)  # 初始化密度、速度等交通流参数，用于之后画图
q_r = np.zeros(72)
time_start = time[0]
index = np.zeros(2,np.dtype(np.int))  # index分别储存开始时刻第一个车辆和最后一个车辆的索引
for k in range(72):
    # 对起始时刻第一辆车和最后一辆车进行搜索,并赋值给index列表
    index[0] = time.index(time_start)
    for i in range(index[0], length):
        if device_id[i] == 916 and time[i] == time_start:
            index[1] = i-1
            break
        else:
            pass
    # 选取试验车，必须标记为2,如果某个时间没有怎么办这是个问题看看吧一会
    print(index)
    # print(time[index[0]])
    if index[0]<index[1]:
        test_car_index = np.random.randint(index[0], index[1])
    else:
        index[1] += 1
        test_car_index = np.random.randint(index[0], index[1])
    while label[test_car_index] != 2:
        test_car_index = np.random.randint(index[0], index[1])
    test_car_info = [device_id[test_car_index], travel_id[test_car_index],
                     time[test_car_index], speed[test_car_index]]  # 记录试验车的信息
    # 选完试验车，以试验车位置开始寻找之前在路段的车辆，直到找到试验车id
    for ii in range(test_car_index+1, length):
        if device_id[ii] == 915 and travel_id[ii] != test_car_info[1]:
            car_in.append(travel_id[ii])
        elif device_id[ii] == 916 and travel_id[ii] != test_car_info[1] and device_id[ii] not in car_in:
            car_out.append(travel_id[ii])
            car_out_speed.append(speed[ii])
        elif travel_id[ii] == test_car_info[1]:
            time_temp = time[ii]    # 记录试验车出去的时间
            location = ii       # 记录试验车出去的位置
            break
    # 以试验车出去时刻开始，往后搜索两分钟，超过两分钟就跳出循环
    for kk in range(location, length):
        if time[kk] < time_temp + time_diff:
            if device_id[kk] == 915 and travel_id[kk] != test_car_info[1]:
                car_in.append(travel_id[kk])
            elif device_id[kk] == 916 and travel_id[kk] != test_car_info[1] and device_id[kk] not in car_in\
                    and label[kk] != 1:
                car_out.append(travel_id[kk])
                car_out_speed.append(speed[kk])
        else:
            break
    # 计算数据并保存在列表里
    k_r[k] = len(car_out)/0.38
    ut = len(car_out_speed)/sum(1/x for x in car_out_speed)
    # ut = sum(car_out_speed)/len(car_out_speed)
    print(ut)
    q_r[k] = k_r[k]*ut
    if time_start < time1:
        ax1.scatter(k_r[k], q_r[k], color="red", marker='+', label='6:00-8:00')  # 这里的label不出来，目前没解决
    elif (time_start >= time1) and (time_start < time2):
        ax1.scatter(k_r[k], q_r[k], color="blue", marker='+', label='8:00-10:00')
    else:
        ax1.scatter(k_r[k], q_r[k], color="green", marker='+', label='10:00-12:00')
    # 重新初始化数据比如时间加五分钟、列表均置空
    time_start = time_start + time_interval
    car_in = []
    car_out = []
    car_out_speed = []
plt.show()
print(k_r.shape)
f=open("data.txt","w")
f.writelines(str(k_r)+"\n"+str(q_r))
