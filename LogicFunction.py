import copy
import time
#Global Variables
initBoard = "" #The 81 character long string of all the board elements
board = [] #2D List of the gameboard
possibleValues = [] #2D List of array of all possible values that fit into that index
doubleValCounter = 0
previousRow = -1
previousCol = -1

#Converts the inputed data from the text file into a string
#def createInit():
t0 = time.time()
f = open("BoardData.txt", "r")
for i in range(9):
    newLine = f.readline()
    initBoard = initBoard + newLine.rstrip("\n")
f.close()
#Initializes the possible values 2D array
def createPossBoard():
    for i in range(9):
        empArray = []
        possibleValues.append([[0], [0], [0], [0], [0], [0], [0], [0], [0]])

#createInit()
createPossBoard()

#Creates the 2D array for the board
def createBoard():
    temp = 0
    for i in range(0,9):
        empArray = []
        board.append(empArray)
        for j in range (0,9):
            board[i].append(initBoard[temp])
            temp = temp + 1

#Creates list of possible values that can be stored in each open cell
def defineList():
    for i in range(9):
        for j in range(9):
            if(int(board[i][j]) == 0):
                possibleValues[i][j] = possVals(i, j)

#Checks if a given value is found in the same column as the given point
def isInCol(row, col, value):
    for i in range(9):
        if(i == row):
            continue
        elif(value == int(board[i][col])):
            return True
    return False

#Checks if a given value is found in the same row as the given point
def isInRow(row, col, value):
    for i in range(9):
        if (i == col):
            continue
        elif (value == int(board[row][i])):
            return True
    return False

#Defines Bad Row Values
def badRowVal(row):
    array = []
    for i in range(9):
        temp = board[row][i]
        if(temp != 0):
            st = temp + ""
            array.append(st)
    return array

#Defines Bad Col Values
def badColVal(col):
    array = []
    for i in range(9):
        temp = board[i][col]
        if(temp != 0):
            array.append(temp)
    return array

#Defines Bad Square Values
def badSquareVal(row,col):
    count = 0;
    badSquareArray = []
    sRow = row - row % 3
    sCol = col - col % 3
    rowLimit = sRow + 3
    colLimit = sCol + 3
    while(sRow < (rowLimit)):
        while(sCol < (colLimit)):
            if(int(board[sRow][sCol]) > 0):
                badSquareArray.append(board[sRow][sCol])
            sCol = sCol + 1
        sRow = sRow + 1
        count += 1
        if(sCol == colLimit and count < 3):
            sCol = col - col % 3
    return badSquareArray

#Returns all the bad values at a given coordinate
def allBadVals(row, col):
    arrayOfBad = badColVal(col)
    arrayOfBad.extend(badRowVal(row))
    arrayOfBad.extend(badSquareVal(row, col))
    return arrayOfBad

#Returns all possible values that fit in a given coordinate
def possVals(row,col):
    returnableArray = []
    tester = "123456789"
    arrayOfBad = allBadVals(row, col)
    for i in range(len(arrayOfBad)):
        indexOfBad = tester.find(arrayOfBad[i])
        if(indexOfBad >= 0): #23479
            tester = tester[0:indexOfBad] + tester[indexOfBad+1:len(arrayOfBad)]
    for i in range(len(tester)):
        returnableArray.append(tester[i:i+1])
    return returnableArray

#Plugs in value of a single length array in the possible values board
def oneSolution():
    wasAltered = False
    for i in range(9):
        for j in range(9):
            if(len(possibleValues[i][j]) == 1 and int(possibleValues[i][j][0]) > 0):
                board[i][j] = possibleValues[i][j][0]
                possibleValues[i][j][0] = 0
                wasAltered = True
    return wasAltered

def bannedValues(row,col):
    couldWork = possVals(row, col)
    tempArray = [0];
    count = 0
    sRow = row - row % 3
    sCol = col - col % 3
    rowLimit = sRow + 3
    colLimit = sCol + 3
    numTimesRun = 0
    while(sRow < (rowLimit)):
        while(sCol < (colLimit)):
            arrayToBeAdded = []
            if ((sRow == row and sCol == col) or int(board[sRow][sCol]) > 0):
                sCol += 1
                continue
            else:
                numTimesRun += 1
                print(sRow, end = " ")
                print(",", end = " ")
                print(sCol)
                arrayOfBad = allBadVals(row, col)
                for e in range(len(arrayOfBad)):
                    if(int(arrayOfBad[e])>0):
                        arrayToBeAdded.append(int(arrayOfBad[e]))
                loopCont = len(arrayToBeAdded) -1
                while(loopCont > 0):
                    if(bubbleSortTwo(arrayToBeAdded, int(arrayToBeAdded[loopCont]))):
                        del arrayToBeAdded[loopCont]
                    loopCont -= 1
                tempArray.extend(arrayToBeAdded)
            sCol = sCol + 1
        sRow = sRow + 1
        count += 1
        if(sCol == colLimit and count < 3):
            sCol = col -col % 3
    del tempArray[0]
    tempArray.sort()
    myTuple = (tempArray, numTimesRun)
    return myTuple

def compareVals(row, col):
    couldWork = possVals(row, col)
    notToBeUsedTuple = bannedValues(row, col)
    notToBeUsed = notToBeUsedTuple[0]
    counter = notToBeUsedTuple[1]
    print("")
    for i in range(len(couldWork)):
            assign = numAppears(notToBeUsed,couldWork[i], counter) and (int(board[row][col]) == 0)
            if(numAppears(notToBeUsed,couldWork[i], counter) and (int(board[row][col]) == 0)):

                board[row][col] = couldWork[i]
                possibleValues[row][col] = [0]

def bannedValuesCol(row, col):
    tempArray = [0]
    numTimesRun = 0
    for i in range(9):
        arrayToBeAdded = []
        if(row == i or int(board[i][col]) > 0):
            continue
        else:
            numTimesRun += 1
            arrayOfBad = allBadVals(i, col)
            for e in range(len(arrayOfBad)):
                if(int(arrayOfBad[e])>0 and (not(isInCol(i, col, int(arrayOfBad[e]))))):
                    arrayToBeAdded.append(int(arrayOfBad[e]))
            loopCont = len(arrayToBeAdded) - 1
            while(loopCont > 0):
                if(bubbleSortTwo(arrayToBeAdded, int(arrayToBeAdded[loopCont]))):
                    del arrayToBeAdded[loopCont]
                loopCont -= 1
            tempArray.extend(arrayToBeAdded)
    del tempArray[0]
    tempArray.sort()
    myTuple = (tempArray, numTimesRun)
    return myTuple

def compareValsCol(row, col):
    couldWork = possVals(row, col)
    notToBeUsedTuple = bannedValuesCol(row, col)
    notToBeUsed = notToBeUsedTuple[0]
    counter = notToBeUsedTuple[1]
    print("")
    for i in range(len(couldWork)):
            if(numAppears(notToBeUsed,couldWork[i], counter) and (int(board[row][col]) == 0)):
                board[row][col] = couldWork[i]
                possibleValues[row][col] = [0]

def bannedValuesRow(row, col):
    tempArray = [0]
    numTimesRun = 0
    for i in range(9):
        arrayToBeAdded = []
        if(col == i or int(board[row][i]) > 0):
            continue
        else:
            numTimesRun += 1
            arrayOfBad = allBadVals(row, i)
            for e in range(len(arrayOfBad)):
                if(int(arrayOfBad[e])>0 and (not(isInRow(row, i, int(arrayOfBad[e]))))):
                    arrayToBeAdded.append(int(arrayOfBad[e]))
            loopCont = len(arrayToBeAdded) - 1
            while(loopCont > 0):
                if(bubbleSortTwo(arrayToBeAdded, int(arrayToBeAdded[loopCont]))):
                    del arrayToBeAdded[loopCont]
                loopCont -= 1
            tempArray.extend(arrayToBeAdded)
    del tempArray[0]
    tempArray.sort()
    myTuple = (tempArray, numTimesRun)
    return myTuple

def compareValsRow(row, col):
    couldWork = possVals(row, col)
    notToBeUsedTuple = bannedValuesRow(row, col)
    notToBeUsed = notToBeUsedTuple[0]
    counter = notToBeUsedTuple[1]
    print("")
    for i in range(len(couldWork)):
            assign = numAppears(notToBeUsed,couldWork[i], counter) and (int(board[row][col]) == 0)
            if(numAppears(notToBeUsed,couldWork[i], counter) and (int(board[row][col]) == 0)):
                board[row][col] = couldWork[i]
                possibleValues[row][col] = [0]

#Prints the Given Board
def printBoard(array):
    for i in range(9):
        for j in range(9):
            print(array[i][j], end = "")
        print("")

def writeToFileBoard():
    f = open("SolvedBoard.txt", "w")
    for i in range(9):
        tempString = ""
        for j in range(9):
            tempString += board[i][j]
        tempString += "\n"
        f.write(tempString)
    f.close()

def writeToFilePossVals():
    f = open("PossibleVals.txt", "w")
    for i in range(9):
        tempString = ""
        for j in range(9):
            tempString += str(possibleValues[i][j])
        tempString += "\n"
        f.write(tempString)
    f.close()

def writeToFilePossValsRaw():
    f = open("PossValsRaw.txt", "w")
    for i in range(9):
        for j in range(9):
            tempString = ""
            for k in range(len(possibleValues[i][j])):
                tempString += str(possibleValues[i][j][k])
            tempString += "\n"
            f.write(tempString)
    f.close()

def findingOneSolution():
    defineList()
    while (oneSolution()):
        defineList()
        printBoard(board)
        print("")

def compareSolutions():
    tempBoard = copy.deepcopy(board)
    tempBoard[0][0] = "a"
    printBoard(tempBoard)
    while (not(isSameBoard(tempBoard))):
        tempBoard = copy.deepcopy(board)
        for i in range(9):
            for j in range(9):
                compareVals(i, j)
                compareValsCol(i, j)
                compareValsRow(i, j)
                printBoard(board)

def solution():
    createPossBoard()
    createBoard()
    findingOneSolution()
    compareSolutions()
    findingOneSolution()
    compareSolutions()

def resolution():
    findingOneSolution()
    compareSolutions()
    findingOneSolution()
    compareSolutions()
#Checks if a given values appears more at least twice in a given array
def bubbleSortTwo(array, n):
    counter = 0
    for i in range(len(array)):
        if(n == array[i]):
            counter += 1
        if(n == array[i] and counter > 1):
            return True
    return False

#Checks if a value is in an array a target number of times
def numAppears(array, n, times):
    counter = 0
    for i in range(len(array)):
        if(int(n) == int(array[i])):
            counter += 1
    if(counter != times):
        return False
    return True

#Checks if the inputed board is same as global gameboard
def isSameBoard(gameBoard):
    for i in range(9):
        for j in range(9):
            if(board[i][j] != gameBoard[i][j]):
                return False
    return True

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
    bool1 = checkAmountOfNonZeros() > 23
    bool2 = checkPossVals()

    totalBool = bool2 and bool1
    return totalBool

def subbingTwo():
    for i in range(9):
        for j in range(9):
            arrayOfWorks = []
            count = 0
            if(len(possibleValues[i][j]) == 2):
                board[i][j] = possibleValues[i][j][count]
                count = 1
                resolution()
                if(not(subbingConditions())):
                    board[i][j] = possibleValues[i][j][count]
                    count = 0
                    resolution()
                    if(not(subbingConditions())):
                        board[i][j] = "0"
                    else:
                        count = 1
                        arrayOfWorks.append(possibleValues[i][j][count])
                else:
                    arrayOfWorks.append(possibleValues[i][j][0])
                    board[i][j] = possibleValues[i][j][count]
                    count = 0
                    resolution()
                    if(not(subbingConditions())):
                        temp = 0
                    else:
                        board[i][j] = "0"
                        arrayOfWorks.append(possibleValues[i][j][1])
                if(len(arrayOfWorks) == 1):
                    board[i][j] = arrayOfWorks[0]
                elif(len(arrayOfWorks)==2 or len(arrayOfWorks)==0):
                    board[i][j] = "0"
                defineList()

def filterPoss():
    for i in range(9):
        for j in range(9):
            tempVal = board[i][j]
            if(len(possibleValues[i][j])>0):
                loopCont = len(possibleValues[i][j]) - 1
                while(loopCont > 0):

                    print(loopCont)
                    board[i][j] = possibleValues[i][j][loopCont]
                    solution()
                    if(not(subbingConditions())):
                        possibleValues[i][j].pop(loopCont)
                        board[i][j] = "0"
                    loopCont -= 1
            board[i][j] = tempVal

def filterPossVals():

    for i in range(9):
        for j in range(9):
            if(len(possibleValues[i][j]) > 1):
                arrayOfBad = []
                lenArray = len(possibleValues[i][j])
                for k in range(lenArray):
                    board[i][j] = possibleValues[i][j][k]
                    solution()
                    if(not(subbingConditions())):
                        arrayOfBad.extend(possibleValues[i][j][k])
                for l in range(len(arrayOfBad)):
                    index = possibleValues[i][j].index(arrayOfBad[l])
                    del possibleValues[i][j][index]
                board[i][j] = "0"

def filterBads():
    for i in range(9):
        for j in range(9):
            if(len(possibleValues[i][j])== 2 and int(board[i][j]) == 0):
                arrayOfBools = []
                board[i][j] = possibleValues[i][j][0]
                resolution()
                if(subbingConditions()):
                    arrayOfBools.append(True)
                else:
                    arrayOfBools.append(False)
                board[i][j] = possibleValues[i][j][1]
                resolution()
                if (subbingConditions()):
                    arrayOfBools.append(True)
                else:
                    arrayOfBools.append(False)
                board[i][j] = "0"
                resolution()

                print(arrayOfBools)

createBoard()
printBoard(board)
solution()


#subbingTwo()
t1 = time.time()
totalTime = t1-t0
print(totalTime)

printBoard(possibleValues)
print("")
"""filterBads()
resolution()"""
writeToFileBoard()
writeToFilePossVals()
writeToFilePossValsRaw()
print(checkAmountOfNonZeros())
print(checkPossVals())
print(subbingConditions())
print(t0)