import pandas as pd                     # 读取csv文件小能手
import matplotlib.pyplot as plt         # 画图小能手
import numpy as np                      # 计算小能手
import datetime                         # 处理时间小能手

data=pd.read_csv('tab_kk.csv')           #读取数据文件小能手

data['SJ']=pd.to_datetime(data['SJ'])                       #将时间从str转化成datetime格式

conv_kk1=data[(data['LANEID']>=0)                          #数据清洗，筛选某一路段，筛选掉laneid为负或速度等于0或大于60km/h的数据
               & (data['FTNODE']=="5021_5012")
               & (data['SPEED']>0) & (data['SPEED']<60)]

conv_kk_in=data[data['DEVICEID']==915]     #分离进出数据
conv_kk_out=data[data['DEVICEID']==916]

match=list(conv_kk_in.TRAVELID)             #转换pandas列为字符串数组，我们要得到有进有出、无进有出的车，这里是为了匹配有进有出的车
screen=list(conv_kk_out.TRAVELID)
select=[]
k=0
for i in range(len(screen)):
    for j in range(len(match)):
        if screen[i]==match[j]:             #匹配数据，我认为这一步可以用其他代码优化一下，这里太久了
            select.append(screen[i])
            k+=1

conv_kk_in=conv_kk_in[conv_kk_in.TRAVELID.isin(select)]     #将匹配好的数据在in数据中筛选，让in数据只有有进有出的车，这样就可以进行匹配了
m,col1=conv_kk_in.shape        #获取有进有出车的数量
conv_kk_in.index=range(m)      #替换行名，原本是data中的行名，为了方便计算，我这里换成0到2000+的单位递增数列
k_r=np.zeros(m)                #初始化密度、速度等交通流参数，用于之后画图
q_r=np.zeros(m)

fig = plt.figure()             #画图初始化，并规定行列标题名称
ax1 = fig.add_subplot(1, 1, 1)
plt.xlabel("density,veh/km")
plt.ylabel("volume,veh/h")
plt.title("Basic Diagram of Traffic Flow")

time1=datetime.datetime.strptime("2019/7/3  8:00:00", "%Y/%m/%d  %H:%M:%S")     #设置两个时间节点，用于分割图像
time2=datetime.datetime.strptime("2019/7/3  10:00:00", "%Y/%m/%d  %H:%M:%S")

for i in conv_kk_in.index:              # 里把所有有进有出的车全部当成了试验车
    start_time=conv_kk_in.SJ[i]                                                      #试验车进入路段时间
    match_single=conv_kk_out[conv_kk_out['TRAVELID']==conv_kk_in.TRAVELID[i]]      #匹配试验车出去的记录
    end_time=match_single.SJ[int(match_single.index[0])]                            #根据试验车出去的记录，获取出去时间
    vel=conv_kk_out[(conv_kk_out['SJ']>=start_time) & (conv_kk_out['SJ']<end_time)]#筛选这段时间内出去的车，这里有一个小问题，就是没有算上超过试验车的车
    n,col2=vel.shape                                                                #获取路段中车的数量
    if (n==0) or ((end_time-start_time).seconds>120):   #筛选路段中无车、停留时间大于两分钟的数据
        k_r[i]=0
        q_r[i]=0
    else:
        k_r[i]=n/0.38                #计算路段的密度
        ut=np.average(vel.SPEED)     #计算时间平均车速
        q_r[i]=k_r[i]*ut             #路段流量

    if start_time<time1:
        ax1.scatter(k_r[i], q_r[i], color="red",marker='+',label='6:00-8:00') # 这里的label不出来，目前没解决
    elif (start_time>=time1) & (start_time<time2):
        ax1.scatter(k_r[i], q_r[i], color="blue",marker='+',label='8:00-10:00')
    else:
        ax1.scatter(k_r[i], q_r[i], color="green",marker='+',label='10:00-12:00')

plt.show()