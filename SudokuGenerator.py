#Author: Zephyrum Alsend
#Sudoku Generator
#Generates randomized Sudoku boards with a defined number of squares filled in,
#saving them to text files in the provided Path, named "Puzzle#.txt", with # being the counter in a for loop.
#Does not guarantee boards generated are solveable.
#Last Edited: 21/08/24

import random

#Creates n .txt files in Path, containing randomized Sudoku puzzles with numbers squares already filled in.
#n must be a positive integer.
#numbers must be a positive integer.
#Path must be a valid directory path.
def writeSudokuPuzzles(n, numbers, Path, size=9):
    #Create n files
    for f in range(0, n):
        puzzle = generateSudokuPuzzle(numbers, size)

        #write puzzle to a .txt file
        name = "Puzzle" + str(f) + ".txt"
        strPuzzle = ""
        for i in range(0, size):
            for j in range(0, size):
                strPuzzle += str(puzzle[i][j])
                if j != size - 1:
                    strPuzzle += " "
            if i != size - 1:
                strPuzzle += "\n"
                
        file = open(Path+name, "w")
        file.truncate()
        file.write(strPuzzle)
        file.close()

    return

def generateSudokuPuzzle(numbers, size=9):
    subsize = int(size**0.5)
    if numbers > size**2:
        numbers = int(size**2)
    
    #Create blank puzzle
    puzzle = [[0 for i in range(0, size)] for j in range(0, size)]
        
    #With numbers squares filled in
    for squares in range(0, numbers):
        while True:
            #Generate square coordinates
            x = random.randint(0, size-1)
            y = random.randint(0, size-1)
            if puzzle[y][x] == 0:
                validNum = [numb for numb in range(1, size+1)]
                    
                #Check row for invalids
                for i in puzzle[y]:
                    if i in validNum:
                        validNum.remove(i)

                #Check column for invalids
                for i in puzzle:
                    if i[x] in validNum:
                        validNum.remove(i[x])

                #Check box for invalids
                Bx = (x//subsize) * subsize
                By = (y//subsize) * subsize
                for i in range(By, By + subsize):
                    for j in range(Bx, Bx + subsize):
                        if puzzle[i][j] in validNum:
                            validNum.remove(puzzle[i][j])

                #Pick number to place in square
                if len(validNum) <= 1:
                    try:
                        puzzle[y][x] = validNum[0]
                    except:
                        break
                else:
                    puzzle[y][x] = validNum[random.randint(0, len(validNum)-1)]
                break #break While True
    return puzzle

#Generates a filled, legal board for Sudoku
def generatePuzzle(size=9):
    subsize = int(size**0.5)
    
    #Create blank puzzle
    puzzle = [[0 for i in range(0, size)] for j in range(0, size)]

    #Fill out the diagonal sub-boxes
    for box in range(0, subsize):
        legalNum = list(range(1, size+1))
        i = box * subsize
        j = box * subsize
        for y in range(j, j + subsize):
            for x in range(i, i + subsize):
                num = random.choice(legalNum)
                puzzle[y][x] = num
                legalNum.remove(num)

    #Fill out the rest of the board
    #Here's an issue:
    #I want to use SudokuSolverMain.Sudoku().getInvalidNum()
    #to check what can go in each empty box.
    #This function's main purpose is to test if 
    #SudokuSolverMain.Sudoku() works.
    #Create b to test a, use a to make b. Is problem.

    return puzzle
    
##########MAIN##########
def main():
    writeSudokuPuzzles(2, 5, "Puzzles/")

if __name__ == "__main__":
    main()