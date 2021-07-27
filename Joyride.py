import pygame
import random

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
clock = pygame.time.Clock()
font = pygame.font.SysFont('dungeon', 30)

# variables
rungame = True
gameactive = True
zaplist = []
charlist = []
charmovement = 0
gravity = 0.2
floorx = 0
labx = 0
coinx = 0
coinlist = []
coinscore = 0
index = 0
score = 0
highscore = 0

# display
dis = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Daman')

# objects
sound = pygame.mixer.music.load('E:/Music/Jetpack Joyride OST _musical_score__musical_keyboard_ - Main Theme ( 256kbps cbr ).mp3')
pygame.mixer.music.play(-1, 0.0, 0)
lab = pygame.image.load('lab4c.jpg').convert()
lab = pygame.transform.scale(lab, (2372, 580))
floor = pygame.image.load('floor.jpg').convert()
floor = pygame.transform.scale(floor, (2160, 198))
char1 = pygame.image.load('char1.png').convert_alpha()
char1 = pygame.transform.scale(char1, (170, 170))
char2 = pygame.image.load('char2.png').convert_alpha()
char2 = pygame.transform.scale(char2, (170, 170))
char3 = pygame.image.load('char3.png').convert_alpha()
char3 = pygame.transform.scale(char3, (170, 170))
char4 = pygame.image.load('char4.png').convert_alpha()
char4 = pygame.transform.scale(char4, (170, 170))
char5 = pygame.image.load('char5.png').convert_alpha()
char5 = pygame.transform.scale(char5, (170, 170))
char6 = pygame.image.load('char6.png').convert_alpha()
char6 = pygame.transform.scale(char6, (170, 170))
char7 = pygame.image.load('char7.png').convert_alpha()
char7 = pygame.transform.scale(char7, (170, 170))
char8 = pygame.image.load('char8.png').convert_alpha()
char8 = pygame.transform.scale(char8, (170, 170))
retry = pygame.image.load('retry.png').convert_alpha()
retry = pygame.transform.scale(retry, (375*2, 118*2))
coin = pygame.image.load('coins.png').convert_alpha()
coin = pygame.transform.scale(coin, (int(1920/3.5), int(720/4)))
SPAWNCOIN = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWNCOIN, 9000)
coinRect = coin.get_rect()
zap = pygame.image.load('zap.png').convert_alpha()
zap = pygame.transform.scale(zap, (100, 250))
zap = pygame.transform.rotate(zap, 45)
SPAWNZAP = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNZAP, 1500)

charframes = [char1, char2, char3, char4, char5, char6, char7, char8]
char = charframes[index]
charRect = char.get_rect(center=(200, 100))
CHARSWAP = pygame.USEREVENT
pygame.time.set_timer(CHARSWAP, 100)

# functions
def createcoins():
    ran = random.randrange(0, 500)
    coi = coin.get_rect(midtop=(2000, ran))
    return coi

def movecoins(coi):
    for i in coi:
        i.centerx -= 5
    return coi

def drawcoins(coi):
    for i in coi:
        dis.blit(coin, i)

def movelab():
    dis.blit(lab, (labx, 0))
    dis.blit(lab, (labx + 2372, 0))

def movefloor():
    dis.blit(floor, (floorx, 580))
    dis.blit(floor, (floorx + 2160, 580))

def animation():
    newchar = charframes[index]
    newRect = newchar.get_rect(center=(200, charRect.centery))
    return newchar, newRect

def scores(fine, fines):
    fine = font.render('Distance: ' + str(int(score)) + 'm', True, (255, 255, 255))
    dis.blit(fine, (10, 10))
    fines = font.render('Coins: ' + str(int(coinscore)), True, (255, 255, 255))
    dis.blit(fines, (10, 40))

def createzap():
    ran = random.randrange(10, 450)
    zap1 = zap.get_rect(midtop=(1350, ran))
    return zap1, zap1

def movezap(zaps):
    for i in zaps:
        i.centerx -= 5
        if score >= 100:
            i.centerx -= 0.1
        if score >= 1000:
            i.centerx -= 0.2
    return zaps

def drawzap(zaps):
    for i in zaps:
        dis.blit(zap, i)

def coilide(coi):
    for i in coi:
        if charRect.colliderect(i):
            return False
    return True

def collide(zaps):
    for i in zaps:
        #if charRect.colliderect(i):
        #if (i.centerx <= 285 and i.centerx >= 115) and (charRect.bottom < i.top and charRect.top > i.bottom):
        if charRect.collidepoint(i.center):
            return False
    return True

while rungame:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rungame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                pygame.mixer.music.pause()
            if event.key == pygame.K_n:
                pygame.mixer.music.unpause()
            if event.key == pygame.K_SPACE:
                charmovement = 0
                charmovement -= 10
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameactive == False:
                gameactive = True
                charlist.clear()
                zaplist.clear()
                coinlist.clear()
                charRect.center = (200, 500)
                charmovement = 0
        if event.type == SPAWNCOIN:
            coinlist.append(createcoins())
        if event.type == SPAWNZAP:
            zaplist.extend(createzap())
        if event.type == CHARSWAP:
            if index < 7:
                index += 1
            else:
                index = 0
            char, charRect = animation()

    floorx -= 3
    labx -= 1

    if gameactive:
        if score >= 100:
            floorx -= 0.1
            labx -= 0.1
        if score >= 500:
            floorx -= 0.2
            labx -= 0.2
        if score >= 1000:
            floorx -= 0.3
            labx -= 0.3
        if score >= 2000:
            floorx -= 0.5
            labx -= 0.5
        movelab()
        if labx <= -2372:
            labx = 0
        movefloor()
        charmovement += gravity
        charRect.centery += charmovement
        coinlist = movecoins(coinlist)
        drawcoins(coinlist)
        zaplist = movezap(zaplist)
        drawzap(zaplist)
        if floorx <= -2160:
            floorx = 0
        if charRect.bottom >= 660:
            charRect.bottom = 660
        if charRect.top <= 0:
            charRect.top = 0
        gameactive = collide(zaplist)
        if coilide(coinlist) is False:
            coinscore += 0.15
        dis.blit(char, (charRect))
        scores(score, coinscore)
    else:
        if highscore < score:
            highscore = score
        score = 0
        coinscore = 0
        highscores = font.render('Highscore: ' + str(int(highscore)) + 'm', True, (255, 255, 255))
        dis.blit(highscores, (500, 20))
        dis.blit(retry, (265, 250))
        hit = font.render('H I T   S P A C E B A R', True, (255, 255, 255))
        dis.blit(hit, (450, 600))
    score += 0.15

    pygame.display.update()
    clock.tick(120)

pygame.quit()
quit()
