from numpy import *

def loadDataset(filename):
    dataMat = []
    tempmat = []
    labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split(' ')
        temp = [1]
        temp.extend(curLine)
        tempmat.append(temp)
    m, n = shape(tempmat)
    del(tempmat[0])
    for line in tempmat:
        labelMat.append(float(line[-1]))
        del(line[-1])
        dataMat.append(map(float, line))
    return dataMat, labelMat

def sigmod(inX):
    return 1/(1+exp(-inX))

def logistic(dataMat, labelMat):
    m, n = shape(dataMat)
    alpha = 0.01
    maxCycles = 500
    weights = ones((n, 1))
    for k in range(maxCycles):
        h = sigmod(dataMat*weights)
        error = labelMat - h
        weights = weights + alpha * dataMat.transpose() * error
    res = sigmod(dataMat*weights)
    err = 0
    for i in range(m):
        if res[i] > 0.5:
            res[i] = 1
        else:
            res[i] = 0
        if res[i] != labelMat[i]:
            err += 1
    print err

    import matplotlib.pyplot as plt
    x1 = []; y1 = []
    x2 = []; y2 = []
    m ,n = shape(dataMat)
    for i in range(m):
        if int(labelMat[i]) == 1:
            x1.append(dataMat[i, 1]); y1.append(dataMat[i, 2])
        else:
            x2.append(dataMat[i, 1]); y2.append(dataMat[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x1, y1, s=30, c='red', marker='s')
    ax.scatter(x2, y2, s=30, c='green')
    x = arange(0, 1, 0.01)
    y = (-weights[0]-weights[1]*x)/weights[2]
    tempy = []
    m, n = shape(y)
    for i in range(n):
        tempy.append(y[0,i])
    ax.plot(x, tempy)
    plt.show()

dataMat, labelMat = loadDataset('./data/watermalon_3_alpha.txt')
dataMat = mat(dataMat)
labelMat = mat(labelMat).transpose()
logistic(dataMat, labelMat)