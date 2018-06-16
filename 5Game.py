import pygame as pg
from time import sleep
import numpy as np
from 5GameAI import *
from sys import argv


#--------------------------------------------------------------------#
# Board Mechanics
#--------------------------------------------------------------------#
#Board class
class Board:
    def __init__(self,length, height):
        self.l=length
        self.h=height
        self.b=np.array([[" "]*self.l]*self.h)

    def reset(self):
        self.b=np.array([[" "]*self.l]*self.h)

    def AddChar(self,char,cord):
        '''take a char and place it in the coordinate. Takes cord in (n,m) format'''
        self.b[cord[0],cord[1]]=char


    def printBoard(self):
        '''Prints to current board in the console.
        The following function works. Don't fuck with it!'''
        print("  ", end=' ')
        for n in range(self.l):            #print numbers on top
            print(" ",n, end=' ')

        m=0                         #row num
        for row in self.b:
            print('\n'+" "*(4*self.l+5))         #print horizontal seperator
            print('{0:2}'.format(m), end=' ')                #print row num
            m+=1
            for element in row:     #print elements
                print(" ",element, end=' ')

        print('\n')

def searchRow(row,streakLength=5,symbol='x'):
    count=0
    for n in range(len(row)):
        if row[n]==symbol:
            count+=1
        else:
            count=0
        if count==streakLength:
            return n-(streakLength-2)   #return the element of the row where the streak started, plus 1

    return 0    #if no streaks ocurred

def playerWon(player):
    global nTurn, exitFlag
    DrawText('The %s has won the game in %d turns'%(player,nTurn))

    #Wait until the player has click the board to exit
    while True:
        for event in pg.event.get():
            #check for user exit
            if event.type == pg.QUIT: 
                exitFlag = True
                return 0

            #check for user click
            if event.type == pg.MOUSEBUTTONUP:
                exitFlag = True
                return 0

playerSymbol={'Human':'x','Computer':'o'}

def detectWin():
    for player in ['Human','Computer']:
        for row in board.b:
            if searchRow(row,5,playerSymbol[player]):
                playerWon(player)
            else:
                pass

        for row in board.b.transpose():
            if searchRow(row,5,playerSymbol[player]):
                playerWon(player)
            else:
                pass
            
        #Treat diagonals
        for n in range(-board.h+1,board.l):
            if searchRow(board.b.diagonal(n),5,playerSymbol[player]):       #get diagonal element
                playerWon(player)
            else:
                pass

        #Treat the other diagnolals
        for n in range(-board.h+1,board.l):
            if searchRow(np.fliplr(board.b).diagonal(n),5,playerSymbol[player]):        #get diagonal element
                playerWon(player)
            else:
                pass

def HumanTurn():
    global exitFlag, board
    while True:
        for event in pg.event.get():
            #check for user exit
            if event.type == pg.QUIT: 
                exitFlag = True
                return 0
    
            #check for user click
            if event.type == pg.MOUSEBUTTONUP:
                userCord = (int(N*event.pos[1]/screen_size[1]), int(N*event.pos[0]/screen_size[0])) #notice that indexed are swapped to comply with n,m matrix convention
                
                if board.b[userCord] == ' ':    #check that input is valid
                    board.AddChar('x',userCord) #add an x to the board matrix
                    surf.blit(x_blob, (userCord[1]*screen_size[0]/N+offset+1, userCord[0]*screen_size[1]/N+offset+1))
                    return 0
                else:
                    pass
                    #to do: give error message to user
    
def ComputerTurn():
    compCord = AIGetMove(board,verbose)
    board.AddChar('o',compCord)
    surf.blit(o_blob, (compCord[1]*screen_size[0]/N+offset+1, compCord[0]*screen_size[1]/N+offset+1))
       

#--------------------------------------------------------------------#
# PyGame Code
#--------------------------------------------------------------------# 

# Constants for use with pygame
screen_size = (500,500)
background_color = (255,255,255)
line_color = (150, 150, 150)
x_colour = (0, 255, 0)
o_colour = (255, 0, 0)
offset = 2 #pixel offset between grid lines and colour blobs
N = 20

# Colour blobs
x_blob = pg.Surface((int(screen_size[0]/N)-2*offset-1 , int(screen_size[1]/N)-2*offset-1))
x_blob.fill(x_colour)

o_blob = pg.Surface((int(screen_size[0]/N)-2*offset-1 , int(screen_size[1]/N)-2*offset-1))
o_blob.fill(o_colour)

# Initialise the pygame window
pg.init()
pg.font.init()  #initialise font module
surf = pg.display.set_mode(screen_size)
surf.fill(background_color)

def DrawGridLines():
    # Draw grid lines
    for i in range(1,N):
        pg.draw.line(surf, line_color, (0,int(screen_size[1]*i/N)), (screen_size[0],int(screen_size[1]*i/N)), 1)
        pg.draw.line(surf, line_color, (int(screen_size[0]*i/N),0), (int(screen_size[0]*i/N),screen_size[1]), 1)

def DrawText(text):
    basicFont = pg.font.SysFont(None, 28)
    text = basicFont.render(text, True, (255, 0, 0), background_color)
    textRect = text.get_rect()
    textRect.centerx = screen_size[0]/2
    textRect.centery = (screen_size[1]*1)/5
    surf.blit(text, textRect)
    pg.display.update()

#--------------------------------------------------------------------#
# Main loop
#--------------------------------------------------------------------#
if __name__ == '__main__':
    #launch options
    if 'verbose' in argv:
        verbose = True
    else:
        verbose = False

    print('Five Row game by Martin Hayhurst Appel')
    print('Interface version:',argv[0])
    print('AI version:',AIversion)

    DrawGridLines()
    
    #Game mechanic stuff
    board = Board(N,N)  #initialise the board object
    nTurn = 0
    
    exitFlag = False

    while exitFlag == False:
        nTurn += 1
        pg.display.update()
        
        HumanTurn()
        pg.display.update()
        detectWin()
        
        sleep(0.5)
    
        ComputerTurn()
        pg.display.update()
        detectWin()
    
    
    
    pg.quit()   