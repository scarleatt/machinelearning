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

# class optStruct:
#     def __init__(self, dataMatIn, classLabels, C, toler):
#         self.X = dataMatIn
#         self.labelMat = classLabels
#         self.C = C
#         self.tol = toler
#         self.m = shape(dataMatIn)[0]
#         self.alphas = mat(zeros((self.m, 1)))
#         self.b = 0
#         self.eCathe = mat(zeros((self.m, 2)))

def calcEk(oS, k):
    fXk = float(multiply(oS.alphas, oS.labelMat).T * (oS.X*oS.X[k, :].T)) + oS.b
    Ek = fXk - float(oS.labelMat[k])
    # fXk = float(multiply(oS.alphas, oS.labelMat).T * oS.K[:, k] + oS.b)
    # Ek = fXk - float(oS.labelMat[k])
    return Ek

def selectJ(i, oS, Ei):
    maxK = -1; maxDeltaE = 0; Ej = 0
    oS.eCathe[i] = [1, Ei]
    validEcatheList = nonzero(oS.eCathe[:, 0].A)[0]
    if (len(validEcatheList)) > 1:
        for k in validEcatheList:
            if k == i: continue
            EK = calcEk(oS, k)
            deltaE = abs(Ei - EK)
            if (deltaE > maxDeltaE):
                maxK = k; maxDeltaE = deltaE; Ej = EK
        return maxK, Ej
    else:
        j = selectJrand(i, oS.m)
        Ej = calcEk(oS, j)
    return j, Ej

def updateEk(oS, k):
    Ek = calcEk(oS, k)
    oS.eCathe[k] = [1, Ek]

def innerL(i, oS):
    Ei = calcEk(oS, i)
    if ((oS.labelMat[i]*Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or ((oS.labelMat[i]*Ei > oS.tol) and (oS.alphas[i] > 0)):
        j, Ej = selectJ(i, oS, Ei)
        alphaIold = oS.alphas[i].copy(); alphaJold = oS.alphas[j].copy()
        if (oS.labelMat[i] != oS.labelMat[j]):
            L = max(0, oS.alphas[j] - oS.alphas[i])
            H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
        else:
            L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
            H = min(oS.C, oS.alphas[j] + oS.alphas[i])
        if L == H: print "L == H"; return 0
        eta = 2.0 * oS.X[i, :]*oS.X[j, :].T - oS.X[i, :]*oS.X[i, :].T - oS.X[j, :]*oS.X[j, :].T
        # eta = 2.0 * oS.K[i, j] - oS.K[i, i] - oS.K[j, j]
        if eta >= 0: print "eta>=0"; return 0
        oS.alphas[j] -= oS.labelMat[j]*(Ei-Ej)/eta
        oS.alphas[j] = clipAlpha(oS.alphas[j], H, L)
        updateEk(oS, j)
        if (abs(oS.alphas[j] - alphaJold) < 0.00001):
            print "j not moving enough"; return 0
        oS.alphas[i] += oS.labelMat[j] * oS.labelMat[i]*(alphaJold-oS.alphas[j])
        updateEk(oS, i)
        b2 = oS.b - Ei - oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.X[i, :]*oS.X[j, :].T - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.X[j, :]*oS.X[j, :].T
        b1 = oS.b - Ei - oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.X[i, :]*oS.X[i, :].T - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.X[i, :]*oS.X[j, :].T
        # b2 = oS.b - Ej - oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.K[i, i] - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.K[i, j]
        # b1 = oS.b - Ej - oS.labelMat[i]*(oS.alphas[i]-alphaIold)*oS.K[i, j] - oS.labelMat[j]*(oS.alphas[j]-alphaJold)*oS.K[j, j]
        if (0 < oS.alphas[i]) and (oS.C > oS.alphas[i]): oS.b = b1
        elif (0 < oS.alphas[j]) and (oS.C > oS.alphas[j]): oS.b = b2
        else: oS.b = (b1+b2) / 2.0
        return 1
    else: return 0

def smoP(dataMatIn, classLabels, C, toler, maxIter, kTup=('lin', 0)):
    oS = optStruct(mat(dataMatIn), mat(classLabels).transpose(), C, toler, kTup=('lin', 0))
    iter = 0
    entireSet = True; alphaPairsChanged = 0
    while (iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
        alphaPairsChanged = 0
        if entireSet:
            for i in range(oS.m):
                alphaPairsChanged += innerL(i, oS)
                print "fullSet, iter: %d i: %d, pairs changed %d" % (iter, i, alphaPairsChanged)
                iter += 1
        else:
            nonBounds = nonzero((oS.alphas.A > 0) * (oS.alphas.A < 0))[0]
            for i in nonBounds:
                alphaPairsChanged += innerL(i, oS)
                print "non-bound, iter: %d, i: %d, pairs change %d" % (iter, i, alphaPairsChanged)
                iter += 1
        if entireSet: entireSet = False
        elif (alphaPairsChanged == 0): entireSet = True
        print "iteration number: %d" % iter
    return oS.b, oS.alphas

def calcWs(alphas, dataArr, classLabels):
    X = mat(dataArr); labelMat = mat(classLabels).transpose()
    m, n = shape(X)
    w = zeros((n, 1))
    for i in range(m):
        w += multiply(alphas[i]*labelMat[i], X[i, :].T)
    return w

def plotBestFit(dataMat, labelMat, alphas, b):
    import matplotlib.pyplot as plt
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []
    sxcord = []; sycord = []
    w = 0
    for i in range(n):
        w += alphas[i]*dataArr[i, 0]*dataArr[i, 1]
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
    ax.scatter(sxcord, sycord, s=40, c='yellow')
    w = calcWs(alphas, dataArr, labelMat)
    w = w.transpose()
    x = arange(-2, 12, 0.1)
    # y = dataMat*mat(w) + b
    # ax.plot(x, y)
    plt.show()

def kernalTrans(X, A, kTup):
    m, n = shape(X)
    K = mat(zeros((m, 1)))
    if kTup[0] == 'lin': K = X * A.T
    elif kTup[0] == 'rbf':
        for j in range(m):
            deltaRow = X[j, :] - A
            K[j] = deltaRow*deltaRow.T
        K = exp(K / (-1*kTup[1]**2))
    else: raise NameError('Houston We Have a Problem -- That Kernal is not recognized')
    return K

class optStruct:
    def __init__(self, dataMatIn, classLabels, C, toler, kTup):
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = shape(dataMatIn)[0]
        self.alphas = mat(zeros((self.m, 1)))
        self.b = 0
        self.eCathe = mat(zeros((self.m, 2)))
        self.K = mat(zeros((self.m, self.m)))
        for i in range(self.m):
            self.K[:, i] = kernalTrans(self.X, self.X[i, :], kTup)

def testRbf(k1=1.3):
    dataArr, labelArr = loadDataSet('testSetRBF.txt')
    b, alphas = smoP(dataArr, labelArr, 200, 0.0001, 10000, ('rbf, k1'))
    dataMat = mat(dataArr); labelMat = mat(labelArr).transpose()
    svInd = nonzero(alphas.A > 0)
    sVs = dataMat[svInd]
    labelSV = labelMat[svInd]
    print "there are %d Support Vector" % shape(sVs)[0]
    m, n = shape(dataMat)
    errCount = 0
    for i in range(m):
        kernalEval = kernalTrans(sVs, dataMat[i, :], ('rbf', k1))
        predict = kernalEval.T * multiply(labelSV, alphas[svInd] + b)
        if sign(predict) != sign(labelArr[i]): errCount += 1
    print "the training error rate is: %f" % (float(errCount)/m)
    dataArr, labelArr = loadDataSet('testSetRBF2.txt')
    errCount = 0
    dataMat = mat(dataArr); labelMat = mat(labelArr).transpose()
    m, n = shape(dataMat)
    for i in range(m):
        kernalEval = kernalTrans(sVs, dataMat[i, :], ('rbf', k1))
        predict = kernalEval.T * multiply(labelSV, alphas[svInd] + b)
        if sign(predict) != sign(labelArr[i]): errCount += 1
    print "the training error rate is: %f" % (float(errCount)/m)

# testRbf()

dataArr, labelArr = loadDataSet('testSet.txt')
b, alphas = smoP(dataArr, labelArr, 0.6, 0.001, 40)
print b, alphas
w = calcWs(alphas, dataArr, labelArr)
print w
# print dataArr*mat(w) + b
# plotBestFit(dataArr, labelArr, alphas, b)