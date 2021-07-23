#Author: Zephyrum Alsend
#Sudoku Solver
#Last Edited: 21/07/23

import copy
from pathlib import Path

class Sudoku:
    
    #Input sanitation is handled outside the class, so assumes all is fine.
    def __init__(self, puzzle):
        self.__puzzle = puzzle
        self.__solved = copy.deepcopy(puzzle)
        self.__size = len(puzzle)
        self.__subsize = int(self.__size**0.5)
        self.__mutable = self.getMutableCount()

        #Solve the board
        if self.solveSudoku():
            print("Board solved.")
        else:
            print("The board is unsolvable.")

        return

    #Returns 2-D array of starting puzzle, 0s are blank squares.
    def getPuzzle(self):
        return self.__puzzle

    #Returns 2-D array of completed puzzle.
    def getSolution(self):
        return self.__solved

    #Returns length of a column/row.
    def getSize(self):
        return self.__size

    #Returns length of a sub-box column/row.
    def getBoxSize(self):
        return self.__subsize

    #Returns total number of squares in the puzzle.
    def getSquareCount(self):
        return self.__size**2

    #Returns total number of squares within a sub-box.
    def getBoxSquareCount(self):
        return self.__subsize**2

    #Returns total number of sub-boxes in the puzzle.
    def getBoxCount(self):
        return self.__size

    #Returns the total number of mutable squares in the puzzle.
    def getMutable(self):
        return self.__mutable

    #Solves the puzzle and stores the result in __solved.
    def solveSudoku(self):
        x = 0
        y = 0
        num = self.__puzzle[0][0] #Seed num

        while 0 <= y < self.__size:
            #Check if coordinate is immutable
            if self.__puzzle[y][x] == 0:
                num = self.getValidNum(self.__solved[y][x], self.getInvalidNum(x, y))   
                self.__solved[y][x] = num
            #By carrying over num from the previous loop and not modifying it, we continue in the previous direction.
                        
            #If no number is invalid, decrement coordinates
            if num == 0:
                x -= 1
                if x < 0:
                    x = self.__size + x
                    y -= 1
                
            #If a number is valid, increment coordinates
            else:
                x += 1
                if x >= self.__size:
                    x = 0
                    y += 1

        if y < 0:
            return(False)

        return(True)

    #Returns the list of numbers which cannot go in (x, y).
    def getInvalidNum(self, x, y):
        invalid = [0]

        #Get the row
        for i in self.__solved[y]:
            if i not in invalid:
                invalid.append(i)

        #Get the column
        for i in self.__solved:
            if i[x] not in invalid:
                invalid.append(i[x])

        #Get the box
        Bx = (x//self.__subsize) * self.__subsize
        By = (y//self.__subsize) * self.__subsize

        for i in range(By, By + self.__subsize):
            for j in range(Bx, Bx + self.__subsize):
                if self.__solved[i][j] not in invalid:
                    invalid.append(self.__solved[i][j])

        return(invalid)

    #Returns a valid value for (x, y), given the current value (floor), maximum size and a list of invalid values.
    #Returns 0 if no valid value was found.
    #Starts at floor + 1; if solveSudoku backtracked to floor, that means floor doesn't work.
    def getValidNum(self, floor, invalid):
        num = floor + 1
        while num in invalid and num <= self.__size:
            num += 1
        if num <= self.__size:
            return(num)
        else:
            return(0)

    #Returns the total number of mutable squares in the puzzle.
    def getMutableCount(self):
        cnt = 0
        for row in self.__puzzle:
            for val in row:
                if val == 0:
                    cnt += 1
        return(cnt)


#Prints a table to console.
#Returns True when successful; returns False if an exception arose.
#Converts entire table to a string before printing, incase the error arises halfway so we don't have half a table printed then ERROR.
def printTable(table):
    try:
        strTable = ''
        for row in table:
            for x in row:
                strTable += str(x) + ' '
            strTable += '\n'        
        print(strTable)
        return(True)
    except:
        print('Parameter passed wasn\'t a table!')
        return(False)

#Reads .txt files in a given folder, interpeting them as Sudoku puzzles.
#Will return a list of tables, each table being a Sudoku puzzle.
#Files which throw errors are not included, instead prompting a console log.
#Will return an empty list if the folder path throws an error.
def readSudokuPuzzles(strPath):
    try:
        Folder = Path(strPath).rglob("*.txt")
    except Exception as e:
        print(repr(e))
        return([])
    
    Files = [x for x in Folder]
    Puzzles = []
    for name in Files:
        f = open(name, "r")
        arr = []
        arr.append(f.readlines()) #each file is now a list of strings in arr
        
        for file in arr:
            #Convert each file into a 2-D array
            temp = []
            try:
                for row in file:
                    temp.append(list(map(int, row.split())))

                #Check the rules of Sudoku are followed
                estr = isIllegal(temp)
                if len(estr) > 0:
                    raise Exception("Illegal board config.")
                
                #Append each converted table
                Puzzles.append(temp)

            except Exception as e:
                print("File " + str(name) + " is not formatted correctly.")
                print(repr(e))
                for err in estr:
                    print(err)
                print("Correct format looks like:\n" +
                "1 4 5 0 0 0 0 0 0\n" +
                "9 3 6 0 0 0 0 0 0\n" +
                "8 7 2 0 0 0 0 0 0\n" +
                "0 0 0 1 4 5 0 0 0\n" +
                "0 0 0 9 3 6 0 0 0\n" +
                "0 0 0 8 7 2 0 0 0\n" +
                "2 6 7 0 0 0 1 4 5\n" +
                "4 1 8 0 0 0 9 3 6\n" +
                "5 9 3 0 0 0 8 7 2\n")

        f.close()

    return(Puzzles)

#Ensure the board passed is legal: dimensions are OK, numbers in bounds, etc.
#Returns a list of error strings. Empty list if no errors.
def isIllegal(puzzle):
    errors = []
    size = len(puzzle)
    subsize = size**0.5

    #Check board size allows for uniform sub-boxes
    if (subsize).is_integer():
        subsize = int(subsize)
    else:
        errors.append("Column length is not the square of a whole number.")
            
    #Check every row is the same length as a column
    for row in puzzle:
        if len(row) != size:
            errors.append("Row length does not match column length.")
            break #Prevents duplicates of this error message
        
    #Check for duplicate numbers in each row
    for y in range(0, size):
        #Get a list of all !0 values in this row
        temp = [n for n in puzzle[y] if n != 0]
        if len(set(temp)) != len(temp):
            errors.append("Repeat number in row " + str(y+1) + ".")

    #Check for duplicate numbers in each column
    for x in range(0, size):
        #Get a list of all !0 values in this column
        temp = []
        for y in puzzle:
            if y[x] != 0:
                temp.append(y[x])
        if len(set(temp)) != len(temp):
            errors.append("Repeat number in column " + str(x+1) + ".")

    #Check for duplicate numbers in each box
    for y in range(0, subsize):
        for x in range(0, subsize):
            temp = []

            Bx = x * subsize
            By = y * subsize
            for i in range(By, By + subsize):
                for j in range(Bx, Bx + subsize):
                    if puzzle[i][j] != 0:
                        temp.append(puzzle[i][j])

            if len(set(temp)) != len(temp):
                errors.append("Repeat number in box " + str(y * subsize + x + 1) + ".")

    #Check for out of bounds numbers
    for y in range(0, size):
        for x in range(0, size):
            if not(0 <= puzzle[y][x] <= size):
                errors.append("Out of bounds number in column " + str(x+1) + ", row " + str(y+1) + ".")

    return(errors)


##########MAIN##########

PuzzlePath = "Puzzles/"
P = readSudokuPuzzles(PuzzlePath)
for X in P:
    S = Sudoku(X)
    printTable(S.getPuzzle())
    printTable(S.getSolution())
    print(S.getMutable())
    print()