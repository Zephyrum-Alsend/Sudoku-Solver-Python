#Author: Lucas Crockett
#Sudoku Solver
#Last Edited: 21/07/18

from array import *

#Replace this with a file reader function
SudokuPuzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]

#Prints a table to console.
#Returns True when successful; returns False if an exception arose.
#Converts entire table to a string before printing, incase the error arises halfway and we don't have half a table printed then ERROR.
def printTable(table):
    try:
        strTable = ''
        for row in table:
            for x in row:
                strTable += str(x) + ' '
            strTable += '\n'        
        print(strTable, end='')
        return(True)
    except:
        print('Parameter passed wasn\'t a table!')
        return(False)


##########MAIN##########
printTable(SudokuPuzzle)
#printTable(5)