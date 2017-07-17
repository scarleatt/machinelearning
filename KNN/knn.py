from numpy import *;
import operator

def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    returnMat = zeros((len(arrayOLines), 3))
    classLabelvector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelvector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelvector

def classify0(inx, dataSet, labels, k):
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

# plot
# import matplotlib.pyplot as plt
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(returnMat[:, 0], returnMat[:, 1], 15.0*array(classLabelvector), 15.0*array(classLabelvector))
# plt.show()

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = (dataSet-tile(minVals, (m, 1)))/(tile(ranges, (m, 1)))
    return normDataSet, ranges, minVals

def datingClassTest():
    ratio = 0.1
    dataMat, datalabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(dataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*ratio)
    errCount = 0
    for i in range(numTestVecs):
        result = classify0(normMat[i,:], normMat[numTestVecs:m,:], datalabels[numTestVecs:m],3)
        print "The classifier came back with: %d, the real answer is %d" \
              % (result, datalabels[i])
        if (result != datalabels[i]): errCount += 1
    print "The total error rate is %f " % (errCount / float(numTestVecs))

datingClassTest()