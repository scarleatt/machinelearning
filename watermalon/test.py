# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")
#
# fin = open('./data/watermalon_2.txt', 'r')
# for eachLine in fin:
#     line = eachLine.strip().decode('gbk', 'utf-8')
#     print line

def loadDataset(filename):
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        print line
    #     curLine = line.strip().split(',')
    #     del(curLine[0])
    #     for i in range(len(curLine)):
    #         if curLine[i].isdigit():
    #             temp = len(curLine[i])
    #         elif curLine[i].isalpha():
    #             temp = -1
    #         else:
    #             temp = curLine[i].index('.')
    #         if temp > -1:
    #             if curLine[i][0:temp].isdigit():
    #                 curLine[i] = float(curLine[i])
    #     dataMat.append(curLine)
    # kinds = dataMat[0]
    # del(dataMat[0]); del(kinds[-1])
    # return dataMat, kinds

print loadDataset('./data/watermalon_3_alpha.txt')