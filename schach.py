import math
import random
import pygame
import tkinter as tk
import numpy as np
import PySimpleGUI as sg
from tkinter import messagebox

blocks = 8
screenWidth = 800
#blockSize = screenWidth / blocks
blockSize = 100
padding = (screenWidth - (blocks * blockSize)) /2
print("padding: " + str(padding))
colorPossible = (154,225,255)

def placeText(text, x, y, color, size):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", size)
    text = font.render(text, 1, color)
    window.blit(text, (x, y))
    pygame.display.update()

class ChessPiece:
    name: str
    #nach https://en.wikipedia.org/wiki/Chess_piece_relative_value#Standard_valuations
    value: int
    position: tuple
    color: str

    #liste mit Tupel relativ zur aktuellen Position 0
    jumpingArea: list
    endlessDirection: bool

    directory = "./assets/"
    image: pygame.Surface

    def drawPiece(self, window):
        window.blit(self.image, (self.position[0]*blockSize  + padding, self.position[1]*blockSize + padding))

    

    def movePiece(self, board, newPosition):
        #Prüfen ob neues Feld erreichbar ist
        if newPosition not in self.getPossibleMoves(board):
            return False

        #Alte Position freigeben
        board.boardArray[self.position[0]][self.position[1]] = None

        #Prüfen ob neues Feld belegt ist
        if board.boardArray[newPosition[0]][newPosition[1]] != None and board.boardArray[newPosition[0]][newPosition[1]].color == self.color:
            print("Feld belegt")
        else:
            board.addPoints(self, newPosition)
            #board.deleteFromPieceList(newPosition)
            #Neue Position belegen
            self.position = newPosition
            board.deleteFromPieceList(board.boardArray[newPosition[0]][newPosition[1]])
            #board.boardArray[newPosition[0]][newPosition[1]] = self
            board.setPieceOnField(self, newPosition)
            self.position = newPosition
            #en passant prüfen
            if self.name == "Pawn":
                if self.color == "white" and board.boardArray[newPosition[0]][newPosition[1]+1] != None and board.boardArray[newPosition[0]][newPosition[1]+1].color == "black":
                    #board.replacePieceWithPiece(None, (newPosition[0], newPosition[1]+1))
                    board.addPoints(self, (newPosition[0], newPosition[1]+1))
                    board.deleteFromPieceList(board.boardArray[newPosition[0]][newPosition[1]+1])
                    board.boardArray[newPosition[0]][newPosition[1]+1] = None
                if self.color == "black" and board.boardArray[newPosition[0]][newPosition[1]-1] != None and board.boardArray[newPosition[0]][newPosition[1]-1].color == "white":
                    #board.replacePieceWithPiece(None, (newPosition[0], newPosition[1]-1))
                    board.addPoints(self, (newPosition[0],newPosition[1]-1))
                    board.deleteFromPieceList(board.boardArray[newPosition[0]][newPosition[1]-1])
                    board.boardArray[newPosition[0]][newPosition[1]-1] = None
                if newPosition[1] == 7 or newPosition[1] == 0:
                    board.createQueen(self.position, self.color)

                

        #Fokus aufheben, wenn erfolgreich bewegt wurde
        board.focusedPiece = None
        board.isBlackTurn = not board.isBlackTurn
        if self.name == "Pawn":
            self.isFirstMove = False

        if len(board.blackPieces) == 0 or len(board.whitePieces) == 0:
            print("ENDE")
            pygame.quit()
        return True

    def getPossibleMoves(self, board):
        possibleFields = list()

        #print(np.matrix(board.boardArray))
        nextFree=True
        
        for tupel in self.jumpingArea:
        #add the new tuple to the list
        #if the tuple is not occupied

            xPosition = self.position[0]
            yPosition = self.position[1]

            xZiel=xPosition+tupel[0]
            yZiel=yPosition+tupel[1]

            if xZiel<0 or xZiel>=blocks or yZiel<0 or yZiel>=blocks:
                continue
            
            if self.endlessDirection:
                counter = 1
                while True:
                    #Wenn das Feld nicht leer ist
                    if board.boardArray[xPosition+counter*tupel[0]][yPosition+counter*tupel[1]] != None:
                        #Wenn auf dem Feld ein anderer Spieler ist füge nich hinzu
                        if  board.boardArray[xPosition+counter*tupel[0]][yPosition+counter*tupel[1]].color != self.color:
                            possibleFields.append((xPosition+counter*tupel[0],yPosition+counter*tupel[1]))
                        break
                    else:
                        #Wenn es leer ist füge das Feld hinzu
                        possibleFields.append((xPosition+counter*tupel[0],yPosition+counter*tupel[1]))
                        counter += 1

                    #Nur gültige Feldindizes verwenden, bei Überlauf abbrechen
                    if xPosition+counter*tupel[0] >7 or xPosition+counter*tupel[0] <0 or yPosition+counter*tupel[1] >7 or yPosition+counter*tupel[1] <0:
                        break
                    

            #Spezielle Regeln für die Bauern
            if self.name == "Pawn":
                #Bei bestimmten Bedingungen wird der Durchlauf abgebrochen. Ansonsten wird das Feld der Liste hinzugefügt

                #Bauer darf nicht zurückgehen
                if self.color == "white" and tupel[1]>0 or self.color == "black" and tupel[1]<0:
                    continue

                #1. Prüfe Diagonale Felder
                if tupel in [(-1,1),(-1,-1),(1,1),(1,-1)] and board.boardArray[xZiel][yZiel] == None:
                        #en passant prüfen, und ggf. anhängen
                        if board.boardArray[xZiel][yZiel-tupel[1]] != None and board.boardArray[xZiel][yZiel-tupel[1]].color != self.color:
                            possibleFields.append((xZiel,yZiel))
                        continue
                
                #2. Prüfe Vorwärts Felder
                else:#tupel muss in [(0,1),(0,2),(0,-1),(0,-2)] enthalten sein
                    if tupel in [(0,1),(0,-1)] and board.boardArray[xPosition][yPosition +tupel[1]] != None:
                        nextFree = False
                        continue
                    
                    if tupel in [(0,2),(0,-2)] and not self.isFirstMove or not nextFree:
                        continue

    	    #Darf sich an ein Feld bewegen, wenn es frei ist (None) oder wenn dort eine Figur mit anderer Farbe ist
            if board.boardArray[xZiel][yZiel] == None or board.boardArray[xZiel][yZiel].color != self.color:
                possibleFields.append((xZiel, yZiel))
            
            #alle Möglichkeiten ausgeben
            #blockToDrawList.append((piece.position[0] + i[0], piece.position[1] + i[1]))

        return possibleFields


class King(ChessPiece):
    endlessDirection = False
    value = 200
    def __init__(self, position, color):
        self.name = "King"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]
        
        img = pygame.image.load(self.directory + "king_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Queen(ChessPiece):
    endlessDirection = True
    value = 9
    def __init__(self, position, color):
        self.name = "Queen"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,1),(1,-1),(-1,1),(-1,-1),(1,0),(-1,0),(0,1),(0,-1)]

        img = pygame.image.load(self.directory + "queen_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Rook(ChessPiece):
    endlessDirection = True
    value = 5
    def __init__(self, position, color):
        self.name = "Rook"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,0),(-1,0),(0,1),(0,-1)]

        img = pygame.image.load(self.directory + "rook_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Bishop(ChessPiece):
    endlessDirection = True
    value = 3
    def __init__(self, position, color):
        self.name = "Bishop"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,1),(1,-1),(-1,1),(-1,-1)]

        img = pygame.image.load(self.directory + "bishop_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Knight(ChessPiece):
    endlessDirection = False
    value = 3
    def __init__(self, position, color):
        self.name = "Knight"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]

        img = pygame.image.load(self.directory + "knight_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))

class Pawn(ChessPiece):
    isFirstMove = True
    endlessDirection = False
    value = 1

    def __init__(self, position, color):
        self.name = "Pawn"
        self.position = position
        self.color = color
        self.jumpingArea = [(1,1),(1,-1),(-1,1),(-1,-1), (0,1), (0,-1), (0,2),  (0,-2)]

        img = pygame.image.load(self.directory + "pawn_" + color + ".png")
        self.image = pygame.transform.scale(img, (blockSize, blockSize))
        

class Board:
    whitePoints = 0
    blackPoints = 0
    whitePieces: list
    blackPieces: list 
    boardArray = [[None for x in range(blocks+1)] for y in range(blocks+1)]
    focusedPiece: ChessPiece = None
    isBlackTurn = True

    def __init__(self, whitePieces, blackPieces):
        
        self.whitePieces = whitePieces
        self.blackPieces = blackPieces

        for piece in whitePieces:
            xPosition = piece.position[0]
            yPosition = piece.position[1]
            self.boardArray[xPosition][yPosition] = piece

        for piece in blackPieces:
            xPosition = piece.position[0]
            yPosition = piece.position[1]
            self.boardArray[xPosition][yPosition] = piece

    def getPiece(self, x, y):
        return self.boardArray[x][y]

    #Fügt Punkte hinzu, falls eine Figur an der Position existiert
    def addPoints(self, pieceToMove, position):
        if self.boardArray[position[0]][position[1]] != None and self.boardArray[position[0]][position[1]].color != pieceToMove.color:
                color = self.boardArray[position[0]][position[1]].color
                if color == "white":
                    self.blackPoints += self.boardArray[position[0]][position[1]].value
                else:
                    self.whitePoints += self.boardArray[position[0]][position[1]].value
    
    #Estelle und Platziere eine Königing an gegebener Position und Farbe
    def createQueen(self, position, color):
        queen = Queen(position, color)
        if color == "white":
            self.whitePieces.append(queen)
            self.boardArray[position[0]][position[1]] = queen
        else:
            self.blackPieces.append(queen)
            self.boardArray[position[0]][position[1]] = queen

    def deleteFromPieceList(self, piece):
        if piece == None:
            return
        if piece.color == "white":
            self.whitePieces.remove(piece)
        else:
            self.blackPieces.remove(piece)
    
    #Ersetzt bzw setzt eine Figur an gegebener Position
    def setPieceOnField(self, newPiece, newPosition):
        if newPiece == None:
            self.boardArray[newPosition[0]][newPosition[1]] = None
            if newPiece.color == "white":
                self.whitePieces.remove(newPiece)
            else:
                self.blackPieces.remove(newPiece)
            
            self.addPoints(newPiece, newPosition)
        else:
            self.boardArray[newPosition[0]][newPosition[1]] = newPiece


    #evtl Board Klasse hinzufügen
    def drawBoard(self, window, board):
        blockWidth = blockSize
        BLACK=(205, 133, 63)
        WHITE=(245,222,179)

        isBlack = False

        for i in range(8):
            for j in range(8):
                if isBlack:
                    pygame.draw.rect(window, BLACK, (i*blockWidth+ padding, j*blockWidth + padding, blockWidth, blockWidth))
                else:
                    pygame.draw.rect(window, WHITE, (i*blockWidth + padding, j*blockWidth + padding, blockWidth, blockWidth))
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

        blockWidth = blockSize

        possibleMoves = piece.getPossibleMoves( board )

        #draw positon of the piece
        print("drawing piece at: ", piece.position)
        pygame.draw.rect(window, (255,0,0), (piece.position[0]*blockWidth, piece.position[1]*blockWidth, blockWidth, blockWidth))
        piece.drawPiece(window)
        pygame.display.update()

        print(possibleMoves)
        for tupel in possibleMoves:
            #print(f"{tupel[0]}, {tupel[1]}")
            pygame.draw.rect(window, color, (tupel[0]*blockWidth, tupel[1]*blockWidth, blockWidth, blockWidth))

            #Wenn Figur auf dem Feld ist, dann zeichnen
            if board.boardArray[tupel[0]][tupel[1]] != None:
                board.boardArray[tupel[0]][tupel[1]].drawPiece(window)

        #pygame.draw.rect(window, color, (col*blockWidth, row*blockWidth, blockWidth, blockWidth))
        pygame.display.update()


def gameWindow(startingColor):
    print("startng color: ", startingColor)

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

    blackPieces = [KingBlack, QueenBlack, RookBlack1, RookBlack2, BishopBlack1, BishopBlack2, KnightBlack1, KnightBlack2, PawnBlack1, PawnBlack2, PawnBlack3, PawnBlack4, PawnBlack5, PawnBlack6, PawnBlack7, PawnBlack8]
    whitePieces = [KingWhite, QueenWhite, RookWhite1, RookWhite2, BishopWhite1, BishopWhite2, KnightWhite1, KnightWhite2, PawnWhite1, PawnWhite2, PawnWhite3, PawnWhite4, PawnWhite5, PawnWhite6, PawnWhite7, PawnWhite8]

    window = pygame.display.set_mode((screenWidth, screenWidth))

    pygame.display.set_caption("Python Chess")
    board = Board(whitePieces, blackPieces)

    if startingColor == "black":
        board.isBlackTurn = True
    else:
        board.isBlackTurn = False

    board.drawBoard(window, board)
    pygame.display.update()

    running = True
    while running:
        pygame.time.delay(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Points of black: ", board.blackPoints)
                print("Points of white: ", board.whitePoints)
                #menu_window()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.isBlackTurn:
                    print("Black Turn")
                else:
                    print("White Turn")

                pos = pygame.mouse.get_pos()
                #print(pos)

                #Geklickte Position ermitteln
                x = pos[0] // (screenWidth // blocks)
                y = pos[1] // (screenWidth // blocks)
                #print("x: ", x, " y: ", y)

                pieceOrNone = board.getPiece(x, y)
                #print(pieceOrNone)

                #Wenn keiner den Fokus hat und Wenn auf dem Feld kein Spieler steht
                if pieceOrNone == None and board.focusedPiece == None:
                    print("no piece focussed")
                    continue

                #Wenn keine Figur den Fokus hat, fokussieren
                if board.focusedPiece == None and pieceOrNone != None:
                    #Prüfen ob die ausgewählte Farbe am Zug ist
                    #if pieceOrNone.color == board.isBlackTurn ? "black" : "white":
                    if pieceOrNone.color == "black" if board.isBlackTurn else pieceOrNone.color == "white":
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
                            if board.focusedPiece.movePiece(board, (x,y)):
                                board.drawBoard(window, board)
                            pygame.display.update()
                    continue            
                else:#Wenn auf dem Feld kein Spieler steht, dann wird der bewegt und der Fokus aufgehoben
                    if  board.focusedPiece.movePiece(board, (x, y)):
                        board.drawBoard(window, board)
                        pygame.display.update()
                        continue

def menu_window():
    #Radio-Buttons nach https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Radio_Buttons_Simulated.py
    radio_unchecked = b'iVBORw0KGgoAAAANSUhEUgAAABkAAAAZCAYAAADE6YVjAAAEwElEQVR4nI1W3W9URRT/nZm7ZXdpbajdWpCAjcFEqw88+CACrgaBmFBIwI3fPPpPaJYND/wjYsxFYgwP+BV2kY9gNCIJIhEIBZSWLl3aprvde2fOOT7c3W27fNSTTO7cMzO/35wz55wZYAVRVVMuaxCGoV2qD8PQlsvlQFXNShhPAqduYEr0lrrmhmFoVbVbvWzdQxKGoS0UCgwAFy6PvySx27cQRVvY80YGZyHaIKJbPUHqvCF8k3/tlb+61z2RJAzVFgrE5QuX1q9K9x6Oouj9TCazKmUBawiAglkQO0bsPOqNejOw9qsoan62Z8eWfx9FRMsJkgnnfrv6FgXBUWOD4UzAWJsb8L3ZNFlrCQSwZ8TO6excXe/eux/UY0EcuQkXRx/t3fX6qW6iDomqGiKS87///QaM/Q7K6efXD7rBgf5AVcl7hgBQEYgqVAQEgqroZLXmb9yeTLGgKRztHtu5/XQbr0NSVDU4dAhvj703LGouBpaGXhwZ5v6nem0cO2gCB002AxGBiICZwSwIrEVtZpav3LhjneN76YxsvnDq1D0AKJVKYgBg9NgxKpVKIkpH0ulVQyPrBvxTfb02ih2ICESAdp2darJHIkIUx+jrXW03rB30PT09zzTm5UipVJLR0VECAGqb9csfV16oN3H56f60Hd20gZzzRJR4UzvAusySxBoBi8A5DyLolWvjOv1gjldnUqN7duavFYtFYyoVGACIvd2fzWZSw4P9IqKkLfBugu4GKFSSr4hSbqBfMplMaiFyBwAgn88bU60eUwCI43hbYIBsJk2e+bHAiQVL/xWiSTB4ZmQzabKG4B1vBYBqtapBoVBgVaUfz13aaI3CEBGzgAjouEuXg3bARSG6pImADJEhwLN/TlWJiDhoecOqSHYpUIJPHYclY4CqdBElZ6Otfse9otlKBRaAb5OwqjbaYSnatqKzpEXQAleFsIAlCWERBbfyR4TBwlDVRj4PBgAThqElIgVhPPaicew02R0vi6ClESWcALEkkbV0bhQ7dZ4VpONEpGEYWpPL5QgArLVnYsc0N99QAuC5nWy8JPEYvtW4PS6LfVXFfL2hznkyxv4MALlcjkwlnxcACCj4ul6fjyeqNeOZ1Xu/COoXwX0XkbDAs8B7BjPrVLVm6vVGDOXjAFCpVMSUiCQMQ/vmlpevE+nRyJOZul9jYwix84sEfrG1d94h9A5EQHW6xrEXYwhffFLYe/3dMLSlUkmS2lUsGgB4Nf/OEIleJEPDI88Ocl/vauu8b5UQdA69nS/t2mWIMDM3x+P/TFp2flKM3Tz+569T7dr1UBU+8dPZbWRS30M4s25ojVvT3xcIlNpRpCpd+cI6XZvxd6emUyrUEPW7DhbGzi6twp37mVpu27Nj65lmo7lbgDsT9+dSV2/cotqDWR/HMYt4ERHx7CWKIq7NzPrrN2/TVG0uBcVt56PdBwtjZ1sRKx3sruLaubiOnzy51tq+wy6KP0j19GSsAQwtlnrPjNgxmgvNBWvNl41m8/NPP94/seLN2E0EACd+qGxyse5runi7Zz+iLL2imLcGN1PWnhYNvv3wwM5r3ev+lzzqtdLSB926lV4rK0qxWDTlcvmx7652ZD5J/gNoDCDS80MCGwAAAABJRU5ErkJggg=='
    radio_checked = b'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'

    radio_keys = ('-R1-', '-R2-')

    def check_radio(key):
        for k in radio_keys:
            window[k].update(radio_unchecked)
            window[k].metadata = False
        window[key].update(radio_checked)
        window[key].metadata = True

    def radio_is_checked(key):
        return window[key].metadata

    layout = [
    [sg.Text('Schachspiel', size=(20, 1),
             justification='center', font=('Helvetica', 20), key='title')],
    [sg.Text("Welche Farbe beginnt?", size=(20, 1),)],
    [sg.Image(radio_checked, enable_events=True, k='-R1-', metadata=True), sg.T('Schwarz', enable_events=True, k='-T1-')],
    [sg.Image(radio_unchecked, enable_events=True, k='-R2-', metadata=False), sg.T('Weiß', enable_events=True, k='-T2-')],
    [sg.Button('Spiel starten', button_color=('white', 'black'), key='start', size=(20, 1)),],
    ]

    window = sg.Window("Button Click", layout, auto_size_buttons=False,
                   default_button_element_size=(12, 1), use_default_focus=False, finalize=True)

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'start':
            window.close()
            gameWindow("black" if radio_is_checked('-R1-') else "white")
        
        if event in radio_keys:
            check_radio(event)
        elif event.startswith('-T'):        # If text element clicked, change it into a radio button key
            check_radio(event.replace('T', 'R'))

        for k in radio_keys:
            print(f'Radio key {k} is {radio_is_checked(k)}')
            
    window.close()

#gameWindow()
menu_window()
