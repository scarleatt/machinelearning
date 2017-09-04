import math
from numpy import *
import operator
import copy

def loadDataset(filename):
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        del(curLine[0])
        for i in range(len(curLine)):
            if curLine[i].isdigit():
                temp = len(curLine[i])
            elif curLine[i].isalpha():
                temp = -1
            else:
                temp = curLine[i].index('.')
            if temp > -1:
                if curLine[i][0:temp].isdigit():
                    curLine[i] = float(curLine[i])
        dataMat.append(curLine)
    kinds = dataMat[0]
    del(dataMat[0]); del(kinds[-1])
    return dataMat, kinds

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

def chooseBestContinueSplit(sortCopy, index):
    m, n = shape(sortCopy)
    labelMat = [example[-1] for example in sortCopy]
    entD = ent(labelMat)
    h = 0.0
    featureIndexs = {}
    for k in range(m):
        temp = sortCopy[k][index]
        if temp not in featureIndexs:
            featureIndexs[temp] = []
        featureIndexs[temp].append(k)
    for key in featureIndexs:
        sublabel = []
        for value in featureIndexs[key]:
            sublabel.append(labelMat[value])
        h -= float(len(featureIndexs[key]))/m * ent(sublabel)
    return entD+h

def continueNum(dataMat, index):
    m, n = shape(dataMat)
    candidates = []
    resData = []
    maxEnt = 0
    sortdata = sorted(dataMat, key=operator.itemgetter(index))
    for i in range(m-1):
        temp = float(sortdata[i][index]) + float(sortdata[i+1][index])
        candidates.append(temp/2)
    sortCopy = copy.deepcopy(sortdata)
    for i in range(len(candidates)):
        for j in range(m):
            if float(sortdata[j][index]) < float(candidates[i]):
                sortCopy[j][index] = 0
            else:
                sortCopy[j][index] = 1
        d = chooseBestContinueSplit(sortCopy, index)
        if d > maxEnt:
            maxEnt = d
            resData = copy.deepcopy(sortCopy)
        sortCopy = copy.deepcopy(sortdata)
    return resData

def chooseBestFeature(dataMat):
    m, n = shape(dataMat)
    labelMat = [example[-1] for example in dataMat]
    entD = ent(labelMat)
    maxIndex = 0
    bestsplit = 0
    features = {}
    for i in range(n-1):
        h = 0.0
        featureIndexs = {}
        for k in range(m):
            temp = dataMat[k][i]
            if temp not in featureIndexs:
                featureIndexs[temp] = []
            featureIndexs[temp].append(k)
        for key in featureIndexs:
            sublabel = []
            for value in featureIndexs[key]:
                sublabel.append(labelMat[value])
            h -= float(len(featureIndexs[key]))/m * ent(sublabel)
        if entD+h > bestsplit:
            bestsplit = entD+h
            maxIndex = i
            features = featureIndexs.copy()
    return bestsplit, maxIndex, features

def listExtract(dataMat, list):
    temp = []
    m, n = shape(dataMat)
    for i in range(m):
        if i in list:
            temp.append(dataMat[i])
    return temp

def trees(dataMat, classList):
    labelMat = [example[-1] for example in dataMat]
    if labelMat.count(labelMat[0]) == len(labelMat):
        print dataMat
        return labelMat[0]
    if shape(dataMat[0])[0] == 1:
        labelCounts = {}
        for vote in labelMat:
            if vote not in labelCounts:
                labelCounts[vote] = 0
            labelCounts[vote] += 1
        sortedClassCount = sorted(labelCounts.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sortedClassCount[0][0]
    bestsplit, maxIndex, featuresIndex = chooseBestFeature(dataMat)
    nowkind = copy.deepcopy(classList[maxIndex])
    mytree = {nowkind: {}}
    del(classList[maxIndex])
    for key in featuresIndex:
        sublabel = []
        temp = listExtract(dataMat, featuresIndex[key])
        subdata = delete(temp, maxIndex, axis=1)
        for i in featuresIndex[key]:
            sublabel.append(labelMat[i])
        mytree[nowkind][key] = trees(subdata, classList)
    return mytree

def giniChooseBest(dataMat):
    m, n = shape(dataMat)
    labelMat = [example[-1] for example in dataMat]
    maxIndex = 0
    bestsplit = Inf
    features = {}
    for i in range(n-1):
        bestsplit = Inf
        print "----------------"
        featureIndexs = {}
        for k in range(m):
            temp = dataMat[k][i]
            if temp not in featureIndexs:
                featureIndexs[temp] = []
            featureIndexs[temp].append(k)
        print featureIndexs
        allkeys = featureIndexs.keys()



        for key in featureIndexs:
            sublabelCount = {}
            for value in featureIndexs[key]:
                curlable = labelMat[value]
                if curlable not in sublabelCount:
                    sublabelCount[curlable] = 0
                sublabelCount[curlable] += 1



            templabelcount = 0
            for j in sublabelCount:
                if sublabelCount[j] > templabelcount:
                    templabelcount = sublabelCount[j]
            templen = float(len(featureIndexs[key]))
            gini = templen/m* 2* templabelcount/templen * (templen-templabelcount)/templen +\
                   (m-templen)/m*2*templabelcount/(m-templen)*(templen-templabelcount)/(m-templen)
            if bestsplit >  gini:
                bestsplit = gini

            print gini
        print bestsplit



    return bestsplit, maxIndex, features

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs


dataMat, kinds = loadDataset('watermelon3_0_En.csv')
dataMat = continueNum(dataMat, -3)
dataMat = continueNum(dataMat, -2)

myTree = trees(dataMat, kinds)
print myTree
print getNumLeafs(myTree)