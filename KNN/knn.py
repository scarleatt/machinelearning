from numpy import *;
import operator
def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    lables = ['A','A','B','B']
    return group,lables

def classify0(inx,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]
    diffMat = dataSet - tile(inx, (dataSetSize, 1))
    sqDiffmat = diffMat ** 2
    sqDistances = sqDiffmat.sum(axis=1)
    distance = sqDistances ** 0.5
    sortedDistIndecies = distance.argsort()
    classCount = {}
    for i in range(k):
        voteIlabes = labels[sortedDistIndecies[i]]
        classCount[voteIlabes] = classCount.get(voteIlabes, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

group, labels = createDataSet()
result = classify0([0, 0], group, labels, 3)
print result