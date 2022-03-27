from math import ceil
from tabnanny import check
from tkinter.tix import CELL
import pygame, sys
from pygame.locals import *
import time
pygame.init()
X=600
Y=650
green=(0,200,0)
blue=(69, 138, 247)
white=(255,255,255)
black = (0,0,0)
red = (255,0,0)
font = pygame.font.Font('freesansbold.ttf', 32)
font_small = pygame.font.Font('freesansbold.ttf', 24)
FBS = 60
score = [0,0]
color=red
counter =0
board =  [['n','n','n','n'],
          ['n','n','n','n'],
          ['n','n','n','n'],
          ['n','n','n','n'],]
display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption('SOS_Game')
display_surface.fill(white)
clock=pygame.time.Clock()


class btn():
    def __init__(self,x,y,C_i,C_j,w=98,h=98):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.i=C_i
        self.j=C_j
        self.rect=None
        self.clicked = False
        self.font = pygame.font.Font('freesansbold.ttf', 32)     

    def draw(self , b=2):
        self.rect = pygame.draw.rect(display_surface,color,pygame.Rect(self.x,self.y,self.w,self.h),b)
  
    def add_text(self,text,c = color , t_c = white):
        t = font.render(text, True, c,t_c)
        t_rect = t .get_rect()
        t_rect.center=(self.x+self.w//2,self.y+self.h//2)
        display_surface.blit(t, t_rect)

    def btn_board(self):
        global color,counter
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if event.type == pygame.MOUSEBUTTONDOWN and not self.clicked:
                if(event.button in [1,3]):
                    if event.button ==1:
                        self.clicked = True
                        self.add_text("S",c=black)
                        if counter%2==0:
                            color=blue
                        else:
                            color=red
                        board[self.i][self.j]="S"
                    elif event.button ==3:
                        self.clicked = True
                        self.add_text("O",c=black)
                        if counter%2==0:
                            color=blue
                        else:
                            color=red
                        board[self.i][self.j]="O"
                    score[counter%2]+=check_win(self.i,self.j)
                    counter+=1
                    re_draw_game()
            
def build_board():
    rects = []
    for i in range(4):
        for j in range(4):
            rects.append(btn(100+100*j,120+100*i,C_i=i,C_j=j))
    return rects
blocks = build_board()
def draw_board(rects):
    for r in rects:
        r.draw()

def catch_clicks(rects):
    for r in rects:
        r.btn_board()

def btns(exit,retry):
    pos = pygame.mouse.get_pos()
    if exit.collidepoint(pos):
        if event.type == pygame.MOUSEBUTTONDOWN :
            if(event.button == 1):
                pygame.quit()
                sys.exit()
    if retry.collidepoint(pos):
        global board,color,score,counter,blocks
        if event.type == pygame.MOUSEBUTTONDOWN :
            if(event.button== 1):
                score = [0,0]
                color=red
                counter =0
                board = [['n','n','n','n'],
                        ['n','n','n','n'],
                        ['n','n','n','n'],
                        ['n','n','n','n'],]
                
                blocks = build_board()
                display_surface.fill(white)
                one_time()
                re_draw_game()
                time.sleep(0.2)
                
def re_draw_game():
    global counter,color
    if(counter >15):
        display_surface.fill(white)
        if(score[0]>score[1]):
            color=red
            text = font.render('Player_1 Win', True, red)
            textRect = text.get_rect()
            textRect.center = (X // 2, 100)
            display_surface.blit(text, textRect)
        elif(score[0]<score[1]):
            color=blue
            text = font.render('Player_2 Win', True, blue)
            textRect = text.get_rect()
            textRect.center = (X // 2, 100)
            display_surface.blit(text, textRect)
        else:
            text = font.render('Draw', True, black)
            textRect = text.get_rect()
            textRect.center = (X // 2, 100)
            display_surface.blit(text, textRect)
        exit = pygame.draw.rect(display_surface,color,pygame.Rect(100,300,150,50),2)
        retry = pygame.draw.rect(display_surface,color,pygame.Rect(350,300,150,50),2)
        t = font.render("Exit", True, color)
        t_rect = t .get_rect()
        t_rect.center=(175,325)
        display_surface.blit(t, t_rect)
        t = font.render("retry", True, color)
        t_rect = t .get_rect()
        t_rect.center=(425,325)
        display_surface.blit(t, t_rect) 
        btns(exit,retry)
    else:
        text = font_small.render('Player_'+str(counter%2+1)+" turn", True, color, white)
        textRect = text.get_rect()
        textRect.center = (175, 95)
        display_surface.blit(text, textRect)
        text = font.render(str(score[0]), True, red,white)
        textRect = text.get_rect()
        textRect.center = (175, 600)
        display_surface.blit(text, textRect)

        text = font.render(str(score[1]), True, blue,white)
        textRect = text.get_rect()
        textRect.center = (600-175, 600)
        display_surface.blit(text, textRect)
        draw_board(blocks)
    text = font.render('SOS_Game', True, color)
    textRect = text.get_rect()
    textRect.center = (X // 2, 20)
    display_surface.blit(text, textRect)

def check_line(x,y,H_or_V):
    word = "SOS"
    gain_points=0
    i=0
    ind = 0
    start= False
    include_it = False
    while i <4:
        if H_or_V == "H":
            cell =board[x][i]
            check_cell = y
        else:
            cell =board[i][y]
            check_cell = x
        if(cell==word[ind]):
            if i==check_cell:
                include_it=True
            ind+=1
            start =True
        else:
            include_it=False
            ind=0
            if start:
                i-=1
                start=False
        if ind>=3 :
            if include_it:
                gain_points+=1
            break
        i+=1    
    return gain_points

def check_diag(x,y,start_x,start_y,L_or_R):
    ind = 0
    word="SOS"
    start= False
    include_it = False
    gain_points=0
    if L_or_R=="L":
        cond =start_x<4 and start_y<4
        inc_x = 1
        inc_y = 1
    else:
        inc_x=1
        inc_y=-1
        cond = start_x<4 and start_y>=0
    while cond:
        if(board[start_x][start_y]==word[ind]):
            if start_x==x and start_y==y:
                include_it=True
            ind+=1
            start =True
        else:
            include_it=False
            ind=0
            if start:
                start_x-=-inc_x
                start_y-=-inc_y
                start=False
        if ind>=3 :
            if include_it:
                gain_points+=1
            break
        start_x+=inc_x
        start_y+=inc_y
        if L_or_R=="L":
            cond =start_x<4 and start_y<4
        else:
            cond = start_x<4 and start_y>=0
    return gain_points

def check_win(x,y):
    word = "SOS"
    gain_points=0
    # horizintal
    gain_points += check_line (x,y,"H")
    # vertical
    gain_points += check_line (x,y,"V")
    #left diagonal
    start_x =x
    start_y =y
    while start_x!=0 and start_y!=0:
        start_x-=1
        start_y-=1
    gain_points +=check_diag(x,y,start_x,start_y,"L")
    #right diagonal
    start_x =x
    start_y =y
    while start_x>0 and start_y<3:
        start_x-=1
        start_y+=1
    gain_points +=check_diag(x,y,start_x,start_y,"R")
    return gain_points

def one_time():
    text = font_small.render("Player_1 Score", True, red, white)
    textRect = text.get_rect()
    textRect.center = (175, 550)
    display_surface.blit(text, textRect)
    text = font_small.render("Player_2 Score", True, blue, white)
    textRect = text.get_rect()
    textRect.center = (600-175, 550)
    display_surface.blit(text, textRect)
one_time()
re_draw_game()
while True: # main game loop
    clock.tick(FBS-30)
    
    if counter>15:
        re_draw_game()
    else:
        catch_clicks(blocks)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

