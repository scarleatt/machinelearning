from numpy import *
import matplotlib.pyplot as plt

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        fltLine = map(float, curLine)
        dataMat.append(fltLine)
    return dataMat

def distEculd(vecA, vecB):
    return sqrt(sum(power(vecA-vecB, 2)))

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centorids = mat(zeros((k, n)))
    for j in range(n):
        minJ = min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        centorids[:, j] = minJ + rangeJ * random.rand(k, 1)
    return centorids

def kMeans(dataSet, k, distMeans=distEculd, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf; minIndex = -1
            for j in range(k):
                distJI = distMeans(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i, 0] != minIndex: clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist**2
        print centroids
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A==cent)[0]]
            centroids[cent, :] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment

def biKmeans(dataSet, k, distMeans=distEculd):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    centroids0 = mean(dataSet, axis=0).tolist()[0]
    centList = [centroids0]
    for j in range(m):
        clusterAssment[j, 1] = distMeans(mat(centroids0), dataSet[j, :])**2
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:, 0].A==i)[0], :]
            centroidMat, splitClusAss = kMeans(ptsInCurrCluster, 2, distMeans)
            sseSplit = sum(splitClusAss[:, 1])
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A!=i)[0], 1])
            print "sshSplit, and notSplit", sseSplit, sseNotSplit
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClusAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[0, :].A==1)[0], 0] = len(centList)
        bestClustAss[nonzero(bestClustAss[0, :].A==0)[0], 0] = bestCentToSplit
        print 'the bestCentToSplit is: ', bestCentToSplit
        print 'the len of bestClusAss is: ', len(bestClustAss)
        centList[bestCentToSplit] = bestClustAss[0, :].tolist()[0]
        centList.append(bestNewCents[1, :])
        clusterAssment[nonzero(clusterAssment[:, 0].A==bestCentToSplit)[0], :] = bestClustAss
    return mat(centList), clusterAssment

def distSLC(vecA, vecB):
    a = sin(vecA[0,1]*pi/180) * sin(vecB[0,1]*pi/180)
    b = cos(vecA[0,1]*pi/180) * cos(vecB[0,1]*pi/180) * cos(pi*(vecB[0,0]-vecA[0,0])/180)
    return arccos(a+b)*6371.0

import matplotlib
import matplotlib.pyplot as plt
def clusterClubs(numClust=5):
    datList = []
    for line in open('places.txt').readlines():
        lineArr = line.split('\t')
        datList.append([float(lineArr[4]), float(lineArr[3])])
    datMat = mat(datList)
    myCentroids, clustAssing = biKmeans(datMat, numClust, distMeans=distSLC)
    fig = plt.figure()
    rect = [0.1, 0.1, 0.8, 0.8]
    scatterMarkers = ['s', 'o', '^', '8', 'p', 'd', 'v', 'h', '>', '<']
    axprops = dict(xticks=[], yticks=[])
    ax0 = fig.add_axes(rect, label='ax0', **axprops)
    imgP = plt.imread('Portland.png')
    ax0.imshow(imgP)
    ax1 = fig.add_axes(rect, label='x1', framon='False')
    for i in range(numClust):
        ptsInCurrCluster = datMat[nonzero(clustAssing[:, 0].A==i)[0], :]
        markerStyle = scatterMarkers[i % len(scatterMarkers)]
        ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0],
                    ptsInCurrCluster[:,1].flatten().A[0], marker=markerStyle, s=90)
    ax1.scatter(myCentroids[:,0].flatten().A[0],
                myCentroids[:,1].flatten().A[0], marker='+', s=300)
    plt.show()

dataSet = loadDataSet('bj_gps_1k.txt')

dataSet = mat(dataSet)
m, n = shape(dataSet)
xcord1 = [([0] * 2) for i in range(m)]; ycord1 = []
for i in range(m):
    xcord1[i][0] = dataSet[i, 4]
    xcord1[i][1] = dataSet[i, 5]
    ycord1.append(dataSet[i, 5])
print xcord1
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(xcord1, ycord1, s=30)
# plt.show()
# print dataSet
# print xcord1
biKmeans(xcord1, 2, distMeans=distEculd)