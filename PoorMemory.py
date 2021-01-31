import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOARDSIZE = 8
BOXSIZE = 40
GAPSIZE = 10
REVEALSPEED = 8

GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGIMAGE = 'Images/背景.jpg'
AFEI = 'Images/阿飞.bmp'
AKAI = 'Images/阿凯.bmp'
AI = 'Images/艾.bmp'
BAN = 'Images/斑.bmp'
CHUTIAN = 'Images/雏田.bmp'
YING = 'Images/春野樱.bmp'
DASHEWAN = 'Images/大蛇丸.bmp'
DAYEMU = 'Images/大野木.bmp'
DAITU = 'Images/带土.bmp'
DIDALA = 'Images/迪达拉.bmp'
DINGCI = 'Images/丁次.bmp'
FEIDUAN = 'Images/飞段.bmp'
FEIJIAN = 'Images/扉间.bmp'
GANGSHOU = 'Images/纲手.bmp'
GUIJIAO = 'Images/鬼鲛.bmp'
HUIYE = 'Images/辉夜.bmp'
JIAODU = 'Images/角都.bmp'
JINGYE = 'Images/井野.bmp'
JIUXINNAI = 'Images/玖辛奈.bmp'
KAKAXI = 'Images/卡卡西.bmp'
LIUDAO = 'Images/六道仙人.bmp'
LUWAN = 'Images/鹿丸.bmp'
LUOKELI = 'Images/洛克李.bmp'
MINGREN = 'Images/鸣人.bmp'
PEIEN = 'Images/佩恩.bmp'
QILABI = 'Images/奇拉比.bmp'
QUANZHONGYA = 'Images/犬冢牙.bmp'
RIZHAN = 'Images/日斩.bmp'
SHOUJU = 'Images/手鞠.bmp'
SHUIMEN = 'Images/水门.bmp'
TIANTIAN = 'Images/天天.bmp'
WOAILUO = 'Images/我爱罗.bmp'
XIAONAN = 'Images/小南.bmp'
XIE = 'Images/蝎.bmp'
YOU = 'Images/鼬.bmp'
ZHAOMEIMING = 'Images/照美冥.bmp'
ZHINAI = 'Images/志乃.bmp'
ZHUJIAN = 'Images/柱间.bmp'
ZILAIYE = 'Images/自来也.bmp'
ZUOJING = 'Images/佐井.bmp'

BOXIMAGE = pygame.transform.scale(pygame.image.load('Images/coverage.bmp'), (BOXSIZE, BOXSIZE))
HIGHLIGHTCOLOR = ORANGE


ALLHEROS = (AFEI, AKAI, AI, BAN, CHUTIAN, YING, DASHEWAN, DAYEMU, DAITU, DIDALA, DINGCI, FEIDUAN, FEIJIAN,
                        GANGSHOU, GUIJIAO, HUIYE, JIAODU, JINGYE, JIUXINNAI, KAKAXI, LIUDAO, LUWAN, LUOKELI, MINGREN, PEIEN, QILABI,
                        QUANZHONGYA, RIZHAN, SHOUJU, SHUIMEN, TIANTIAN, WOAILUO, XIAONAN, XIE, YOU, ZHAOMEIMING, ZHINAI,
                        ZHUJIAN, ZILAIYE, ZUOJING)

def main():
    global FPSCLOCK, DISPLAYSURF, BACKGROUND, xmargin, ymargin, boardsize, revealspeed
    boardsize = 2
    xmargin = int((WINDOWWIDTH - (boardsize * (BOXSIZE + GAPSIZE))) / 2)
    ymargin = int((WINDOWHEIGHT - (boardsize * (BOXSIZE + GAPSIZE))) / 2)
    revealspeed = int(boardsize / 2)
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    mousex = 0
    mousey = 0
    pygame.display.set_caption('Show Me Your Poor Memory~')
    music = pygame.mixer.Sound('music/高梨康治 - 動天.wav')
    music.play()
    BACKGROUND = pygame.transform.scale(pygame.image.load(BGIMAGE), (WINDOWWIDTH, WINDOWHEIGHT))
    
    mainBoard = getRandomizedBoard(boardsize)
    revealedBoxes = generateRevealedBoxesData(False, boardsize)
    DISPLAYSURF.blit(BACKGROUND, (0, 0))
    startGameAnimation(mainBoard, boardsize, revealspeed, xmargin, ymargin)
    
    firstSelection = None 
    while True:
        mouseClicked = False
        drawBoard(mainBoard, revealedBoxes, boardsize, xmargin, ymargin)
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey, boardsize, xmargin, ymargin)
        if boxx != None and boxy != None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy, xmargin, ymargin)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)], revealspeed)
                revealedBoxes[boxx][boxy] = True
                if firstSelection == None: 
                    firstSelection = (boxx, boxy)
                else:
                    hero1 = getHero(mainBoard, firstSelection[0], firstSelection[1])
                    hero2 = getHero(mainBoard, boxx, boxy)

                    if hero1 != hero2:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)], revealspeed)
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        result = gameWonAnimation(mainBoard, boardsize, xmargin, ymargin)
                        if result == 'solved':
                            if(boardsize==BOARDSIZE): boardsize=2
                            else: boardsize = boardsize + 2
                            xmargin = int((WINDOWWIDTH - (boardsize * (BOXSIZE + GAPSIZE))) / 2)
                            ymargin = int((WINDOWHEIGHT - (boardsize * (BOXSIZE + GAPSIZE))) / 2)
                            revealspeed = int(boardsize / 2)
                            mainBoard = getRandomizedBoard(boardsize)
                            revealedBoxes = generateRevealedBoxesData(False, boardsize)

                            drawBoard(mainBoard, revealedBoxes, boardsize, xmargin, ymargin)
                            pygame.display.update()
                            pygame.time.wait(1000)

                            startGameAnimation(mainBoard, boardsize, revealspeed, xmargin, ymargin)
                    firstSelection = None 

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def getRandomizedBoard(boardsize):
    icons = list(ALLHEROS)
    random.shuffle(icons)
    numIconsUsed = int(boardsize * boardsize / 2)
    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)
    board = []
    for x in range(boardsize):
        column = []
        for y in range(boardsize):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board
def generateRevealedBoxesData(v, boardsize):
    revealedBoxes = []
    for i in range(boardsize):
        revealedBoxes.append([v] * boardsize)
    return revealedBoxes
def startGameAnimation(board, boardsize, revealspeed, xmargin, ymargin):
    coveredBoxes = generateRevealedBoxesData(False, boardsize)
    boxes = []
    for x in range(boardsize):
        for y in range(boardsize):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(revealspeed, boxes)
    drawBoard(board, coveredBoxes, boardsize, xmargin, ymargin)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup, revealspeed)
        coverBoxesAnimation(board, boxGroup, revealspeed)
def splitIntoGroupsOf(groupNum, group):
    groups = []
    for i in range(0, len(group), groupNum):
        groups.append(group[i:i+groupNum])
    return groups
def drawBoard(board, coveredBoxes, boardsize, xmargin, ymargin):
    DISPLAYSURF.blit(BACKGROUND, (0, 0))
    for boxx in range(boardsize):
        for boxy in range(boardsize):
            left, top = leftTopCoordsOfBox(boxx, boxy, xmargin, ymargin)
            if not coveredBoxes[boxx][boxy]:
                DISPLAYSURF.blit(BOXIMAGE, (left, top))
            else:
                hero = getHero(board, boxx, boxy)
                drawIcon(hero, left, top)
def leftTopCoordsOfBox(boxx, boxy, xmargin, ymargin):
    left = boxx * (BOXSIZE+GAPSIZE) + xmargin
    top = boxy * (BOXSIZE+GAPSIZE) + ymargin
    return (left, top)
def getHero(board, boxx, boxy):
    hero = board[boxx][boxy]
    return hero
def drawIcon(hero, left, top):
    hero = pygame.transform.scale(pygame.image.load(hero), (BOXSIZE, BOXSIZE))
    DISPLAYSURF.blit(hero, (left, top))
def revealBoxesAnimation(board, boxesToReveal, revealspeed):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage, xmargin, ymargin)
def coverBoxesAnimation(board, boxesToCover, revealspeed):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage, xmargin, ymargin)
def drawBoxCovers(board, boxes, coverage, xmargin, ymargin):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1], xmargin, ymargin)
        DISPLAYSURF.blit(BOXIMAGE, (left, top))
        hero = getHero(board, box[0], box[1])
        drawIcon(hero, left, top)
        if coverage > 0:
            part = pygame.transform.scale(BOXIMAGE, (coverage, BOXSIZE))
            DISPLAYSURF.blit(part, (left, top))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
def getBoxAtPixel(x, y, boardsize, xmargin, ymargin):
    for boxx in range(boardsize):
        for boxy in range(boardsize):
            left, top = leftTopCoordsOfBox(boxx, boxy, xmargin, ymargin)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)
def drawHighlightBox(boxx, boxy, xmargin, ymargin):
    left, top = leftTopCoordsOfBox(boxx, boxy, xmargin, ymargin)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)
def gameWonAnimation(board, boardsize, xmargin, ymargin):
    coveredBoxes = generateRevealedBoxesData(True, boardsize)
    DISPLAYSURF.blit(BACKGROUND, (0, 0))
    drawBoard(board, coveredBoxes, boardsize, xmargin, ymargin)

    imageSolved = pygame.image.load('Images/solved.png')
    solvedRect = imageSolved.get_rect()
    solvedRect.center = (0.5*WINDOWWIDTH, 0.5*WINDOWHEIGHT)
    DISPLAYSURF.blit(imageSolved, solvedRect)
    
    pygame.display.update()
    pygame.time.wait(300)
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                return 'solved'
        
def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True

if __name__ == '__main__':
    main()
    input()
