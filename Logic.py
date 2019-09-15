import copy
f = open("BoardData.txt", "r")
initBoard = ""

for i in range(9):
    newLine = f.readline()
    initBoard = initBoard + newLine.rstrip("\n")
f.close()
#print(initBoard)

board = []
possibleValues = []

globalNumTimesRun = 0
for i in range(9):
    empArray = []
    possibleValues.append([[0],[0],[0],[0],[0],[0],[0],[0],[0]])

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

                possibleValues[i][j] = possVals(i,j)

#Checks row value
def checkRow(value, col):
    for i in range(9):
        if(board[i][col] == value):
            return False
    return True
#Checks col value
def checkCol(value, row):
    for i in range(9):
        if(board[row][i] == value):
            return False
    return True

def isInCol(row, col, value):
    for i in range(9):
        if(i == row):
            continue
        elif(value == int(board[i][col])):
            return True
    return False

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
def goodRowVal(row):
    tester = "123456789"
    tempArray = [];
    badListRow = badRowVal(row)
    for i in range(len(badListRow)):
        indexOfBad = tester.find(badListRow[i])
        if(indexOfBad > 0):
            tester = tester[0:indexOfBad-1] + tester[indexOfBad:len(badListRow)]

    for i in range(len(tester)):
        tempArray.append(tester[i:i+1])


def goodColVal(col):
    tester = "123456789"
    tempArray = [];
    badListCol = badColVal(col)
    for i in range(len(badListRow)):
        indexOfBad = tester.find(badListCol[i])
        if(indexOfBad > 0):
            tester = tester[0:indexOfBad-1] + tester[indexOfBad:len(badListRow)]

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

def possVals(row,col):
    returnableArray = []
    tester = "123456789"
    arrayOfBad = badColVal(col)
    arrayOfBad.extend(badRowVal(row))
    arrayOfBad.extend(badSquareVal(row, col))
    for i in range(len(arrayOfBad)):
        indexOfBad = tester.find(arrayOfBad[i])

        if(indexOfBad >= 0): #23479

            tester = tester[0:indexOfBad] + tester[indexOfBad+1:len(arrayOfBad)]

    for i in range(len(tester)):
        returnableArray.append(tester[i:i+1])
    return returnableArray

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
                arrayOfBad = badColVal(sCol)
                arrayOfBad.extend(badRowVal(sRow))
                arrayOfBad.extend(badSquareVal(sRow, sCol))
                print(len(arrayOfBad))
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
            arrayOfBad = badColVal(col)
            arrayOfBad.extend(badRowVal(i))
            arrayOfBad.extend(badSquareVal(i, col))
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
            assign = numAppears(notToBeUsed,couldWork[i], counter) and (int(board[row][col]) == 0)
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
            arrayOfBad = badColVal(i)
            arrayOfBad.extend(badRowVal(row))
            arrayOfBad.extend(badSquareVal(row, i))
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

def printBoard(array):
    for i in range(9):
        for j in range(9):
            print(array[i][j], end = "")
        print("")
def checkZeros(gameBoard):
    for i in range(9):
        for j in range(9):
            if(int(gameBoard[i][j]) == 0):
                return True
    return False

def solveBoard():
    totalIterations = 0
    createBoard()
    attempts = 0
    counter = 0

    defineList()
    while(oneSolution()):
        totalIterations += 1
        print("Total Iterations: ")
        print(totalIterations)
        defineList()
        printBoard(board)
        print("")

        attempts += 1

    tempBoard = copy.deepcopy(board)
    tempBoard[0][0] = "a"
    anotherCount = 0
    printBoard(tempBoard)
    while(not(isSameBoard(tempBoard))):
        totalIterations += 1
        print("Total Iterations: ")
        print(totalIterations)
        anotherCount += 1
        tempBoard = copy.deepcopy(board)
        for i in range(9):
            for j in range(9):
                compareVals(i, j)
                compareValsCol(i,j)
                compareValsRow(i,j)
                printBoard(board)
    print("Another Coutner: ", end = "")
    print(anotherCount)
    defineList()
    while (oneSolution()):
        totalIterations += 1
        print("Total Iterations: ")
        print(totalIterations)
        defineList()
        printBoard(board)
        print("")
    tempBoard = copy.deepcopy(board)
    tempBoard[0][0] = "a"

    while (not(isSameBoard(tempBoard))):
        totalIterations += 1
        print("Total Iterations: ")
        print(totalIterations)
        anotherCount += 1
        tempBoard = copy.deepcopy(board)
        temp = 0
        for i in range(9):
            for j in range(9):
                temp += 1
                compareVals(i, j)
                compareValsCol(i, j)
                compareValsRow(i, j)
                printBoard(board)
                print(temp)

    return attempts

def bubbleSortTwo(array, n):
    counter = 0
    for i in range(len(array)):
        if(n == array[i]):
            counter += 1
        if(n == array[i] and counter > 1):
            return True
    return False

def numAppears(array, n, times):
    counter = 0
    for i in range(len(array)):
        if(int(n) == int(array[i])):
            counter += 1
    if(counter != times):
        return False
    return True

def isSameBoard(gameBoard):
    for i in range(9):
        for j in range(9):
            if(board[i][j] != gameBoard[i][j]):
                return False
    return True

createBoard()

#print(isInCol(0,0,3))

print(solveBoard())
printBoard(board)
print("")
printBoard(possibleValues)
