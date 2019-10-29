#coding=utf-8
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
"""
    绘制概率密度函数曲线
"""
mean=0
std=1
x = np.arange(-1,1,0.05)
print(np.mean(x))
def normfun(x,mu,sigma):
    pdf = np.exp(-((x - mu)**2)/(2*sigma**2)) / (sigma * np.sqrt(2*np.pi))
    return pdf
y = normfun(x, mean, std)
plt.plot(x,y)
plt.show()







