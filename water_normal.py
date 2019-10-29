import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import wntr
import pandas as pd


"""
Pattern(name[, multipliers, time_options, wrap])
Pattern class.
TimeSeries(model, base[, pattern_name, category])
Time series class.
Demands(patterns, *args)
Demands class.
"""

"""

需求结果是以m3/s为单位的,此为si单位
但用C++调用epanet的输出的报告文件是以GPM为单位的

转换：1GPM=0.003785411784/60.0m3/s
      1GPM=0.06308L/S
      1L/S=0.001m3/s      

"""

def getWaterNetworkModel(inp_file):
    file=inp_file
    wn = wntr.network.WaterNetworkModel(file)
    return wn
def getRandomDemand(wn,length=1317,Size=1000):
    """
    获得节点的随机需水量矩阵，形状：length*Size
    :param wn:
    :param length: 每个行向量的长度，代表生成多少节点的随机需求，从矩阵看是多少列
    :param Size: 代表每个节点生成多少个随机需求，从矩阵看是多少行
    :return: 返回矩阵(单位未转化为GPM)
    """
    sim = wntr.sim.EpanetSimulator(wn)#库->包->模块->类/函数
    results =sim.run_sim()
    #print(results.node['demand'].loc[0,:])
    #series=results.node['demand'].loc[0,:]/(0.003785411784/60.0) #把流量单位m3/s转换为GPM,结果为0时刻所有节点的需求值
    series=results.node['demand'].loc[0,:]
    np.set_printoptions(suppress=True)  #取消科学计数法
    mean = np.array(series[0:length].values)   #以0时的基本需水量为均值,长度为1317
    sigma=mean*0.1          #标准差为节点基本需求的10%，
    var=sigma**2            #矩阵每个元素都取平方为节点方差
    conv=np.diag(var)       #协方差矩阵
    np.random.seed(1)       #保证每次试验生成的随机样本是一样的
    random_demand= np.random.multivariate_normal(mean=mean, cov=conv, size=Size)     #随机抽取多元正太分布变量的样本，这是实际需水量。random_demand.shape=(1000, 1317)
    # node_name_list = wn.node_name_list[0:1317]
    # length=len(random_demand[0])
    for i in range(len(random_demand)):#把需水量为0的节点的随机需水量该为0
        for j in range(length):
            if(mean[j]==0):
                random_demand[i][j]=0
    return random_demand

def saveRandomDemand(random_demand):
    """
    :param random_demand: 随机需水量
    :return: 保存成单位为GPM的随机需水量矩阵
    """
    random_demand=random_demand/(0.003785411784/60.0)
    np.savetxt('random_demand.txt',random_demand,fmt='%.15f')

def getRandomPressureFromFile(fileName,wn):
    # node_name_list = wn.node_name_list[0:1317]
    pressure=[]
    with open(fileName, 'r') as file:
        for line in file:
            data=line.split()
            data = list(map(float, data))
            pressure.append(data)
    pressure=np.array(pressure)
    return pressure

def drawRandomData(random_Data,flag=False):
    """
    打印前几个节点的随机抽样的需水量分布图像（概率密度函数）
    :param random_demand:
    :param flag:设置是否显示生成的图像，默认不显示
    :return:
    """
    # print(random_demand.mean(axis=0))    #打印样本平均值
    # print(random_demand.std(axis=0))     #打印样本标准差
    for i in range(4):
        plt.subplot(221 + i)
        n, bins, patches = plt.hist(random_Data[:, i]/(0.003785411784/60.0), 1000, facecolor='green', alpha=0.5)
        # plt.xlabel('Expectation(GPM)')
        plt.xlabel('Expectation')
        plt.ylabel('frequency')
        plt.title('σ=%s' % random_Data[:, i].std())

    # y = mlab.normpdf(bins,mean[0] , sigma[0]) #求bins对应的变量的概率密度
    # plt.plot(bins, y, 'r--')        #画拟合函数
    plt.tight_layout()
    #print(random_demand)
    if(flag==True):
        plt.show()

if __name__=="__main__":
    file = "resoures/Net3.inp"
    wn=getWaterNetworkModel(file)
    random_demand=getRandomDemand(wn,length=92)
    saveRandomDemand(random_demand)
    # #drawRandomDemand(random_demand,flag=True)
    pressureFilePath = "resoures/randomPressure.txt"
    # pressure=getRandomPressureFromFile(pressureFilePath,wn)
    # drawRandomData(pressure, flag=True)
    print(random_demand.shape)



















