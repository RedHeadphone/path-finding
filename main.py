import pygame as p

side=600
numbox=20

p.init()
screen=p.display.set_mode((side,side+60))
p.display.set_caption("Path Finding")

class Button:
    def __init__(self,x,y,st,c1,c2):
        self.x=x
        self.y=y
        self.bool=True
        self.st=st
        self.color1=c1
        self.color2=c2

    def check(self,x1,y1,click):
        if self.x<x1<self.x+100 and self.y<y1<self.y+40:
            self.bool=False
            if click==1:
                print(self.st+" pressed")
        else :
            self.bool=True
    def draw_button(self):
        if self.bool:
            c1=self.color1
            c2=self.color2
        else :
            c2=self.color1
            c1=self.color2
        font = p.font.Font('freesansbold.ttf',18)
        text = font.render(self.st, True, c1) 
        textRect = text.get_rect()
        textRect.center = (self.x+50, self.y+20)
        p.draw.rect(screen,c2,[(self.x,self.y),(100,40)])
        screen.blit(text, textRect)

class Point:
    def __init__(self):
        self.parent=None
        self.dfs=None
        self.dfe=None
        self.isblocked=False

blocks=[[Point() for i in range(20)] for i in range(20)]

def draw_grid():
    eachlen=side//numbox
    for x in range(1,numbox+1):
        p.draw.line(screen,(0,0,0),(0,x*eachlen),(side,x*eachlen),2)
    for y in range(1,numbox+1):
        p.draw.line(screen,(0,0,0),(y*eachlen,0),(y*eachlen,side),2)

done=False
Bs=[Button(10,610,"start point",(75,194,197),(52,132,152)),Button(120,610,"end point",(75,194,20),(52,132,30)),
    Button(230,610,"block",(200,132,132),(200,75,75)),Button(490,610,"find path",(200,200,30),(200,100,30))]
while not done:
    for event in p.event.get():
        if event.type==p.QUIT:
            done=True
    mo=p.mouse.get_pressed()
    mot0,mot1=p.mouse.get_pos()
    screen.fill((255,255,255))
    draw_grid()
    for b in Bs:
        b.check(mot0,mot1,mo[0])
        b.draw_button()
    p.display.update()
p.quit()