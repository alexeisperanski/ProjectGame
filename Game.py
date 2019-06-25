import pygame
import random
from time import time

pygame.init()
# размеры окна
xdis = 500
ydis = 500
# размеры карты
pointmax = 1500
pointmin = 0
# край карты
xusl = 0


win = pygame.display.set_mode((xdis,ydis)) #размеры окна
pygame.display.set_caption("Project Game") #название окна

# Параметры персонажа
pwidth = 60 #высота
pheight = 71 #ширина
speed = 5 #скорость
lastMove = "right" #направление движения


# расположение по x and y
player_x = 50
player_y = ydis - pheight - 100

# пол карты
constpol = ydis - 10
pol = constpol

# Обозначения наличия движения по y
isJump = False
jumpCount = 0
y_speed = 0
left = False
right = False
speed_r = speed_l = speed #скорости движения вправо, влево
animCount = 0

# Блоки препядствия
blocks = []
Bl = 10
startx = 200


#  прорисовка походов влево, вправо, на месте и задний фон
walkRight = [pygame.image.load('ImageGame/pygame_right_1.png'), pygame.image.load('ImageGame/pygame_right_2.png'),
             pygame.image.load('ImageGame/pygame_right_3.png'),pygame.image.load('ImageGame/pygame_right_4.png'),
             pygame.image.load('ImageGame/pygame_right_5.png'),pygame.image.load('ImageGame/pygame_right_6.png'),]

walkLeft = [pygame.image.load('ImageGame/pygame_left_1.png'), pygame.image.load('ImageGame/pygame_left_2.png'),
             pygame.image.load('ImageGame/pygame_left_3.png'),pygame.image.load('ImageGame/pygame_left_4.png'),
             pygame.image.load('ImageGame/pygame_left_5.png'),pygame.image.load('ImageGame/pygame_left_6.png'),]

playerStand = pygame.image.load('ImageGame/pygame_idle.png')

bg = pygame.image.load('ImageGame/pygame_bg.jpg')

clock = pygame.time.Clock()

class bullet():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8*facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class Block():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win, xusl):
        pygame.draw.rect(win, self.color, (self.x - xusl, self.y, self.width, self.height))

# создание препядствия
def createBlock(x):
    y = ydis - random.randint(30, 300)
    return(Block(random.randint(x, x+100), y, random.randint(10, 100), random.randint(30, y), (0, 200, 64)))

# проверка на влезание в блок
def blockin(x,y,bl:Block):
    pass

def newPol():
    x = player_x + xusl
    maxy = constpol
    for bl in blocks:
        if ((x + pwidth//2) > bl.x) and ((x + pwidth//2) < (bl.x + bl.width)):
            if (player_y + pheight) <= (bl.y + 5):
                if bl.y < maxy:
                    maxy = bl.y
    return maxy

def nowPol(pol):
    global player_x
    global player_y
    global y_speed
    x = player_x + xusl
    y_foot = player_y + pheight
    for bl in blocks:
        if x + pwidth > bl.x and x < bl.x + bl.width: #попадает по x
            # player_x = 100
            if y_foot > bl.y and player_y < bl.y + bl.height:# попадает по y
                if x + pwidth < bl.x + 7: # левее
                    player_x = bl.x - pwidth - xusl
                elif x > bl.x + bl.width - 7:  # правее
                    player_x = bl.x + bl.width - xusl
                if player_y > bl.y + bl.height - 15: #ниже
                    player_y = bl.y + bl.height + 1
                    y_speed = 0
                    return pol
                elif y_foot < bl.y + 2:
                    return bl.y
    return newPol()

# прорисовка деталей
def drawWindow():
    # прорисовка анимаций игрока
    global animCount
    win.blit(bg, (0, 0))
    if animCount + 1 >= 30:
        animCount = 0
    if left:
        win.blit(walkLeft[animCount // 5], (player_x, player_y))
        animCount += 1
    elif right:
        win.blit(walkRight[animCount // 5], (player_x, player_y))
        animCount += 1
    else:
        win.blit(playerStand, (player_x, player_y))
    # pygame.draw.rect(win, (0, 0, 255), (x, y, width, height))
    # прорисовка пуль
    for bull in bullets:
        bull.draw(win)
    # прорисовка фона и стоячих деталей
    for bl in blocks:
        bl.draw(win, xusl)
    font = pygame.font.Font(None, 25)
    text = font.render("Центр позиции х: " + str(xusl), True, [255,255,255])
    win.blit(text, [0, 0])
    # timetext = font.render("Время: " + str(nowBullet - lastBullet), True, [255, 255, 255])
    # win.blit(timetext, [0, 30])
    pygame.display.update()


# создание списка блоков препядствий
for i in range(Bl):
    startx += random.randint(0, 100)
    blocks.append(createBlock(startx))
    startx +=100

lastBullet = time()
# запуск игры
bullets = []
run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # гравитация
    pol = nowPol(pol)
    player_y -= y_speed
    if player_y + pheight < pol:
        y_speed -= jumpCount / 2
        jumpCount += 1
    elif player_y + pheight > pol:
        player_y = pol - pheight
        isJump = False
        jumpCount = 0
        y_speed = 0

    # смещение заряда стрельба пулями
    for bull in bullets:
        if bull.x < 500 and bull.x > 0:
            bull.x += bull.vel
        else:
            bullets.pop(bullets.index(bull))

    keys = pygame.key.get_pressed() #сочитывание зажатых кнопок

    # действия по кнопкам
    # стрельба
    nowBullet = time()
    if keys[pygame.K_SPACE]:
        if len(bullets) < 10 and nowBullet - lastBullet > 0.1:
            bullets.append(bullet(round(player_x + pwidth // 2), round(player_y + pheight // 2),
                                  6, (120, 120, 155), 1 if lastMove == "right" else -1))
            lastBullet = nowBullet

    # смещение персонажа
    if player_x >= 350 and xusl < pointmax - 500:
        speed_r = 0
    elif player_x <= 100 and xusl > pointmin:
        speed_l = 0
    else:
        speed_l = speed_r = speed

    if keys[pygame.K_a] and player_x > 5:
        player_x -= speed_l
        xusl = xusl + speed_l - speed
        left = True
        right = False
        lastMove = 'left'
    elif keys[pygame.K_d] and player_x < xdis - pwidth - 5:
        player_x += speed_r
        xusl = xusl - speed_r + speed
        left = False
        right = True
        lastMove = "right"
    else:
        left = False
        right = False
        animCount = 0

    # Прыжок
    if (keys[pygame.K_w]) and isJump == False:
        isJump = True
        y_speed = 30



    drawWindow()

pygame.quit()
