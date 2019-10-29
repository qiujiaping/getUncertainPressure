#coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import wntr

"""
  正太分布随机抽样，并绘制图像
"""
mean = np.array([10,10,30])              # 均值
conv = np.array([[0.0,0.0,0.0],        # 协方差矩阵
                 [0.0,3.0,0.0],
                 [0.0,0.0,6.0]])
axis = np.random.multivariate_normal(mean=mean, cov=conv, size=200)
x, y ,z= np.random.multivariate_normal(mean=mean, cov=conv, size=1000).T

n, bins, patches = plt.hist(x, 200, normed=1, facecolor = 'green', alpha = 0.5)
# 拟合曲线
# y = mlab.normpdf(bins,10 , 1) #求bins对应的变量的概率密度
# plt.plot(bins, y, 'r--')        #画拟合函数
plt.show()
print(axis)
plt.xlabel("x")
plt.ylabel("y")
plt.plot(axis[:, 0], axis[:, 1],'ro')

plt.show()
plt.plot(x, y, 'ro')
plt.show()
