import pygame as p

side=600
numbox=20
eachlen=side//numbox

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
        self.lastclick=0

    def check(self,x1,y1,click):
        global start,end,mousef,blocked,doneblock,neighbour,path
        if self.x<x1<self.x+100 and self.y<y1<self.y+40:
            self.bool=False
            if click==0 and self.lastclick==1:
                if self.st=="reset":
                    start=None
                    end=None
                    blocked=set()
                    doneblock=set()
                    neighbour=set()
                    path=set()
                    mousef=None
                elif self.st=="find path":
                    if start!=None and end!=None:
                        node=blocks[start[0]//eachlen][start[1]//eachlen]
                        node.dfs=0
                        node.dfe=distancecalc(start,end)
                        checkn(start)
                        mousef=self.st
                    else:
                        mousef=None
                else:
                    mousef=self.st
            self.lastclick=click
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

def distancecalc(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

class Point:
    def __init__(self,i,j):
        self.parent=None
        self.dfs=None
        self.dfe=None
        self.coor=(i*eachlen,j*eachlen)
    def dis(self):
        return self.dfs+self.dfe

def checkn(k):
    i,j=k
    i=i//eachlen
    j=j//eachlen
    global start,end,blocked,doneblock,neighbour,mousef,path
    doneblock.add((i*eachlen,j*eachlen))
    node=blocks[i][j]
    nodev=(i*eachlen,j*eachlen)
    allpos=[(0,1),(1,1),(-1,1),(0,-1),(1,-1),(-1,-1),(-1,0),(1,0)]
    for x,y in allpos:
        xn,yn=i+x,j+y
        if (xn*eachlen,yn*eachlen) in blocked or (xn*eachlen,yn*eachlen) in doneblock:
            continue
        elif (xn*eachlen,yn*eachlen) in neighbour:
            if node.dfs+distancecalc((xn*eachlen,yn*eachlen),nodev)<blocks[xn][yn].dfs:
                blocks[xn][yn].parent=node
                blocks[xn][yn].dfs=node.dfs+distancecalc((xn*eachlen,yn*eachlen),nodev)
        elif (xn*eachlen,yn*eachlen)==end:
            path.add(end)
            while node!=blocks[start[0]//eachlen][start[1]//eachlen]:
                path.add((node.coor))
                node=node.parent
                allrender()
            mousef=None
        else:
            if 0<=xn<numbox and 0<=yn<numbox:
                blocks[xn][yn].parent=node
                blocks[xn][yn].dfs=node.dfs+distancecalc((xn*eachlen,yn*eachlen),nodev)
                blocks[xn][yn].dfe=distancecalc((xn*eachlen,yn*eachlen),(end[0],end[1]))
                neighbour.add((xn*eachlen,yn*eachlen))


blocks=[[Point(j,i) for i in range(numbox)] for j in range(numbox)]
start=None
end=None
blocked=set()
doneblock=set()
neighbour=set()
path=set()

def draw_grid():
    for x in range(1,numbox+1):
        p.draw.line(screen,(0,0,0),(0,x*eachlen),(side,x*eachlen),2)
    for y in range(1,numbox+1):
        p.draw.line(screen,(0,0,0),(y*eachlen,0),(y*eachlen,side),2)

def allrender():
    screen.fill((255,255,255))
    for i in neighbour:
        p.draw.rect(screen,(100,200,100),[(i[0],i[1]),(eachlen,eachlen)])
    for i in doneblock:
        p.draw.rect(screen,(200,50,50),[(i[0],i[1]),(eachlen,eachlen)])
    if end!=None:
        p.draw.rect(screen,(25,200,15),[(end[0],end[1]),(eachlen,eachlen)])
    for i in path:
        p.draw.rect(screen,(25,25,200),[(i[0],i[1]),(eachlen,eachlen)])
    if start!=None:
        p.draw.rect(screen,(25,25,200),[(start[0],start[1]),(eachlen,eachlen)])
    
    for i in blocked:
        p.draw.rect(screen,(15,15,15),[(i[0],i[1]),(eachlen,eachlen)])
    draw_grid()
    for b in Bs:
        b.check(mot0,mot1,mo[0])
        b.draw_button()
    p.display.update()

mousef=None
done=False
Bs=[Button(10,610,"start point",(75,194,197),(52,132,152)),Button(120,610,"end point",(75,194,20),(52,132,30)),
    Button(230,610,"block",(200,132,132),(200,75,75)),Button(340,610,"reset",(132,132,132),(99,75,75)),Button(490,610,"find path",(200,200,30),(200,100,30))]
while not done:
    for event in p.event.get():
        if event.type==p.QUIT:
            done=True
    mo=p.mouse.get_pressed()
    mot0,mot1=p.mouse.get_pos()
    if mousef!=None and mo[0]==1 and mot1<side and mousef!="find path":
        pos=((mot0//eachlen)*eachlen,(mot1//eachlen)*eachlen)
        if start==pos or end==pos or pos in blocked:
            pass
        elif mousef=="start point":
            start=pos
        elif mousef=="end point":
            end=pos
        elif mousef=="block":
            blocked.add(pos)

    if mousef=="find path":
        min=None
        for i in neighbour:
            if min==None:
                min=i
                continue
            if blocks[min[0]//eachlen][min[1]//eachlen].dis()>blocks[i[0]//eachlen][i[1]//eachlen].dis():
                min=i
            if blocks[min[0]//eachlen][min[1]//eachlen].dis()==blocks[i[0]//eachlen][i[1]//eachlen].dis():
                if blocks[min[0]//eachlen][min[1]//eachlen].dfe>blocks[i[0]//eachlen][i[1]//eachlen].dfe:
                    min=i
        if len(neighbour)==0:
            mousef=None
        else:
            neighbour.remove(min)
            checkn(min)

    allrender()
p.quit()