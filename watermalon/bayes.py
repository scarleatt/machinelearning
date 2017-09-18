# -*- coding: utf-8 -*-
from numpy import *
import copy

def loadDataSet(filename):
    dataSet = []; dataContinue = []; dataDiscrete = []; labelSet = []
    fr = open(filename)
    for line in fr.readlines():
        curline = line.strip().split(',')
        dataSet.append(curline[1:-1])
        labelSet.append(curline[-1])
    kinds = dataSet[0]
    del(dataSet[0]); del(labelSet[0])
    for curline in dataSet:
        continueIndex = []
        discreteIndex = []
        index = 0
        for i in range(len(curline)):
            if curline[i].replace('.', '').isdigit():
                continueIndex.append(index)
                curline[i] = float(curline[i])
            else:
                discreteIndex.append(index)
            index += 1
        ctemp = []
        dtemp = []
        for index in discreteIndex:
            dtemp.append(curline[index])
        for index in continueIndex:
            ctemp.append(curline[index])
        dataContinue.append(ctemp)
        dataDiscrete.append(dtemp)
    return dataContinue, dataDiscrete, labelSet, kinds

# 连续值
def pcontinue(dataContinue, labelSet, kinds):
    data = copy.deepcopy(dataContinue)
    dataMat = mat(data)
    m, n = shape(dataContinue)
    for i in range(n):
        avg = sum(dataMat[:, i])/len(dataMat[:, i])
        



# 离散值
def bayes(dataDiscrete, labelSet, kinds):
    labelCounts = {}
    labelIndex = {}
    index = 0
    for vote in labelSet:
        if vote not in labelCounts:
            labelCounts[vote] = 0
            labelIndex[vote] = []
        labelCounts[vote] += 1
        labelIndex[vote].append(index)
        index += 1
    p = {}
    m, n = shape(dataDiscrete)
    for label in labelCounts:
        p[label] = {}
        group = labelIndex[label]
        for j in range(n):
            nowkind = kinds[j]
            p[label][nowkind] = {}
            for i in group:
                vote = dataDiscrete[i][j]
                if vote not in p[label][nowkind]:
                    p[label][nowkind][vote] = 0
                p[label][nowkind][vote] += 1
    print p

dataContinue, dataDiscrete, labelSet, kinds = loadDataSet('./data/watermalon_3.txt')

# bayes(dataDiscrete, labelSet, kinds)
pcontinue(dataContinue, labelSet, kinds)