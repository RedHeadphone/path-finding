import pygame as p
import cv2, sys


class Button:
    def __init__(self, x, y, st, c1, c2):
        global side
        mulfac = side/600
        self.x = x*mulfac
        self.y = side + 60 - y
        self.cx = self.x + 50*mulfac
        self.cy =  self.y + 20
        self.width = 100*mulfac
        self.height = 40
        self.bool = True
        self.st = st
        self.color1 = c1
        self.color2 = c2
        self.lastclick = 0

    def checkclick(self, x1, y1, click):
        global start, end, mousef, blocked, doneblock, neighbour, path, foundpath, stopshowingneighbour
        if self.x < x1 < self.x + 100 and self.y < y1 < self.y + 40:
            self.bool = False
            if click == 0 and self.lastclick == 1:
                if self.st == "reset":
                    start = None
                    end = None
                    blocked = set()
                    doneblock = set()
                    neighbour = set()
                    path = set()
                    mousef = None
                    foundpath = False
                    stopshowingneighbour = False
                elif self.st == "find path":
                    if start != None and end != None:
                        node = blocks[start[0]][start[1]]
                        node.dfs = 0
                        node.dfe = distancecalc(start, end)
                        checkneighbour(start)
                        mousef = self.st
                    else:
                        mousef = None
                else:
                    mousef = self.st
            self.lastclick = click
        else:
            self.bool = True

    def draw_button(self):
        if self.bool:
            c1 = self.color1
            c2 = self.color2
        else:
            c2 = self.color1
            c1 = self.color2
        font = p.font.Font("freesansbold.ttf", 18)
        text = font.render(self.st, True, c1)
        txt_w, txt_h = text.get_size()
        text = p.transform.smoothscale(text, (txt_w * self.width // 100, txt_h * self.height // 40))
        textRect = text.get_rect()
        textRect.center = (self.cx,self.cy)
        p.draw.rect(screen, c2, [( self.x ,self.y), (self.width, self.height)])
        screen.blit(text, textRect)


def distancecalc(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


class Point:
    def __init__(self, i, j):
        self.parent = None
        self.dfs = None
        self.dfe = None
        self.coor = (i, j)

    def dis(self):
        return self.dfs + self.dfe


def checkneighbour(k):
    i, j = k
    global start, end, blocked, doneblock, neighbour, mousef, path, cangodiagonally, foundpath
    doneblock.add((i, j))
    node = blocks[i][j]
    nodev = (i, j)
    allpos = [
        (0, 1),
        (0, -1),
        (-1, 0),
        (1, 0),
    ]
    if cangodiagonally:
        allpos.extend([(1, 1), (-1, 1), (1, -1), (-1, -1)])
    for x, y in allpos:
        xn, yn = i + x, j + y
        if (xn, yn) in blocked or (
            xn,
            yn,
        ) in doneblock:
            continue
        elif (xn, yn) in neighbour:
            if node.dfs + distancecalc((xn, yn), nodev) < blocks[xn][yn].dfs:
                blocks[xn][yn].parent = node
                blocks[xn][yn].dfs = node.dfs + distancecalc((xn, yn), nodev)
        elif (xn, yn) == end:
            path.add(end)
            ctr2 = 0
            foundpath = True
            while node != blocks[start[0]][start[1]]:
                path.add((node.coor))
                node = node.parent
                ctr2 += 1
                if ctr2 == int(skipframes * 0.7):
                    ctr2 = 0
                    allrender()
            mousef = None
        else:
            if 0 <= xn < numbox and 0 <= yn < numbox:
                blocks[xn][yn].parent = node
                blocks[xn][yn].dfs = node.dfs + distancecalc((xn, yn), nodev)
                blocks[xn][yn].dfe = distancecalc((xn, yn), (end[0], end[1]))
                neighbour.add((xn, yn))


side = 600
numbox = 100
cangodiagonally = True
foundpath = False
stopshowingneighbour = False
skipframes = 5
countertorefresh = 0
gridlinewidth = 1
thresholdvalue = 100
start = None
end = None
blocked = set()
doneblock = set()
neighbour = set()
path = set()

if len(sys.argv) > 1:
    main = cv2.imread(sys.argv[1], 0)
    img = cv2.resize(main, (numbox, numbox))
    img[img > thresholdvalue] = 255
    img[img <= thresholdvalue] = 0

    def renderimage():
        global img, main, numbox, thresholdvalue
        img = cv2.resize(main, (numbox, numbox))
        img[img > thresholdvalue] = 255
        img[img <= thresholdvalue] = 0
        cv2.imshow("image preview", cv2.resize(img, (500, 500)))

    def on_trackbar(val):
        global numbox
        if val == 0:
            return
        numbox = val
        renderimage()

    def on_trackbar2(val):
        global thresholdvalue
        thresholdvalue = (val * 255) // 1000
        renderimage()

    cv2.imshow("image preview", cv2.resize(img, (500, 500)))
    cv2.namedWindow("image settings", cv2.WINDOW_NORMAL)
    cv2.createTrackbar("size", "image settings", numbox, 200, on_trackbar)
    cv2.createTrackbar(
        "threshold",
        "image settings",
        (thresholdvalue * 1000) // 255,
        1000,
        on_trackbar2,
    )

    cv2.waitKey()
    cv2.destroyAllWindows()

    eachlen = side // numbox
    side = eachlen * numbox
    
    gridlinewidth = 0
    for i in range(numbox):
        for j in range(numbox):
            if img[i][j] == 0:
                blocked.add((j, i))

    skipframes = 50
    blocks = [[Point(j, i) for i in range(numbox)] for j in range(numbox)]
else:
    numbox = 50
    eachlen = side // numbox
    blocks = [[Point(j, i) for i in range(numbox)] for j in range(numbox)]


p.init()
screen = p.display.set_mode((side, side + 60))
p.display.set_caption("Path Finding")


def draw_grid():
    for x in range(1, numbox + 1):
        p.draw.line(
            screen, (0, 0, 0), (0, x * eachlen), (side, x * eachlen), gridlinewidth
        )
    for y in range(1, numbox + 1):
        p.draw.line(
            screen, (0, 0, 0), (y * eachlen, 0), (y * eachlen, side), gridlinewidth
        )


def allrender(skip=False):
    screen.fill((255, 255, 255))
    if not skip:
        for i in neighbour:
            p.draw.rect(
                screen,
                (100, 200, 100),
                [(i[0] * eachlen, i[1] * eachlen), (eachlen, eachlen)],
            )
        for i in doneblock:
            p.draw.rect(
                screen,
                (200, 50, 50),
                [(i[0] * eachlen, i[1] * eachlen), (eachlen, eachlen)],
            )
    if end != None:
        p.draw.rect(
            screen,
            (25, 200, 15),
            [(end[0] * eachlen, end[1] * eachlen), (eachlen, eachlen)],
        )
    for i in path:
        p.draw.rect(
            screen,
            (25, 25, 200),
            [(i[0] * eachlen, i[1] * eachlen), (eachlen, eachlen)],
        )
    if start != None:
        p.draw.rect(
            screen,
            (25, 25, 200),
            [(start[0] * eachlen, start[1] * eachlen), (eachlen, eachlen)],
        )

    for i in blocked:
        p.draw.rect(
            screen, (15, 15, 15), [(i[0] * eachlen, i[1] * eachlen), (eachlen, eachlen)]
        )
    if gridlinewidth > 0:
        draw_grid()
    for b in Bs:
        b.checkclick(mot0, mot1, mo[0])
        b.draw_button()
    p.display.update()


mousef = None
done = False
Bs = [
    Button(10, 50, "start point", (75, 194, 197), (52, 132, 152)),
    Button(120, 50, "end point", (75, 194, 20), (52, 132, 30)),
    Button(230, 50, "block", (200, 132, 132), (200, 75, 75)),
    Button(340, 50, "reset", (132, 132, 132), (99, 75, 75)),
    Button(490, 50, "find path", (200, 200, 30), (200, 100, 30)),
]

while not done:
    for event in p.event.get():
        if event.type == p.QUIT:
            done = True
    mo = p.mouse.get_pressed()
    mot0, mot1 = p.mouse.get_pos()
    pos = ( int(mot0 // eachlen), int(mot1 // eachlen))
    if (
        mousef != None
        and mo[0] == 1
        and mot1 < side
        and mousef != "find path"
        and not foundpath
    ):
        if start == pos or end == pos or pos in blocked:
            pass
        elif mousef == "start point":
            start = pos
        elif mousef == "end point":
            end = pos
        elif mousef == "block":
            blocked.add(pos)
    elif (
        mousef != None
        and mo[2] == 1
        and mot1 < side
        and mousef != "find path"
        and not foundpath
    ):
        if mousef == "block" and pos in blocked:
            blocked.remove(pos)
    if foundpath and mo[0] == 1 and mot1 < side:
        stopshowingneighbour = True

    if mousef == "find path" and not foundpath:
        min = None
        for i in neighbour:
            if min == None:
                min = i
                continue
            if blocks[min[0]][min[1]].dis() > blocks[i[0]][i[1]].dis():
                min = i
            if blocks[min[0]][min[1]].dis() == blocks[i[0]][i[1]].dis():
                if blocks[min[0]][min[1]].dfe > blocks[i[0]][i[1]].dfe:
                    min = i
        if len(neighbour) == 0:
            mousef = None
        else:
            neighbour.remove(min)
            checkneighbour(min)
    countertorefresh += 1
    if countertorefresh == skipframes:
        countertorefresh = 0
        allrender(stopshowingneighbour)
p.quit()
