'''
本次的建模分为五个场景，第一个场景我已经完成，各场景介绍见交通流理论第四章ppt（主要是11到20页）介绍，根据自己的需要添加各自部分的代码（看清楚要求，都是很简单的代码），
关于用到的各自阶段用到的一些特殊变量（其他场景用不到的）可以自行添加使用。
'''
import numpy as np
import matplotlib.pyplot as plt

x_i=[0]#用于记录第i辆车的行驶距离
v_i=[0]#用于记录第i辆车的速度
a_i=[0]#用于记录第i辆车的加速度

x_j=[40]    #用于记录第(i-1)辆车(前车)的行驶距离
v_j=[0]     #用于记录第(i-1)辆车的速度
a_j=[0]     #用于记录第(i-1)辆车的加速度

#以下四个变量用于计算过程中的用于记录某一时刻的“时刻、加速度、速度、行驶距离、车头间距”
t0=0
a0=0
v0=0
x0=0
h=40

#接下来是一些可变参数的设置(根据不同场景可自行添加)
start_time=0    #开始时间
final_time=450  #结束时间
time_gap=0.1    #计数间隔
T=0.5           #反应时间
r=0.5           #反应强度（用于计算减速度）ppt第20页
v_max=36        #第i辆车的最大行驶速度，即理想速度
v1=24             #前车速度，场景三用到
a=5             #场景一用到的加速度大小
a2=3            #制动加速度，场景二用到
a3=-3             #前车减速度，场景三用到
n_label=0       #判断场景一加速是否完城的标记
l_j=4           #定义前车车长为4米
safety=200      #根据《道路交通安全法实施条例》，高速公路建议两车距离为200米

t=np.linspace(start_time,final_time,int((final_time-start_time)/time_gap+1))#均匀产生从start_time（0）到final_time（450）的（(final_time-start_time)/time_gap+1）（4501）个浮点数数

for i in range(int(100/time_gap+1)):#场景一，前100秒启动、加速自由流行驶过程
    if((a*t[i])<v_max):
        t0=t[i]#记录此时刻
        a0=a#记录此时的加速度
        v0=a*t0#计算此时的速度
        x0=0.5*a*t[i]**2#计算此时的行驶距离
    if((a*t[i])>=v_max):
        t0=t[i]
        a0=0
        v0=v_max
        x0=x0+v_max*time_gap
        if(n_label==0):
            print('第%.2f秒的时候完成加速'%t0)
            n_label=1
    a_i.append(a0)#往加速度数组中添加记录
    v_i.append(v0)#往速度数组中添加记录
    x_i.append(x0)#往行驶距离数组中添加记录
    a_j.append(0)
    v_j.append(24)
    x_j.append(x0+h)#往第(i-1)辆车行驶距离数组中添加记录

v_j2=24                                 #设置i-1车初始速度

# for i in range(int(100/time_gap+1),int(200/time_gap+1)):#场景二，被抢道、跟驰过程（100秒）
#     v_j.append(v_j2)                #记录i-1车的速度
#     t0=t[i]                         #保持绘图的横坐标在100-200之间
#     t2=t[i]-100                     #记录该场景的相对时间
#     if t2<T:                    #驾驶员反应车辆i-1需要T时间
#         a0=0                    #记录反应时间内，i车的加速度、速度、车头间距
#         v0=v_max
#         h=h+(v_j2-v0)*time_gap
#     else:                       #反应结束，开始刹车
#         if v0>=v_j2:
#             a0=r*(v_j2-v0)              #记录反应时间内，i车的加速度、速度、车头间距
#             v0=v0+a0*time_gap
#             h=h+(v_j2-v0)*time_gap
#
#     x0=x0+v0*time_gap
#     a_i.append(a0)
#     v_i.append(v0)
#     x_i.append(x0)
#     x_j.append(x0+h)

### 为了让跟驰模型更合理，这里新写了一段防撞的代码以保持与实际相符的合理性，加速度减少到3m/s²时,保持3m/s²的减速度继续减少
### 之后再以5m/s增加直到与前车保持匀速且距离为高速公路安全距离200米
flag = 0                                #设置flag来转换车的加减速状态

for i in range(int(100/time_gap+1),int(200/time_gap+1)):#场景二，被抢道、跟驰过程（100秒）
    v_j.append(v_j2)                #记录i-1车的速度
    t0=t[i]                         #保持绘图的横坐标在100-200之间
    t2=t[i]-100                     #记录该场景的相对时间
    if flag==0:
        if t2<T:                    #驾驶员反应车辆i-1需要T时间
            a0=0                    #记录反应时间内，i车的加速度、速度、车头间距
            v0=v_max
            h=h+(v_j2-v0)*time_gap
        else:                       #反应结束，开始刹车
            # 加入距离过近的修正方案，如果距离过近，就会退回200米之外，即减速再加速的过程正好让i车与i-1车距离20米
            if h<(safety-(v_j2*v0*2-v0**2)*(24/(v_j2+v0)-1/2)/a):
                if v0>60/3.6:           #60km/h为正常情况下高速公路最低行驶速度，减速到60km/h取消减速
                    if a0>-a2:          #减速度小于a2时，保持a2不变继续减速
                        a0=r*(v_j2-v0)  #记录反应时期减速过程的加速度变化
                    else:
                        a0=-a2
                else:
                    v0=60/3.6
                    a0=0
                v0 = v0 + a0 * time_gap #记录减速过程的速度、车头间距
                h=h+(v_j2-v0)*time_gap
            else:
                flag=1
    else:                       #减速结束，进入加入过程，让i车与i-1车保持匀速且距离为200米
        a0=a                    #记录第二次加速过程的加速度、速度、车头间距
        v0 = v0 + a0 * time_gap
        h = h + (v_j2 - v0) * time_gap
        if v0>v_j2:             #如果两车速度相同，则他们保持匀速，永远不会相撞
            v0=v_j2
            a0=0
            h=safety

    x0=x0+v0*time_gap            #记录该过程的i车轨迹
    a_i.append(a0)
    v_i.append(v0)
    x_i.append(x0)
    a_j.append(0)
    v_j.append(v_j2)
    x_j.append(x0+h)

ft=0   #表示驾驶员反应的变量
t31=0

for i in range(int(200/time_gap+2),int(300/time_gap+1)):#场景三，停车起步过程（100秒）
    t0=t[i]                         #记录i-1车的速度
    t3=t[i]-200                     #保持绘图的横坐标在200300之间
    t31=t31+time_gap                #用于计算反应时间

    if t0<250:
        if v1>=0:                       #前车动作，车辆做匀减速运动直至速度减至0
            a3=-3
            v1=v1+a3*time_gap
        else:
            a3=0
            v1=0

#    else:                               #车辆启动测试，可去掉
#        if v1<24:
#            a3=3
#            v1=v1+a3*time_gap
#        else:
#            a3=0
#            v1=24


    if ft==0:                        #判断跟车状况是否发生变化
        if h<safety:                 #车距小于安全距离需要改变行车状况
            ft=1
            t31=0                    #反应时间统计
        else:
            if v1!=v0:               #车速与前车不同需要改变尽量相同
                ft=1
                t31=0
        a0=0                         #此时视为车辆无动作
        h=h+(v1-v0)*time_gap
        x0=x0+v0*time_gap
        v0=v0+a0*time_gap
    else:                                                           #判断反应时间
        if t31>=T:                                                  #达到反应时间
            if v0<=0:                                               #判断车辆是否静止，静止时将速度与加速度置零，视为停车
                    a0=0
                    h=h
                    x0=x0
                    v0=0
                    ft=0                                            #解除警报
                    if v1>0:                                        #若前车启动则跟随启动
                        a0=a
                        h=h+(v1-v0)*time_gap
                        x0=x0+v0*time_gap
                        v0=v0+a0*time_gap
            else:                                                   #路上正常行驶时
                if h<safety:                                        #状况为车距小于安全距离，则车辆减速
                    a0=-a
                    h=h+(v1-v0)*time_gap
                    x0=x0+v0*time_gap
                    v0=v0+a0*time_gap
                else:                                               #状况为车速大于前车，则车辆减速
                    if v0>v1:
                        a0=-a
                        h=h+(v1-v0)*time_gap
                        x0=x0+v0*time_gap
                        v0=v0+a0*time_gap
                    else:
                        if v0==v1:                                  #状况为车速与前车相同，且车距合适，则车辆维持，并解除警报
                            a0=0
                            h=h+(v1-v0)*time_gap
                            x0=x0+v0*time_gap
                            v0=v0+a0*time_gap
                            ft=0
                        else:                                       #状况为车速小于前车，则车辆加速
                                a0=a
                                h=h+(v1-v0)*time_gap
                                x0=x0+v0*time_gap
                                v0=v0+a0*time_gap
        else:
                a0=0                                                #未到达反应时间则视为无动作
                h=h+(v1-v0)*time_gap
                x0=x0+v0*time_gap
                v0=v0+a0*time_gap
             
    a_i.append(a0)
    v_i.append(v0)
    x_i.append(x0)
    a_j.append(a3)
    v_j.append(v1)
    x_j.append(x0+h)
#print(x0)
#print(v0)
#print(a0)
#print(h)

a_41=2
v_41=0
x_41=x0+h

for i in range(int(300/time_gap+2),int(400/time_gap+1)):#场景四，随行过程（100秒）
    t0=t[i]
    a0=a0
    v0=v0
    x0=x0
    if(v_41<=v_max and v0<=v_max):
        a_41=2
        v_41=v_41+a_41*time_gap
        x_41=x_41+0.5*a_41*time_gap**2
        if(t0-t[int(300/time_gap+2)]<=T):
            a0=0
            v0=0
            x0=x0
            h=x_41-x0
        else:
            a0=r*(v_41-v0)
            v0=v0+a0*time_gap
            x0=x0+0.5*a0*time_gap**2
            h=x_41-x0
            pass
        pass
    if(v_41>=v_max and v0<v_max):
        v_41=v_max
        a_41=0
        x_41=x_41+v_41*time_gap

        a0=r*(v_41-v0)
        v0=v0+a0*time_gap
        x0=x0+0.5*a0*time_gap**2
        h=x_41-x0
        pass
    if(v_41>=v_max and v0>=v_max):
        a_41=0
        v_41=v_max
        x_41=x_41+v_41*time_gap

        a0=0
        v0=v_max
        x0=x0+v0*time_gap
        h=x_41-x0
        
    a_i.append(a0)
    v_i.append(v0)
    x_i.append(x0)
    a_j.append(a_41)
    v_j.append(v_41)
    x_j.append(x_41)
    pass

"""
场景五基于场景四下的匀速跟驰，假设在场景四的基础上已经保持了相对速度和安全间距
"""

ft = 0  # 表示驾驶员反应的变量
t31 = 0
v1 = 36
for i in range(int(400 / time_gap + 2), int(450 / time_gap + 1)):  # 场景五，靠近过程（20秒）
    t0 = t[i]  # 记录i-1车的速度
    t31 = t31 + time_gap  # 用于计算反应时间
    if v1 > 0:  # 前车动作，车辆做匀减速运动直至速度减至0
        a3 = -3
        if v1 + a3 * time_gap <= 0:
            v1 = 0
        else:
            v1 = v1 + a3 * time_gap
    else:
        a3 = 0
        v1 = 0
    if ft == 0:  # 判断跟车状况是否发生变化
        if h < safety:  # 车距小于安全距离需要改变行车状况
            ft = 1
            t31 = 0  # 反应时间统计
        else:
            if v1 != v0:  # 车速与前车不同需要改变尽量相同
                ft = 1
                t31 = 0
        a0 = 0  # 此时视为车辆无动作
        h = h + (v1 - v0) * time_gap
        x0 = x0 + v0 * time_gap
        v0 = v0 + a0 * time_gap
    else:  # 判断反应时间
        if t31 >= T:  # 达到反应时间
            if v0 <= 0:  # 判断车辆是否静止，静止时将速度与加速度置零，视为停车
                a0 = 0
                h = h
                x0 = x0
                v0 = 0
                ft = 0  # 解除警报
            else:  # 路上正常行驶时
                if h < safety:  # 状况为车距小于安全距离，则车辆减速
                    a0 = r * (v1 - v0)
                    h = h + (v1 - v0) * time_gap
                    x0 = x0 + v0 * time_gap
                    v0 = v0 + a0 * time_gap
                else:
                    if h > 200:
                        a0 = 0  # 未达到警示距离则视为无动作
                        h = h + (v1 - v0) * time_gap
                        x0 = x0 + v0 * time_gap
                        v0 = v0 + a0 * time_gap
                    else:
                        if v0 > v1:  # 状况为车速大于前车且间距小于300m，则车辆减速

                            a0 = r * (v1 - v0)
                            h = h + (v1 - v0) * time_gap
                            x0 = x0 + v0 * time_gap
                            v0 = v0 + a0 * time_gap
                        else:
                            if v0 == v1:  # 状况为车速与前车相同，且车距合适，则车辆维持，并解除警报
                                a0 = 0
                                h = h + (v1 - v0) * time_gap
                                x0 = x0 + v0 * time_gap
                                v0 = v0 + a0 * time_gap
                                ft = 0
                            else:  # 状况为车速小于前车，则车辆加速
                                a0 = r * (v1 - v0)
                                h = h + (v1 - v0) * time_gap
                                x0 = x0 + v0 * time_gap
                                v0 = v0 + a0 * time_gap
        else:
            a0 = 0  # 未到达反应时间则视为无动作
            h = h + (v1 - v0) * time_gap
            x0 = x0 + v0 * time_gap
            v0 = v0 + a0 * time_gap

    a_i.append(a0)
    v_i.append(v0)
    x_i.append(x0)
    x_j.append(x0 + h)
    

t_finally=np.linspace(400,t0,len(a_i[4000:]))#记录已完成过程的时间，注意"t0"一定要更新
#print(t)
#print(x_i)
#print(v_i)
#print(a_i)


'''
作图
'''
x=t_finally#横坐标为时间
y0=x_i[4000:]#第i辆车的行驶距离
y=x_j[4000:]#第(i-1)辆车的行驶距离
y1=v_i[4000:]#第i辆车的行驶速度
y2=a_i[4000:]#第i辆车的加速度
y3=[]#车头间距
for i in range(len(x_i)):
    jian_ju=x_j[i]-x_i[i]
    if(jian_ju<l_j):#判断是否撞车
        print("在第%.2f时刻发生撞车"%i*0.5)
    else:#如果没有撞车，往车头间距数组中添加记录
        y3.append(jian_ju)
y3=y3[4000:]

ax1=plt.subplot(221)
plt.plot(x,y0,color='g',label='x_i')
plt.plot(x,y,color='r',label='x_j')
ax1.set_xlabel('t(s)')
ax1.set_ylabel('x(m)')
plt.legend()

ax2=plt.subplot(222)
plt.plot(x,y1,color='g',label='v_i')
# plt.plot(x,v_j,color='r',label='v_j')
ax2.set_xlabel('t(s)')
ax2.set_ylabel('v(m/s)')


ax3=plt.subplot(223)
plt.plot(x,y2,color='g',label='a_i')
#plt.plot(x,a_j,color='r',label='a_j')
ax3.set_xlabel('t(s)')
ax3.set_ylabel('a(m/s^2)')

ax4=plt.subplot(224)
plt.plot(x,y3,color='b',label='h')
ax4.set_xlabel('t(s)')
ax4.set_ylabel('h(m)')
plt.tight_layout()
#plt.legend()
plt.show()
#plt.legend()

plt.show()
       
