#Author: Zephyrum Alsend
#Sudoku Generator
#Generates randomized Sudoku boards with a defined number of squares filled in,
#saving them to text files in the provided Path, named "Puzzle#.txt", with # being the counter in a for loop.
#Does not guarantee boards generated are solveable.
#Last Edited: 21/07/31

import random

#Creates n .txt files in Path, containing randomized Sudoku puzzles with numbers squares already filled in.
#n must be a positive integer.
#numbers must be a positive integer.
#Path must be a valid directory path.
def generateSudokuPuzzles(n, numbers, Path):
    size = 9
    subsize = int(size**0.5)
    if numbers > size**2:
        numbers = int(size**2)
    
    #Create i files
    for f in range(0, n):
        #Create blank puzzle
        puzzle = [[0 for i in range(0, size)] for j in range(0, size)]
        
        #With numbers squares filled in
        for s in range(0, numbers):
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

        #print puzzle to a .txt file
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
        #print(strPuzzle + "\n")

##########MAIN##########
def main():
    generateSudokuPuzzles(2, 5, "Puzzles/")

if __name__ == "__main__":
    main()