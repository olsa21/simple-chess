import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

blocks = 8
screenWidth = 800
blockSize = screenWidth // blocks

class Board:
    boardArray = [[None for x in range(blocks+1)] for y in range(blocks+1)] 

    def __init__(self, whitePieces, blackPieces):
        for i in whitePieces:
            #print("i[0]=" + str(i[0]) + " i[1]=" + str(i[1]))
            xPosition = i.position[0]
            yPosition = i.position[1]
            self.boardArray[xPosition][yPosition] = i

        for i in blackPieces:
            xPosition = i.position[0]
            yPosition = i.position[1]
            self.boardArray[xPosition][yPosition] = i

    def movePiece(self, piece, newPosition):
        xPosition = piece.position[0]
        yPosition = piece.position[1]
        self.boardArray[xPosition][yPosition] = None
        self.boardArray[newPosition[0]][newPosition[1]] = 1
        piece.position = newPosition

    def getPiece(self, x, y):
        return self.boardArray[x][y]

class ChessPiece:
    name: str
    position: tuple
    color: str

    #liste mit Tupel relativ zur aktuellen Position 0
    jumpingArea: list

    directory = "./assets/"
    image: pygame.Surface

class King(ChessPiece):
    def __init__(self, position, color):
        self.name = "King"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]
        
        img = pygame.image.load(self.directory + "king_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Queen(ChessPiece):
    def __init__(self, position, color):
        self.name = "Queen"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]

        img = pygame.image.load(self.directory + "queen_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Rook(ChessPiece):
    def __init__(self, position, color):
        self.name = "Rook"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,0),(-1,0),(0,1),(0,-1)]

        img = pygame.image.load(self.directory + "rook_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Bishop(ChessPiece):
    def __init__(self, position, color):
        self.name = "Bishop"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,1),(1,-1),(-1,1),(-1,-1)]

        img = pygame.image.load(self.directory + "bishop_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Knight(ChessPiece):
    def __init__(self, position, color):
        self.name = "Knight"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]

        img = pygame.image.load(self.directory + "knight_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Pawn(ChessPiece):
    def __init__(self, position, color):
        self.name = "Pawn"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,1),(1,-1),(-1,1),(-1,-1)]

        img = pygame.image.load(self.directory + "pawn_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))


def drawBoard(window):
    blockWidth = screenWidth // 8
    BLACK=(205, 133, 63)
    WHITE=(245,222,179)

    isBlack = False

    for i in range(8):
        for j in range(8):
            if isBlack:
                pygame.draw.rect(window, BLACK, (i*blockWidth, j*blockWidth, blockWidth, blockWidth))
            else:
                pygame.draw.rect(window, WHITE, (i*blockWidth, j*blockWidth, blockWidth, blockWidth))
            isBlack = not isBlack
        isBlack = not isBlack

    #pygame.draw.rect(window,BLUE,(0,0,50,50))
    #pygame.draw.rect(window,WHITE,(0,50,50,50))
    pygame.display.update()

def colorizeBlock(window, piece, color, board):
    blockWidth = screenWidth // 8
    x= (8-1)*blockWidth

    blockToDrawList = list()

    #for every tuple in the jumping area
    for i in piece.jumpingArea:
        #add the new tuple to the list
        #if the tuple is not occupied
        print()



        #if board.boardArray[piece.position[0]+i[0]][piece.position[1]+i[1]] == None:
        #    blockToDrawList.append((piece.position[0]+i[0], piece.position[1]+i[1]))
        blockToDrawList.append((piece.position[0] + i[0], piece.position[1] + i[1]))

    #draw positon of the piece
    print("drawing piece at: ", piece.position)
    pygame.draw.rect(window, (255,0,0), (piece.position[0]*blockWidth, piece.position[1]*blockWidth, blockWidth, blockWidth))
    pygame.display.update()

    print(blockToDrawList)
    for tupel in blockToDrawList:
        print(f"{tupel[0]}, {tupel[1]}")
        pygame.draw.rect(window, color, (tupel[0]*blockWidth, tupel[1]*blockWidth, blockWidth, blockWidth))

    #pygame.draw.rect(window, color, (col*blockWidth, row*blockWidth, blockWidth, blockWidth))
    pygame.display.update()

window = pygame.display.set_mode((screenWidth, screenWidth))

drawBoard(window)

pygame.time.delay(1000)

#tupelList = [(0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]


#Figuren werden erstellt
#Wenn oben links die Position 0,0 ist
KingBlack = King((4,0), "black")
QueenBlack = Queen((3,0), "black")
RookBlack1 = Rook((0,0), "black")
RookBlack2 = Rook((7,0), "black")
BishopBlack1 = Bishop((2,0), "black")
BishopBlack2 = Bishop((5,0), "black")
KnightBlack1 = Knight((1,0), "black")
KnightBlack2 = Knight((6,0), "black")
PawnBlack1 = Pawn((0,1), "black")
PawnBlack2 = Pawn((1,1), "black")
PawnBlack3 = Pawn((2,1), "black")
PawnBlack4 = Pawn((3,1), "black")
PawnBlack5 = Pawn((4,1), "black")
PawnBlack6 = Pawn((5,1), "black")
PawnBlack7 = Pawn((6,1), "black")
PawnBlack8 = Pawn((7,1), "black")

BlackPieceList = [KingBlack, QueenBlack, RookBlack1, RookBlack2, BishopBlack1, BishopBlack2, KnightBlack1, KnightBlack2, PawnBlack1, PawnBlack2, PawnBlack3, PawnBlack4, PawnBlack5, PawnBlack6, PawnBlack7, PawnBlack8]

KingWhite = King((4,7), "white")
QueenWhite = Queen((3,7), "white")
RookWhite1 = Rook((0,7), "white")
RookWhite2 = Rook((7,7), "white")
BishopWhite1 = Bishop((2,7), "white")
BishopWhite2 = Bishop((5,7), "white")
KnightWhite1 = Knight((1,7), "white")
KnightWhite2 = Knight((6,7), "white")
PawnWhite1 = Pawn((0,6), "white")
PawnWhite2 = Pawn((1,6), "white")
PawnWhite3 = Pawn((2,6), "white")
PawnWhite4 = Pawn((3,6), "white")
PawnWhite5 = Pawn((4,6), "white")
PawnWhite6 = Pawn((5,6), "white")
PawnWhite7 = Pawn((6,6), "white")
PawnWhite8 = Pawn((7,6), "white")

#image = pygame.image.load("./assets/bishop_white.png")

#image = pygame.image.load(KingBlack.imageFile)
#window.blit(image, (KingBlack.position[0]*screenWidth//8, KingBlack.position[1]*screenWidth//8))

#window.blit(KingBlack.image, (KingBlack.position[0]*blockSize, KingBlack.position[1]*blockSize))

WhitePieceList = [KingWhite, QueenWhite, RookWhite1, RookWhite2, BishopWhite1, BishopWhite2, KnightWhite1, KnightWhite2, PawnWhite1, PawnWhite2, PawnWhite3, PawnWhite4, PawnWhite5, PawnWhite6, PawnWhite7, PawnWhite8]

for i in WhitePieceList:
    window.blit(i.image, (i.position[0]*blockSize, i.position[1]*blockSize))

for i in BlackPieceList:
    window.blit(i.image, (i.position[0]*blockSize, i.position[1]*blockSize))

board = Board(WhitePieceList, BlackPieceList)

color = (154,225,255)
#colorizeBlock(window, KnightWhite2, color, board)


pygame.time.delay(1000)

running = True
while running:
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)

            #Geklickte Position ermitteln
            x = pos[0] // (screenWidth // blocks)
            y = pos[1] // (screenWidth // blocks)
            print("x: ", x, " y: ", y)

            piece = board.getPiece(x, y)
            print(piece)

            if piece != None:
                colorizeBlock(window, piece, color, board)