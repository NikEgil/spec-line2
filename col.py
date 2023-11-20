import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import statistics as st
from scipy import signal
path_folder = "C:/Users/Nik/Desktop/prog/set/"
size = 1    #кол-во графиков
s=0         #начальный файл
#153 884    измеряемый диапазон. 0-2136 диапазон данных
start=400   #нм
end=700     #нм
step = (884-153)/2134

start_point=round((start-153)/step)
end_point=start_point+int((end-start)/step)

print(step, start_point, end_point)

file_list =np.array( os.listdir(path_folder))
n=len(file_list)
print(n)
y= np.zeros(int((end-start)/step))
x=np.arange(start+step, end,step)
mas=np.zeros((1,len(x)))
crit=0.1

s=0

for i in range(len(file_list)):
    spec= open(str(path_folder+file_list[i]), "r", encoding="utf8")
    spec = spec.read().split(",")
    for j in range(start_point,end_point):
        y[j-start_point]=float(spec[j+11])
    mean= np.mean(y [len(y)-150:len(y)-100])
    y-=mean
    if np.max(y)>=crit:
        s+=1
        mas=np.append(mas,[y],axis=0)
    print(len(mas))
mas=np.delete(mas,0,0)

def sums(ar):
    a=np.zeros(len(ar[0]))
    for i in range(len(ar)):
        for j in range(len(ar[0])):
            a[j]+=ar[i][j]
    return a

def mean(ar):
    a=np.zeros(len(ar[0]))
    for i in range(len(ar)):
        for j in range(len(ar[0])):
            a[j]+=ar[i][j]
    a/=len(ar)
    return a

plt.subplot(111)
plt.plot(x,mean(mas),linewidth=1)
plt.legend(loc=1, title=s)

plt.show()

    
