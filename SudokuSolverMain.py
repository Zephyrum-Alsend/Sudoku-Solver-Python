#Author: Zephyrum Alsend
#Sudoku Solver
#Last Edited: 21/07/18

from array import *
import copy

#Replace this with a file reader function
SudokuPuzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 3, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 3, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 5, 3, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]

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


def solveSudoku(puzzle, size, subsize):
    x = 0
    y = 0
    solve = copy.deepcopy(puzzle)
    num = puzzle[0][0] #Seed num

    while 0 <= y < size:
        #Check if coordinate is immutable
        if puzzle[y][x] == 0:
            num = getValidNum(solve[y][x], getInvalidNum(x, y, solve, subsize), size)    
            solve[y][x] = num
        #By carrying over num from the previous loop and not modifying it, we continue in the previous direction.
            
        #If no number is invalid, decrement coordinates
        if num == 0:
            x -= 1
            if x < 0:
                x = size + x
                y -= 1
            
        #If a number is valid, increment coordinates
        else:
            x += 1
            if x >= size:
                x = 0
                y += 1

        #printTable(puzzle)

    if y < 0:
        print('Puzzle is impossible!')
        return(False)

    return(solve)


#Returns the list of numbers which cannot go in (x, y).
def getInvalidNum(x, y, puzzle, subsize):
    invalid = [0]

    #Get the row
    for i in puzzle[y]:
        if i not in invalid:
            invalid.append(i)

    #Get the column
    for i in puzzle:
        if i[x] not in invalid:
            invalid.append(i[x])

    #Get the box
    Bx = (x//subsize) * subsize
    By = (y//subsize) * subsize

    for i in range(By, By + subsize):
        for j in range(Bx, Bx + subsize):
            if puzzle[i][j] not in invalid:
                invalid.append(puzzle[i][j])

    return(invalid)


#Returns a valid value, given the current value (floor), maximum size and a list of invalid values.
#Returns 0 if no valid value was found.
#Starts at floor + 1; if solveSudoku backtracked to floor, that means floor doesn't work.
def getValidNum(floor, invalid, size):
    num = floor + 1
    while num in invalid and num <= size:
        num += 1
    if num <= size:
        return(num)
    else:
        return(0)


##########MAIN##########
printTable(SudokuPuzzle)
#printTable(5) #Should throw an error
printTable(solveSudoku(SudokuPuzzle, 9, 3))