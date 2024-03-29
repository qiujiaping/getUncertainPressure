import numpy as np
from numpy import matrix as mat
from matplotlib import pyplot as plt
import random
random.seed(0)
n = 100
a1, b1, c1 = 1, 2, 3  # 这个是需要拟合的函数y(x) 的真实参数
h = np.linspace(0, 1, n).reshape(100, 1)  # 产生包含噪声的数据

y=[]
for i in h:
    r=random.gauss(0, 8);#加入噪声

    fun=np.exp(a1 * i ** 2 + b1 * i + c1)
    y.append(r+fun)
# y = [np.exp(a1 * i ** 2 + b1 * i + c1) + random.gauss(0, 8) for i in h]
J = mat(np.zeros((n, 3)))  # 雅克比矩阵

fx = mat(np.zeros((n, 1)))  # f(x)  100*1  误差
fx_tmp = mat(np.zeros((n, 1)))
xk = mat([[2.4], [2.4], [2.4]])
# xk = mat([[12.0],[12.0],[12.0]]) # 参数初始化
lase_mse = 0
step = 0
u, v = 1, 2
conve = 10000


def Func(abc, iput):  # 需要拟合的函数，abc是包含三个参数的一个矩阵[[a],[b],[c]],函数的第一个部分
    """
    :param abc: 参数
    :param iput: 输入的自变量
    :return:
    """

    a = abc[0, 0]
    b = abc[1, 0]
    c = abc[2, 0]

    return np.exp(a * iput ** 2 + b * iput + c)


def Deriv(abc, iput, n):  # 对函数求偏导（分别对a,b,c求偏导）
    """
    x1代表abc这三个参数的矩阵
    :param abc: 要拟合的参数
    :param iput: 输入的自变量len(iput)=100
    :param n: 取值在[0,1,2]控制对哪个参数求偏导
    :return:
    """

    x1 = abc.copy()
    x2 = abc.copy()
    x1[n, 0] -= 0.000001
    x2[n, 0] += 0.000001
    p1 = Func(x1, iput)
    p2 = Func(x2, iput)
    df=(p2 - p1)
    dx=0.000002
    d = df * 1.0 / dx
    return d


while (conve):
    mse, mse_tmp = 0, 0
    step += 1

    fx = Func(xk, h) - y    #残差
    mse += sum(fx ** 2) #最小二乘累计和
    for j in range(3):
        J[:, j] = Deriv(xk, h, j)  # 数值求导
    mse /= n  # 范围约束


    #理解
    H = J.T * J + u * np.eye(3)  # 3*3

    dx = -H.I * J.T * fx  #步长，也是搜寻方向
    xk_tmp = xk.copy()
    xk_tmp += dx
    fx_tmp = Func(xk_tmp, h) - y

    mse_tmp = sum(fx_tmp[:, 0] ** 2)
    mse_tmp /= n
    # 判断是否下降
    q = float((mse - mse_tmp) / ((0.5 * dx.T * (u * dx - J.T * fx))[0, 0]))
    if q > 0:
        s = 1.0 / 3.0
        v = 2
        mse = mse_tmp
        xk = xk_tmp
        temp = 1 - pow(2 * q - 1, 3)

        if s > temp:
            u = u * s
        else:
            u = u * temp
    else:
        u = u * v
        v = 2 * v
        xk = xk_tmp

    #print("step = %d,abs(mse-lase_mse) = %.8f" % (step, abs(mse - lase_mse)))
    if abs(mse - lase_mse) < 0.000001:
        break

    lase_mse = mse  # 记录上一个 mse 的位置
    conve -= 1

#print(xk)
# 用拟合好的参数画图
z = [Func(xk, i) for i in h]

plt.figure(0)
plt.scatter(h, y, s=4)  #散点图
plt.plot(h, z, 'r')
plt.show()

