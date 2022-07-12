import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

blocks = 8
screenWidth = 800
blockSize = screenWidth / blocks
colorPossible = (154,225,255)

def placeText(text, x, y, color, size):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", size)
    text = font.render(text, 1, color)
    window.blit(text, (x, y))
    pygame.display.update()

class ChessPiece:
    name: str
    position: tuple
    color: str

    #liste mit Tupel relativ zur aktuellen Position 0
    jumpingArea: list

    directory = "./assets/"
    image: pygame.Surface

    def drawPiece(self, window):
        window.blit(self.image, (self.position[0]*blockSize, self.position[1]*blockSize))

    def getPossibleMoves(self):
        blockToDrawList = list()
        for i in self.jumpingArea:
        #add the new tuple to the list
        #if the tuple is not occupied

            x=self.position[0]+i[0]
            y=self.position[1]+i[1]

            if x<0 or x>=blocks or y<0 or y>=blocks:
                continue

            print("INDEX x: ", x, "y: ", y)

    	    #Darf sich an ein Feld bewegen, wenn es frei ist (None) oder wenn dort eine Figur mit anderer Farbe ist
            if board.boardArray[x][y] == None or board.boardArray[x][y].color != self.color:
                blockToDrawList.append((self.position[0]+i[0], self.position[1]+i[1]))
            
            #alle Möglichkeiten ausgeben
            #blockToDrawList.append((piece.position[0] + i[0], piece.position[1] + i[1]))

        return blockToDrawList


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
    isFirstMove = True

    def __init__(self, position, color):
        self.name = "Pawn"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,1),(1,-1),(-1,1),(-1,-1)]

        img = pygame.image.load(self.directory + "pawn_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Board:
    whitePieces: list
    blackPieces: list
    boardArray = [[None for x in range(blocks+1)] for y in range(blocks+1)]
    focusedPiece: ChessPiece = None

    def __init__(self, whitePieces, blackPieces):
        self.whitePieces = whitePieces
        self.blackPieces = blackPieces

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
        #Prüfen ob neues Feld erreichbar ist
        if newPosition not in piece.getPossibleMoves():
            return False

        #Alte Position freigeben
        self.boardArray[piece.position[0]][piece.position[1]] = None

        #Prüfen ob neues Feld belegt ist
        if self.boardArray[newPosition[0]][newPosition[1]] != None and self.boardArray[newPosition[0]][newPosition[1]].color == piece.color:
            print("Feld belegt")
        else:
            #Neue Position belegen
            piece.position = newPosition
            self.boardArray[newPosition[0]][newPosition[1]] = piece
            piece.position = newPosition

        #Fokus aufheben
        self.focusedPiece = None
        return True

    def getPiece(self, x, y):
        return self.boardArray[x][y]

    #evtl Board Klasse hinzufügen
    def drawBoard(self, window, board):
        blockWidth = blockSize
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

        #Jede Figur im Array wird angezeigt
        for i in range(8):
            for j in range(8):
                if board.boardArray[i][j] != None:
                    board.boardArray[i][j].drawPiece(window)

        pygame.display.update()

    #evtl Board Klasse hinzufügen
    def focusPieceAndColor(self, window, piece, color, board):
        self.drawBoard(window, board)

        board.focusedPiece = piece

        blockWidth = screenWidth // 8
        x= (8-1)*blockWidth

        possibleMoves = piece.getPossibleMoves()

        #draw positon of the piece
        print("drawing piece at: ", piece.position)
        pygame.draw.rect(window, (255,0,0), (piece.position[0]*blockWidth, piece.position[1]*blockWidth, blockWidth, blockWidth))
        piece.drawPiece(window)
        pygame.display.update()

        print(possibleMoves)
        for tupel in possibleMoves:
            print(f"{tupel[0]}, {tupel[1]}")
            pygame.draw.rect(window, color, (tupel[0]*blockWidth, tupel[1]*blockWidth, blockWidth, blockWidth))

            #Wenn Figur auf dem Feld ist, dann zeichnen
            if board.boardArray[tupel[0]][tupel[1]] != None:
                board.boardArray[tupel[0]][tupel[1]].drawPiece(window)

        #pygame.draw.rect(window, color, (col*blockWidth, row*blockWidth, blockWidth, blockWidth))
        pygame.display.update()




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

BlackPieceList = [KingBlack, QueenBlack, RookBlack1, RookBlack2, BishopBlack1, BishopBlack2, KnightBlack1, KnightBlack2, PawnBlack1, PawnBlack2, PawnBlack3, PawnBlack4, PawnBlack5, PawnBlack6, PawnBlack7, PawnBlack8]
WhitePieceList = [KingWhite, QueenWhite, RookWhite1, RookWhite2, BishopWhite1, BishopWhite2, KnightWhite1, KnightWhite2, PawnWhite1, PawnWhite2, PawnWhite3, PawnWhite4, PawnWhite5, PawnWhite6, PawnWhite7, PawnWhite8]

window = pygame.display.set_mode((screenWidth, screenWidth))

pygame.display.set_caption("Python Chess")



board = Board(WhitePieceList, BlackPieceList)

board.drawBoard(window, board)

pygame.display.update()

#placeText("Starte Spiel", 0,0,(0,0,255), 50)



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

            pieceOrNone = board.getPiece(x, y)
            print(pieceOrNone)

            #Wenn keiner den Fokus hat und Wenn auf dem Feld kein Spieler steht
            if pieceOrNone == None and board.focusedPiece == None:
                print("no piece focussed")
                continue

            #Wenn keine Figur den Fokus hat, fokussieren
            if board.focusedPiece == None:
                if pieceOrNone != None:
                    board.focusPieceAndColor(window, pieceOrNone, colorPossible, board)
                    continue

            #Wenn auf dem Feld eine Figur steht
            if pieceOrNone != None:
                #Wenn dieselbe Figur gewählt wird, der bereits den Fokus hat, dann Fokus entfernen
                if board.focusedPiece == pieceOrNone:
                    board.drawBoard(window, board)
                    board.focusedPiece = None
                else:
                    #Auf dem Feld steht eine Figur derselben Farbe, Fokus wird gewechselt
                    if board.focusedPiece.color == board.getPiece(x, y).color:
                        board.focusPieceAndColor(window, pieceOrNone, colorPossible, board)
                    else:
                        #bewegen
                        if board.movePiece(board.focusedPiece, (x,y)):
                            board.drawBoard(window, board)
                        pygame.display.update()
                continue            
            else:#Wenn auf dem Feld kein Spieler steht, dann wird der bewegt und der Fokus aufgehoben
                if board.movePiece(board.focusedPiece, (x, y)):
                    board.drawBoard(window, board)
                    pygame.display.update()
                    continue