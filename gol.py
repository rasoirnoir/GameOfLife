#!/usr/bin/env python

import sys, time, pygame

'''
    implémentation en python du célèbre automate cellulaire.
    Les règles:
        - Une cellule avec 2 ou 3 voisins survit
        - Une cellule morte avec 3 voisins vivant devient vivante
        - Une cellule ayant moins de 2 ou plus de 3 voisins vivants meurt (ou reste morte)

        - résumé en 2 règles : 
            - 2 voisines => même état
            - 3 voisine => vivante
'''

DEBUG = False
FPS = 2


#Définition des règles du jeu
def alive(vivante, nb_voisines):
    switcher = {
        2: vivante,
        3: True
    }
    return switcher.get(nb_voisines, False)

def help():
    print('usage: python gol.py <file>')
    print('       Where <file> is the descriptive matrice of the initial board')

def main(argv):
    if DEBUG: print('debug mode ON')
    fileName = ''
    if len(argv) != 1:
        help()
        exit(1)
    
    if len(argv) == 1:
        fileName = argv[0]
        initialBoard = []

        try:
            with open(fileName, 'r') as stream:
                boardDegeu = stream.read().split()
                for i in range(len(boardDegeu)):
                    ligne = []
                    for j in range(len(boardDegeu[i])):
                        ligne.append(boardDegeu[i][j])
                    initialBoard.append(ligne)
                if DEBUG: 
                    print('Initial board :')
                    displayMatrice(initialBoard)
                    print(initialBoard)
        except FileNotFoundError:
            print('{} not found. Exiting...'.format(fileName))
            exit(1)
        gameStart(initialBoard)
        


def gameStart(board):

    tmpBoard = board
    nextBoard = []

    pygame.init()
    size = width, height = 800, 600
    smallest = width if width < height else height
    screen = pygame.display.set_mode(size)
    caption = pygame.display.set_caption("Game of Life")
    screen.fill((255, 255, 255))

    cell_size = smallest / len(board[0])
    #cell = pygame.Rect(0, 0, cell_size, cell_size)
    #pygame.draw.rect(screen, (0, 0, 0), cell)

    
    running = True
    finished = False
    while running:    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        while not finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    finished = True
            displayMatrice(tmpBoard)
            drawMatrice(screen, tmpBoard, cell_size)
            nextBoard = nextIte(tmpBoard)
            pygame.display.flip()
            if nextBoard == tmpBoard:
                finished = True
            tmpBoard = nextBoard
            time.sleep(1 / FPS)


def drawMatrice(surface, matrice, cell_size):
    surface.fill((255, 255, 255))
    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            if(matrice[i][j] == '1'):
                pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size))

        
def nextIte(board):
    #Iteration suivante du jeu suivant les règles définies
    # 1- Pour chaque cellule, on calcul le nombre de voisines vivantes
    # 2- On determine ensuite si elle doit être vivante ou morte à la prochaine itération
    if DEBUG: print('Next itereration')
    nextBoard = newMatrice(len(board), len(board[0]))
    voisine = newMatrice(len(board), len(board[0]))
    for line in range(len(board)):
        for col in range(len(board[line])):
            nbVoisines = 0
            if col-1 >= 0:
                if line-1 >= 0:
                    if board[line-1][col-1] == '1':
                        nbVoisines+=1
                if board[line][col-1] == '1':
                    nbVoisines+=1
                if line+1 < len(board):
                    if board[line+1][col-1] == '1':
                        nbVoisines+=1
            if line-1 >= 0:
                if board[line-1][col] == '1':
                       nbVoisines+=1
            if line+1 < len(board):
                if board[line+1][col] == '1':
                    nbVoisines+=1
            if col+1 < len(board[line]):
                if line-1 >= 0:
                    if board[line-1][col+1] == '1':
                        nbVoisines+=1
                if board[line][col+1] == '1':
                    nbVoisines+=1
                if line+1 < len(board):
                    if board[line+1][col+1] == '1':
                        nbVoisines+=1            
            voisine[line][col] = nbVoisines
            if alive(board[line][col] == '1', nbVoisines):
                nextBoard[line][col] = '1'
            else:
                nextBoard[line][col] = '0'
    if DEBUG: 
        print('Matrice voisines :')
        displayMatrice(voisine)
        print('Matrice suivante :')
        displayMatrice(nextBoard)
    return nextBoard

def displayMatrice(matrice):
    ouptut = ''
    for line in matrice:
        for value in line:
            ouptut += '{} '.format(value)
        ouptut += '\n'
    print(ouptut)

def newMatrice(height, width):
    mat = []
    for i in range(height):
        temp = []
        for j in range(width):
            temp.append(0)
        mat.append(temp)
    return mat
    

if __name__ == "__main__":
    main(sys.argv[1:])
