#!/usr/bin/env python

import argparse, sys, random

'''
    This is a random matrix generator for the Game of Life
    Give the size and then random cells will be generated
'''

SIZE = 0
PERCENTAGE_COVERED = 0
FILE = ""
VERSION = "1.0"


def main():
    numberOfCells = SIZE * SIZE
    numberOfLivingCells = int(round(numberOfCells * PERCENTAGE_COVERED / 100, 0))
    print("Generating Matrix...")
    finalMatrix = populateMatrice(numberOfLivingCells)
    if(FILE == ""):
        displayMatrice(finalMatrix)
    else:
        print("Writing to the file {}".format(FILE))
        writeFile(finalMatrix)



def writeFile(matrix):
    line = ""
    with open(FILE, "w") as f:
        for row in matrix:
            line = line.join(row)
            f.write(line + "\n")
            line = ""



def displayMatrice(matrice):
    ouptut = ''
    for line in matrice:
        for value in line:
            ouptut += '{} '.format(value)
        ouptut += '\n'
    print(ouptut)


def init_coord():
    initial = []
    for i in range(SIZE):
        for j in range(SIZE):
            initial.append((i, j))
    return initial

def createEmptyMatrice():
    mat = []
    for i in range(SIZE):
        temp = []
        for j in range(SIZE):
            temp.append('0')
        mat.append(temp)
    return mat

def populateMatrice(numberOfLivingCells):
    finalMatrix = createEmptyMatrice()
    for x, y in choosingLiveCells(init_coord(), numberOfLivingCells):
        finalMatrix[x][y] = '1'
    return finalMatrix


def choosingLiveCells(cellsList, numberOfLivingCells):
    livingCellsList = []
    for i in range(numberOfLivingCells):
        index = random.randint(0, len(cellsList) - 1)
        livingCellsList.append(cellsList[index])
        cellsList.pop(index)
    return livingCellsList

def version():
    print("gol_generator.py version {} by Cactuspin, 2020".format(VERSION))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''Creates a file containing a matrix of a given size 
    to be then executed by the Game of Life program.
    ''')

    parser.add_argument("size", help="The number of cells in a line of the field.", type=int)
    parser.add_argument("percentage", help="The percentage of living cells covering the field. (between 0 and 100)", type=int)
    parser.add_argument("-f", "--file", help="A text file were the generated field will be written.", default="")
    parser.add_argument("-v", "--version", help="Display the version number of this program", action="store_true")

    args = parser.parse_args()

    if args.version:
        version()
        sys.exit(0)

    if args.percentage < 0 or args.percentage > 100:
        print("Percentage must be between 0 and 100. See --help option for more details.")
        sys.exit(1)

    SIZE = args.size
    PERCENTAGE_COVERED = args.percentage
    FILE = args.file

    main()

