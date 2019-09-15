import LogicFunction
import time

t0 = time.time()

LogicFunction

possibleValues = []

def initPossVals():
    for i in range(9):
        possibleValues.append([[0], [0], [0], [0], [0], [0], [0], [0], [0]])
    print(possibleValues)
    f = open("PossValsRaw.txt", "r")
    for i in range(9):
        for j in range(9):
            newLine = f.readline()
            newLine = newLine.rstrip("\n")
            if(newLine == ""):
                possibleValues[i][j] = []
            elif (int(newLine) == 0):
                continue
            else:
                print(newLine)
                for k in range(len(newLine)):
                    possibleValues[i][j].extend(newLine[k])
                del possibleValues[i][j][0]

def checkPossVals():
    for i in range(9):
        for j in range(9):
            if(len(possibleValues[i][j]) == 0):
                return False
    return True

def checkAmountOfNonZeros():
    count = 0
    for i in range(9):
        for j in range(9):
            if(len(possibleValues[i][j]) > 1):
                count += 1
    return count

def subbingConditions():
    bool1 = checkAmountOfNonZeros() > 25
    bool2 = checkPossVals()

    totalBool = bool2 and bool1
    return totalBool

def checkIfGoodValue(list):
    if(list[0] and list [1]):
        return (False, -1)
    elif(not(list[0] and list[1])):
        tempVar = False
        if(list[0]):
            tempVar = 0
        else:
            tempVar = 1
        return (True, tempVar)







def writeToCopy():
    f = open("BoardData.txt", "r")
    m = open("CopiedBoard.txt", "w")
    for i in range(9):
        m.write(f.readline())


def writeToBoard(i, j, val):
    f = open("CopiedBoard.txt", "r")
    m = open("BoardData.txt", "w")

    for k in range(9):
        if(i == k):
            modline = f.readline()
            modline = modline[0:j] + str(val) + modline[j+1:]
            m.write(modline)
        else:
            modLine = f.readline()
            m.write(modLine)

"""def searchForTwo():
    for i in range(9):
        for j in range(9):
            tempList = []
            if(len(possibleValues[i][j]) == 2):
                print(i, end = " ")
                print(",", end = " ")
                print(j)
                subValue = possibleValues[i][j][0]
                writeToCopy()
                writeToBoard(i, j, subValue)
                LogicFunction
                tempList.append(subbingConditions())
                subValue = possibleValues[i][j][1]
                writeToCopy()
                writeToBoard(i, j, subValue)
                LogicFunction
                tempList.append(subbingConditions())
                myTuple = checkIfGoodValue(tempList)
                if(myTuple[0] == True):
                    writeToBoard(i, j, possibleValues[i][j][myTuple[1]])
                else:
                    writeToBoard(i, j, 0)"""

def testing():
    tempList = []
    subValue = possibleValues[0][2][0]
    writeToCopy()
    writeToBoard(0, 2, subValue)
    LogicFunction
    tempList.append(subbingConditions())
    subValue = 0
    writeToCopy()
    writeToBoard(0, 2, subValue)
    LogicFunction
    subValue = possibleValues[0][2][1]
    writeToCopy()
    writeToBoard(0, 2, subValue)
    LogicFunction
    tempList.append(subbingConditions())
    print(tempList)




def printBoard(array):
    for i in range(9):
        for j in range(9):
            print(array[i][j], end = "")
        print("")


initPossVals()
print("hello")
#searchForTwo()
#testing()
printBoard(possibleValues)
t1 = time.time()
print(t1-t0)

