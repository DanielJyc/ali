import csv
import numpy as np
#mt = np.load('data.npy')

def convertToMatrix():
    f = open('1.csv', 'rb')
    rd = csv.reader(f)
    tMatrix = np.array(list(rd)).astype('int')
    print tMatrix.shape
    matrix = np.array(range(5)).astype('int')
    matrix.shape = (1, 5)
    for r in tMatrix:
        t = r
        t.shape = (1,4)
        t = np.append(t, [[int(str(t[0][3])[1:])]], 1)
        t[0][3] = int(str(t[0][3])[0])
        matrix = np.append(matrix, t, 0)
    matrix = matrx[np.lexsort((mt[:,1], mt[:,4], mt[:,3], mt[:,0]))]
    return matrix

def compressMatrixToAddBuyTimes(mt):
    t = mt[0]
    t = np.append(t, [0, 0], 1)
    rtMatrix = np.array(range(0)).astype('int')
    rtMatrix.shape = (0, 7)
    for r in mt:
        if (r[0] == t[0]):
            if (r[1] == t[1]):
                t[5] += 1
                if (r[2] == 0):
                    t[6] += 1
            else:
                t.shape = (1,7)
                rtMatrix = np.append(rtMatrix, t, 0) 
                t.shape = (7,)
                t[0:5] = r
                t[5] = 1 
                if (r[2] == 0):
                    t[6] = 1
                else:
                    t[6] = 0
        else:
            t.shape = (1,7)
            rtMatrix = np.append(rtMatrix, t, 0) 
            t.shape = (7,)
            t[0:5] = r
            t[5] = 1
            if (r[2] == 0):
                t[6] = 1
            else:
                t[6] = 0
    return rtMatrix





def getWithParameter(mt, userID=0, brandID=0, action=0,month=0, day=0):
    userJudge = judgeParameter(userID)
    brandJudge = judgeParameter(brandID)
    actionJudge = judgeParameter(action)
    monthJudge = judgeParameter(month)
    dayJudge = judgeParameter(day) 
    if (action == 0):
        action = (0, 1, 2, 3)
    if (month == 0):
        month = (4, 5, 6, 7, 8)
    if (day == 0):
        day = tuple(range(1,32))
    reMt = np.array(range(0)).astype('int')
    reMt.shape = (0,5)
    if (userID == 0):
        if (brandID == 0):
            for r in mt:
                if(r[2] in action and r[3] in month and r[4] in day):
                    reMt = np.append(reMt, [r], 0)
        else:
            for r in mt:
                if(r[2] in action and r[1] in brandID and r[3] in month and r[4] in day):
                    reMt = np.append(reMt, [r], 0)
    elif (brandID == 0):
        for r in mt:
            #print action, userID, month, day
            #print type(action), type(userID), type(month), type(day)
            if(r[2] in action and r[0] in userID and r[3] in month and r[4] in day):
                reMt = np.append(reMt, [r], 0)
    else:
        for r in mt:
            if (r[2] in action and r[0] in userID and r[1] in brandID and r[3] in month) and r[4] in day:
                reMt = np.append(reMt, [r], 0)
    return reMt

def judgeParameter(parameter):
    if (parameter == 0):
        return True
    else:
        return False

def generateBrandSet(mt):
    userList = list(set(mt[:,0]))
    brandList = list(set(mt[:,1]))
    brandSet = list()
    for userID in userList:
        userIDTuple = (userID,)
        print userIDTuple
        userData = getWithParameter(mt, userIDTuple, 0, 0, 0, 0) 
        monthList = list(set(userData[:,3]))
        dayList = list(set(userData[:,4]))
        for month in monthList:
            for day in dayList:
                templeBrandSet = list(set(getWithParameter(userData, userIDTuple, 0, 0, (month,), (day,))[:,1])) 
                if (templeBrandSet != [] and templeBrandSet not in brandSet):
                    brandSet.append(templeBrandSet)
                    brandSet.append([userID, month, day])
    return brandSet

def computeDiceIndex(setSample):
    diceIndexMatrix = []
    i = 0.0
    length = len(setSample)
    for s in range(0, len(setSample), 2):
        for os in range(0, len(setSample), 2):
            diceIndex = 2.0 * float(len(setSample[s].intersection(setSample[os]))) / float((len(setSample[s]) + len(setSample[os])))
            if (diceIndex > 0.5 and diceIndex != 1):
                t = [setSample[s], setSample[os]];ti = [setSample[os], setSample[s]]
                if (t not in diceIndexMatrix and ti not in diceIndexMatrix):
                    diceIndexMatrix.append(t)
                    diceIndexMatrix.append(diceIndex)
                    diceIndexMatrix.append([setSample[s+1], setSample[os+1]])
                #else:
                    #diceIndexMatrix[diceIndexMatrix.index(t) + 1] += diceIndex
                    #print diceIndexMatrix
                #print diceIndexMatrix[diceIndexMatrix.index(t)], diceIndexMatrix[diceIndexMatrix.index(t) + 1]
        i += 1
        print i / length
    return diceIndexMatrix
                        
