import matplotlib.pyplot as plt
import numpy as np
from math import *
from decimal import *
from mpl_toolkits.mplot3d import Axes3D


v_max = 2
hc = 2
a = 1.5
h0 = 2

τ = 0.01
m = int(1000/τ)

def tanh(x):
    return (exp(x)-exp(-x))/(exp(x)+exp(-x))

def V(h):
    return (v_max/2)*(tanh(h-hc)+tanh(hc))

#初始时刻车辆加速度、速度、位置和车头间距
a_all = np.zeros((m,100))
v_all = np.zeros((m,100))
x_all = np.zeros((m,100))
l_all = np.zeros((m,100))

for j in range(100):
    v_all[0,j] = V(h0)
    x_all[0,j] = h0*j
    l_all[0,j] = h0

#头车加入扰动后
v_all[1,0] = V(h0)+0.01*τ
x_all[1,0] = 0 + τ*V(h0)+ 0.005*τ*τ


#τ时刻
for j in range(1,100):
    v_all[1,j] = V(h0)

for j in range(1, 100):
    x_all[1,j] = x_all[0,j]+ τ*V(h0)

for j in range(0, 100):
    if j == 99 :
        l_all[1,j] = x_all[1,0]+ h0*100 - x_all[1,j]
    else:
        l_all[1,j] = x_all[1,j+1]- x_all[1,j]

t_all = np.arange(0+2*τ,1000,τ)


for i in range(1,m-1):

    for j in range(100):
        a_all[i,j] = a*(V(l_all[i,j])-v_all[i,j])

    for j in range(100):
        v_all[i+1,j] = v_all[i,j]+ a_all[i,j]*τ

    for j in range(100):
        x_all[i+1,j] = x_all[i,j]+v_all[i,j]*τ

    for j in range(100):
        if j == 99:
            l_all[i+1,j] = x_all[i+1,0] + h0*100 - x_all[i+1,j]
        else:
            l_all[i+1,j] = x_all[i+1,j+1] - x_all[i+1,j]

print(x_all)
print(l_all)



