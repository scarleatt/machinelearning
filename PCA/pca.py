from numpy import *

def loadDatSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    dataArr = [map(float, line) for line in stringArr]
    return mat(dataArr)

def pca(dataMat, topNfeat=9999999):
    meansVals = mean(dataMat, axis=0)
    meanRemoved = dataMat - meansVals
    covMat = cov(meanRemoved, rowvar=0)
    eigVals, eigVects = linalg.eig(mat(covMat))
    print eigVals
    eigValInd = argsort(eigVals)
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    redEigVects = eigVects[:, eigValInd]
    lowDDataMat = meanRemoved * redEigVects
    reconMat = (lowDDataMat * redEigVects.T) + meansVals
    return lowDDataMat, reconMat

def replaceNanWithMean():
    dataMat = loadDatSet('secom.data', ' ')
    numFeat = shape(dataMat)[1]
    for i in range(numFeat):
        meanVal = mean(dataMat[nonzero(~isnan(dataMat[:,i].A))[0], i])
        dataMat[nonzero(isnan(dataMat[:,i].A))[0], i] = meanVal
    return dataMat

# dataMat = loadDatSet('testSet.txt')
# lowDMat, reconMat = pca(dataMat, 1)

# import matplotlib
# import matplotlib.pyplot as plt
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(dataMat[:, 0].flatten().A[0], dataMat[:, 1].flatten().A[0], marker='^', s=90)
# ax.scatter(reconMat[:, 0].flatten().A[0], reconMat[:, 1].flatten().A[0], marker='o', s=50, c='red')
# plt.show()
