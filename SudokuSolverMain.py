#Author: Zephyrum Alsend
#Sudoku Solver
#Last Edited: 21/07/22

import copy
from pathlib import Path
from collections import Counter

class Sudoku:
    
    def __init__(self, puzzle):
        self.__puzzle = puzzle
        self.__solved = copy.deepcopy(puzzle)
        self.__size = 0
        self.__subsize = 0
        self.__mutable = 0

        #Ensure the board passed is 1.) usable data 2.) not breaking any rules
        try:
            self.__size = len(self.__puzzle)
            self.__subsize = self.__size**0.5

            if (self.__subsize).is_integer():
                self.__subsize = int(self.__subsize)
            else:
                raise Exception("Column length is not the square of a whole number.")
            
            for row in self.__puzzle:
                if len(row) != self.__size:
                    raise Exception("Row length does not match column length.")
                
                for val in row:
                    if isinstance(val, int):
                        if not ( 0 <= val <= self.__size ):
                            raise Exception("Integer value out of bounds.")
                    else:
                        raise Exception("Non-integer data found.")
        except Exception as e:
            print("The board provided is invalid. Please double-check the data.")
            print(repr(e))
            return

        Illegal = self.isLegal()
        if len(Illegal) > 0:
            for e in Illegal:
                print(e)
            return

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

    #Checks all immutable values obey the rules of Sudoku.
    #Returns a list of messages dictating where illegal numbers are.
    #Returns an empty list if everything is legal.
    def isLegal(self):
        Illegal = []

        Columns = [[]]
        for y in range(0, self.__size):
            #Get a list of all !0 values in this row
            temp = [n for n in self.__puzzle[y] if n != 0]
            if len(set(temp)) != len(temp):
                Illegal.append("Illegal placement in row " + str(y+1) + ".")

        for x in range(0, self.__size):
            #Get a list of all !0 values in this column
            temp = []
            for y in self.__puzzle:
                if y[x] != 0:
                    temp.append(y[x])
            if len(set(temp)) != len(temp):
                Illegal.append("Illegal placement in column " + str(x+1) + ".")

        #Get the boxes
        for y in range(0, self.__subsize):
            for x in range(0, self.__subsize):
                temp = []

                Bx = x * self.__subsize
                By = y * self.__subsize

                for i in range(By, By + self.__subsize):
                    for j in range(Bx, Bx + self.__subsize):
                        if self.__puzzle[i][j] != 0:
                            temp.append(self.__puzzle[i][j])

                if len(set(temp)) != len(temp):
                    Illegal.append("Illegal placement in box " + str(y * self.__subsize + x + 1) + ".")

        return(Illegal)
        
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
#Will return an empty list if an error occured.
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

            except Exception as e:
                print("File " + str(name) + " is not formatted correctly.")
                print(repr(e))
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
                return([])

            #Append each converted table
            Puzzles.append(temp)

        f.close()

    return(Puzzles)

def checkFile(puzzle):
    #Ensure the board passed is 1.) usable data 2.) not breaking any rules
    try:
        size = len(puzzle)
        subsize = size**0.5

        if (subsize).is_integer():
            subsize = int(subsize)
        else:
            raise Exception("Column length is not the square of a whole number.")
            
        for row in puzzle:
            if len(row) != size:
                raise Exception("Row length does not match column length.")
                
            for val in row:
                if isinstance(val, int):
                    if not ( 0 <= val <= size ):
                        raise Exception("Integer value out of bounds.")
                else:
                    raise Exception("Non-integer data found.")

    except Exception as e:
        print("The board provided is invalid. Please double-check the data.")
        print(repr(e))
        return

    Illegal = isLegal(puzzle)
    if len(Illegal) > 0:
        for e in Illegal:
            print(e)
        return


##########MAIN##########

PuzzlePath = "Puzzles/"
P = readSudokuPuzzles(PuzzlePath)
for X in P:
    S = Sudoku(X)
    printTable(S.getPuzzle())
    printTable(S.getSolution())
    print(S.getMutable())
    print()