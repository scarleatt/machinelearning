import math
from numpy import *
import operator

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
    if labelMat.count(labelMat[0]) == len(labelMat):
        return labelMat[0]
    if shape(dataMat[0])[1] == 1:
        labelCounts = {}
        for vote in labelMat:
            if vote not in labelCounts:
                labelCounts[vote] = 0
            labelCounts[vote] += 1
        sortedClassCount = sorted(labelCounts.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]
    bestsplit, maxIndex, featuresIndex = chooseBestFeature(dataMat, labelMat)
    nowkind = kinds[maxIndex]
    mytree = {nowkind: {}}
    # del(kinds[maxIndex])
    for key in featuresIndex:
        sublabel = []
        temp = dataMat[featuresIndex[key]]
        subdata = delete(temp, maxIndex, axis=1)
        for i in featuresIndex[key]:
            sublabel.append(labelMat[i])
        mytree[nowkind][key] = trees(subdata, sublabel)
    return mytree

dataMat, labelMat = loadDataset('watermelon3_0_En.csv')
kinds = ['Color','Root','Knocks','Texture','Umbilicus','Touch']
print trees(mat(dataMat), labelMat)

