from numpy import *

def loadDataSet(filename):
    dataMat = []; labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]), float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat, labelMat

def selectJrand(i, m):
    j = i
    while (j==i):
        j = int(random.uniform(0, m))
    return j

def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if L > aj:
        aj = L
    return aj

def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMat = mat(dataMatIn); labelMat = mat(classLabels).transpose()
    b = 0;  m, n = shape(dataMat)
    alphas = mat(zeros((m, 1)))
    iter = 0
    while (iter < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            fXi = float(multiply(alphas, labelMat).T*(dataMat*dataMat[i,:].T)) + b
            Ei = fXi - float(labelMat[i])  # tolerance scope
            if ((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or ((labelMat[i]*Ei > toler) and (alphas[i] > 0)):  # alpha can be optimized ?
                j = selectJrand(i, m)  # randomly select 2th alpha
                fXj = float(multiply(alphas, labelMat).T*(dataMat*dataMat[j, :].T)) + b
                Ej = fXj - float(labelMat[j])
                alphaIold = alphas[i].copy()  # create new address space
                alphaJold = alphas[j].copy()
                if (labelMat[i] != labelMat[j]):  # limit alpha in range(0, C)
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L==H: print "L==H"; continue
                eta = 2.0 * dataMat[i, :] * dataMat[j, :].T - dataMat[i, :]*dataMat[i, :].T - dataMat[j, :]*dataMat[j, :].T
                if eta >= 0: print "eta>=0"; continue
                alphas[j] -= labelMat[j] * (Ei - Ej)/eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if (abs(alphas[j] - alphaJold) < 0.00001):
                    print "j not moving enough"; continue
                alphas[i] += labelMat[j]*labelMat[i]*(alphaJold - alphas[j])
                b1 = b - Ei - labelMat[i]*(alphas[i]-alphaIold)*dataMat[i, :]*dataMat[i, :].T - labelMat[j]*(alphas[j]-alphaJold)*dataMat[i, :]*dataMat[j, :].T
                b2 = b - Ej - labelMat[i]*(alphas[i]-alphaIold)*dataMat[i, :]*dataMat[j, :].T - labelMat[j]*(alphas[j]-alphaJold)*dataMat[j, :]*dataMat[j, :].T
                if (0 < alphas[i]) and (C > alphas[i]): b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): b = b2
                else: b = (b1 + b2) / 2.0
                alphaPairsChanged += 1
                print "iter: %d i: %d, pairs change %d" % (iter, i, alphaPairsChanged)
        if (alphaPairsChanged == 0): iter += 1
        else: iter = 0
        print "iteration number: %d" % iter
    return b, alphas

def plotBestFit(dataMat, labelMat, alphas, b):
    import matplotlib.pyplot as plt
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    sxcord = []; sycord = []
    womiga = []
    for i in range(n):
        womiga.append(alphas[i]*dataArr[i, 0]*dataArr[i, 1])
        if int(labelMat[i]) > 0:
            if alphas[i]>0:
                sxcord.append(dataArr[i, 0]); sycord.append(dataArr[i, 1])
                continue
            xcord1.append(dataArr[i, 0]); ycord1.append(dataArr[i, 1])
        elif int(labelMat[i]) < 0:
            if alphas[i]>0:
                sxcord.append(dataArr[i, 0]); sycord.append(dataArr[i, 1])
                continue
            xcord2.append(dataArr[i, 0]); ycord2.append(dataArr[i, 1])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    ax.scatter(sxcord, sycord, s=40, c='color')
    womiga = mat(womiga).transpose()
    x = range[-2, 12, 0.1]
    y = multiply(womiga, x)+b
    ax.plot(x, y)
    plt.show()









    # dataMat = []
    # labelMat = []
    # for i in range(len(dataArr)):
    #     if (alphas[i] > 0):
    #         dataMat.append(dataArr[i])
    #         labelMat.append(labelArr[i])



dataArr, labelArr = loadDataSet('testSet.txt')
b, alphas = smoSimple(dataArr, labelArr, 0.6, 0.001, 40)
# b = -3.83770979
# alphas = [ 0.13479885, 0.21636047, 0.01726106, 0.36842038]
# for i in range(100):
#     if alphas[i]>0: print dataArr[i], labelArr[i]
plotBestFit(dataArr, labelArr, alphas, b)

# print array(dataArr)[0][0]