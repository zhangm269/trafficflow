import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D
import math

e=math.e


#下面为模型的一些参数选取，具体意义看PPT
N=100#车辆数
v_max=2#最大速度
h_c=2#
b=2#初始车头间距
a=2#敏感强度，为反应时间的倒数
L=b*N#环形路的长度
T=0.2#反应时间
y=0.1
tao = 0.2
#tanh函数，优化速度模型
def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

def V_opt(x):
    if(x<1):
        return 0
    elif(x<=5):
        return 0.5*(x-1)
    else:
        return 2


start_time=0
end_time=1000
t=np.linspace(start_time,end_time,int((end_time-start_time)/T+1))#时间
t_gap=t[1]-t[0]#时间间隔，步长

x=np.zeros([N,len(t)])#记录各车的行驶距离
xx=np.zeros([N,len(t)])
h_gap=np.zeros([len(t),N])#记录车头间距
hh_gap=np.zeros([len(t),N])

x[0,0]=b*(N-1)+y
x[0,1]=x[0,0]
h_gap[0,0]=L-x[0,0]
h_gap[1,0]=L-x[0,1]

x[1,0]=b*(N-2)
x[1,1]=x[1,0]
h_gap[0,1]=x[0,0]-x[1,0]
h_gap[1,1]=x[0,1]-x[1,1]



xx[0,0]=b*(N-1)
xx[0,1]=xx[0,0]
hh_gap[0,0]=L-xx[0,0]
hh_gap[1,0]=L-xx[0,1]

xx[1,0]=b*(N-2)
xx[1,1]=xx[1,0]
hh_gap[0,1]=xx[0,0]-xx[1,0]
hh_gap[1,1]=xx[0,1]-xx[1,1]

for i in range(2,N):#第三辆车之后的车辆初始状态
    x[i,0]=b*((N-1)-i)#第一时刻位移
    x[i,1]=x[i,0]#第二时刻位移
    h_gap[0,i]=b#初始车头间距
    h_gap[1,i]=b#第二时刻车头间距

    xx[i,0]=b*((N-1)-i)#第一时刻位移
    xx[i,1]=xx[i,0]#第二时刻位移
    hh_gap[0,i]=b#初始车头间距
    hh_gap[1,i]=b#第二时刻车头间距
    pass



#以下为车辆行为更新
for j in range(0,len(t)-2):#时间循环
    
    #机算x_0(t+2),h_gap[j,0]为t时刻车头间距

    x[0,j+2]=x[0,j+1]+t_gap*(v_max/2*(tanh(h_gap[j,0]-h_c)+tanh(h_c)))
#    x[0,j+2]=x[0,j+1]+T*(V_opt(h_gap[j,0]))
    if(x[0,j+2]>L):#环形路段模拟
        x[0,j+2]=x[0,j+2]-L
        pass
    
    for i in range(1,N):#车辆循环
        
        x[i,j+2]=x[i,j+1]+t_gap*(v_max/2*(tanh(h_gap[j,i]-h_c)+tanh(h_c)))
#        x[i,j+2]=x[i,j+1]+T*(V_opt(h_gap[j,i]))
        
        
        if(x[i,j+2]>L):
            x[i,j+2]=x[i,j+2]-L
            pass
        
        h_gap[j+2,i]=x[i-1,j+2]-x[i,j+2]            
        if(h_gap[j+2,i]<0):
            h_gap[j+2,i]=L-x[i,j+2]+x[i-1,j+2]
            pass
        pass

    
    h_gap[j+2,0]=x[N-1,j+2]-x[0,j+2]#记录dalta x_0(t+2)
    if(h_gap[j+2,0]<0):
        h_gap[j+2,0]=L-x[0,j+2]+x[N-1,j+2]
        pass



    #机算x_0(t+2),h_gap[j,0]为t时刻车头间距
    xx[0,j+2]=xx[0,j+1]+t_gap*(v_max/2*(tanh(hh_gap[j,0]-h_c)+tanh(h_c)))
#    xx[0,j+2]=xx[0,j+1]+T*(V_opt(hh_gap[j,0]))
    if(xx[0,j+2]>L):#环形路段模拟
        xx[0,j+2]=xx[0,j+2]-L
        pass
    
    for i in range(1,N):#车辆循环
        
        xx[i,j+2]=xx[i,j+1]+t_gap*(v_max/2*(tanh(hh_gap[j,i]-h_c)+tanh(h_c)))
 #       xx[i,j+2]=xx[i,j+1]+T*(V_opt(hh_gap[j,i]))
        
        
        if(xx[i,j+2]>L):
            xx[i,j+2]=xx[i,j+2]-L
            pass
        
        hh_gap[j+2,i]=xx[i-1,j+2]-xx[i,j+2]            
        if(hh_gap[j+2,i]<0):
            hh_gap[j+2,i]=L-xx[i,j+2]+xx[i-1,j+2]
            pass
        pass

    
    hh_gap[j+2,0]=xx[N-1,j+2]-xx[0,j+2]#记录dalta x_0(t+2)
    if(hh_gap[j+2,0]<0):
        hh_gap[j+2,0]=L-xx[0,j+2]+xx[N-1,j+2]
        pass

    pass





'''
for i in range(1,int(N/25)):
    plt.plot(t,x[(i-1)*25]-x[i*25])
plt.show()
'''
'''
dd=np.linspace(0,5,100)
plt.plot(dd,v_max/2*(tanh(dd-h_c)+tanh(h_c)))
plt.show()
'''

for i in range(int(N/50)):
    plt.plot(t,x[i*50])
plt.show()

for i in range(int(N/50)):
    plt.plot(t,xx[i*50])
plt.show()

'''
for i in range(len(t)):
    print(h_gap[i,0])
    pass
'''

'''  
for i in range(N):
    print(h_gap[900,i])
    pass
'''





fig = plt.figure()
ax = Axes3D(fig)
for i in range(int(len(t)*8/100),int(len(t)/10)):
    X = range(100)
    Y = np.zeros([N])
    for j in range(N):
        Y[j]=t[i*10]
        pass
    Z = h_gap[i*10]
#    print(Z[:100])
    ax.plot(X[:100], Y[:100], Z[:100])
    pass
#ax.set_title("Gap")
ax.set_xlabel("Car Number")
ax.set_ylabel("Time")
ax.set_zlabel("Headway")
ax.set_zlim(0,4)
#ax.set_ylim(0,100)
plt.show()

cc=np.zeros([N])
fig2 = plt.figure()
ax1 = Axes3D(fig2)
for i in range(int(len(t)*4/100),int(len(t)/20)):
    XX = range(100)
    YY = np.zeros([N])
    for j in range(N):
        YY[j]=t[i*20]
        cc[j]=b
        pass
    ZZ = h_gap[i*20]-hh_gap[i*20]+cc
#    print(ZZ[:100])
    ax1.plot(XX[:100], YY[:100], ZZ[:100])
    pass
#ax.set_title("Gap")
ax1.set_xlabel("Car Number")
ax1.set_ylabel("Time")
ax1.set_zlabel("Headway")
ax1.set_zlim(0,4)
#ax1.set_ylim(0,100)
plt.show()


def dV_opt(dd,h_c,v_max):
    return v_max/2*4*np.exp(-2*(dd-h_c))/(1+np.exp(-2*(dd-h_c)))**2
    
dd=np.linspace(2,5,100)
plt.plot(dd,dV_opt(dd,h_c,v_max),'y',label='V’(x)')
plt.plot([min(dd),max(dd)],[a/2,a/2],'r',label='a/2')
plt.plot([b,b],[0,1],'g',label='b')
plt.scatter(b,dV_opt(b,h_c,v_max),c='r',marker='x',label='V’(b)')
if(dV_opt(b,h_c,v_max)<a/2):
    plt.title('稳定')
    pass
elif(dV_opt(b,h_c,v_max)==a/2):
    plt.title('临界稳定')
    pass
else:
    plt.title('不稳定')
    pass
plt.xlabel("x")
plt.ylabel("V’(x)")
plt.grid()
plt.legend()
plt.rcParams['font.sans-serif']=['SimHei']#显示中文标题
plt.rcParams['axes.unicode_minus'] = False
plt.show()
