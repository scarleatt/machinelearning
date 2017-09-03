import math
from numpy import *

def loadDataset(filename):
    dataMat = []; labelMat = []
    fr = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        del(curLine[0])
        labelMat.append(curLine[-1])
        dataMat.append(curLine[0:-4])
    del(dataMat[0]); del(labelMat[0])
    return dataMat,labelMat

def ent(labelMat):
    n = len(labelMat)
    labelsCount = {}
    h = 0.0
    for i in range(n):
        if labelMat[i] not in labelsCount:
            labelsCount[labelMat[i]] = 0
        labelsCount[labelMat[i]] += 1
    for ck in labelsCount:
        p = float(labelsCount[ck])/n
        h -= p * math.log(p, 2)
    return h

def chooseBestFeature(dataMat, labelMat):
    m, n = shape(dataMat)
    entD = ent(labelMat)
    maxIndex = 0
    bestsplit = 0
    features = {}
    for i in range(n):
        h = 0.0
        featureIndexs = {}
        for k in range(m):
            temp = dataMat[k,i]
            if temp not in featureIndexs:
                featureIndexs[temp] = []
            featureIndexs[temp].append(k)
        for key in featureIndexs:
            sublabel = []
            for value in featureIndexs[key]:
                sublabel.append(labelMat[value])
            h -= float(len(featureIndexs[key]))/m * ent(sublabel)
        # print entD+h
        if entD+h > bestsplit:
            bestsplit = entD+h
            maxIndex = i
            features = featureIndexs.copy()
    return bestsplit, maxIndex, features

def trees(dataMat, labelMat):
    # if labelMat.count(labelMat[0]) == len(labelMat):
    #     return labelMat[0]
    # if len(dataMat[0]) == 1:
    #     return labelMat[0]
    bestsplit, maxIndex, featuresIndex = chooseBestFeature(dataMat, labelMat)
    sublabel = []
    mytree = {kinds[maxIndex]:{}}
    print "___________________________________________________"
    print featuresIndex
    for key in featuresIndex:
        temp = dataMat[featuresIndex[key]]
        subdata = delete(temp, maxIndex, axis=1)
        for i in featuresIndex[key]:
            sublabel.append(labelMat[i])
        mytree[kinds[maxIndex]][key] = trees(subdata, sublabel)
        print mytree
    return mytree

dataMat, labelMat = loadDataset('watermelon3_0_En.csv')
kinds = ['Color','Root','Knocks','Texture','Umbilicus','Touch']
# print ent(labelMat)
# print chooseBestFeature(dataMat, labelMat)
print trees(mat(dataMat), labelMat)
# print mat(dataMat)[:,1]