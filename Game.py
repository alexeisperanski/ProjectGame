import pygame
import random

pygame.init()
xdis = 500
ydis = 500
pointmax = 1500
pointmin = 0
xusl = 250
win = pygame.display.set_mode((xdis,ydis)) #размеры окна
pygame.display.set_caption("Project Game") #название окна

width = 60 #высота
height = 71 #ширина
speed = 5 #скорость
lastMove = "right"

# расположение по x and y
x = 50
y = ydis - height - 10

# Обозначения наличия движения
isJump = False
jumpCount = 10
left = False
right = False
animCount = 0


speed_r = speed_l = speed

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
        pygame.draw.rect(win, self.color, (self.x - xusl + 250, self.y, self.width, self.height))

# создание препядствия
def createBlock(x):
    y = ydis - random.randint(30, 300)
    return(Block(random.randint(x, x+100), y, random.randint(10, 100), random.randint(30, y), (0, 200, 64)))


def drawWindow(): # прорисовка движений
    global animCount
    win.blit(bg, (0, 0))
    if animCount + 1 >= 30:
        animCount = 0
    if left:
        win.blit(walkLeft[animCount // 5], (x, y))
        animCount += 1
    elif right:
        win.blit(walkRight[animCount // 5], (x, y))
        animCount += 1
    else:
        win.blit(playerStand, (x, y))
    # pygame.draw.rect(win, (0, 0, 255), (x, y, width, height))
    for bull in bullets:
        bull.draw(win)

    for bl in blocks:
        bl.draw(win, xusl)
    font = pygame.font.Font(None, 25)
    text = font.render("Центр позиции х: " + str(xusl), True, [255,255,255])
    win.blit(text, [0,0])
    pygame.display.update()

blocks = []
Bl = 10
startx = 200
for i in range(Bl):
    startx += random.randint(0, 100)
    blocks.append(createBlock(startx))
    startx +=100

bullets = []
run = True

while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bull in bullets:
        if bull.x < 500 and bull.x > 0:
            bull.x += bull.vel
        else:
            bullets.pop(bullets.index(bull))

    keys = pygame.key.get_pressed() #сочитывание зажатых кнопок
    # действия по кнопкам
    if keys[pygame.K_SPACE]:
        if len(bullets) < 10:
            bullets.append(bullet(round(x + width // 2), round(y + height // 2),
                                  6, (120, 120, 155), 1 if lastMove == "right" else -1))
    if x>=350 and xusl < pointmax - 250:
        speed_r = 0
    elif x <= 100 and xusl > 250 + pointmin:
        speed_l = 0
    else:
        speed_l = speed_r = speed

    if keys[pygame.K_a] and x > 5:
        x -= speed_l
        xusl = xusl + speed_l - speed
        left = True
        right = False
        lastMove = 'left'
    elif keys[pygame.K_d] and x < xdis - width - 5:
        x += speed_r
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
    if isJump:
        if jumpCount >= -10:
            y -= abs(jumpCount) * jumpCount / 2
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    drawWindow()

pygame.quit()
