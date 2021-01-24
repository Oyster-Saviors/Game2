import math
import random
from pygame import mixer
from datetime import datetime, time
import  pygame

# Intialize the game
pygame.init()
# initialize the mixer for audio
#pygame.mixer.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background Image
background = pygame.image.load('images/river.png')
bg = pygame.transform.scale(background, (800,600))
bgY_change = 0
height = 800

# Sound
mixer.music.load("sound/background_music.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Foster the Oyster")
icon = pygame.image.load('images/oyster.png')
pygame.display.set_icon(icon)

# Player_Kajak
playerImg = pygame.image.load('images/Right_00.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Octopus
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_octopus = 6

for i in range(number_of_octopus):
    enemyImg.append(pygame.image.load('images/octopus.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - the oyster is not displayed in the screen
# Fire - The oyster is moving

bulletImg = pygame.image.load('images/oyster_bullet.png')
oysterX = 0
oysterY = 480
oysterX
_change = 0
oysterY_change = 10
bullet_state = "ready"

# game Score
now = datetime.now()
game_begin = datetime.combine(now.date(), time(0))
score_value = (now - game_begin).seconds
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# font for Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def display_Score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def GameOver_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def octopus(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_oyster(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, oysterX
, oysterY):
    distance = math.sqrt(math.pow(enemyX - oysterX
    , 2) + (math.pow(enemyY - oysterY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game-Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((139,69,19))
    # Background Image
    screen.blit(background, (180, bgY_change))
    screen.blit(background, (180, height+bgY_change))

    if bgY_change == -height:
      screen.blit(background, (180, height+bgY_change))
      bgY_change = 0
    bgY_change -= 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Action events for Pressed Keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -1
            if  event.key == pygame.K_RIGHT:
                playerX_change = 1
            if  event.key == pygame.K_UP:
                playerY_change = -1
            if  event.key == pygame.K_DOWN:
                playerY_change = 1
								
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    oysterSound = mixer.Sound("sound/shoot_oyster_sound.wav")
                    oysterSound.play()
                    # Get the current x cordinate of the spaceship
                    oysterX = playerX
                    fire_oyster(oysterX, oysterY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT  or event.key == pygame.K_UP  or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
                

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # octopus movements
    for i in range(number_of_octopus):

        # Game Over
        if enemyY[i] > 440:
            for j in range(number_of_octopus):
                enemyY[j] = 2000
            GameOver_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], oysterX
        , oysterY)
        if collision:
            collision_sound = mixer.Sound("sound/collision_sound.wav")
            collision_sound.play()
            oysterY = 480
            bullet_state = "ready"
            score_value += 5
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        octopus(enemyX[i], enemyY[i], i)

    # oyster Movement
    if oysterY <= 0:
        oysterY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_oyster(oysterX, oysterY)
        oysterY -= oysterY_change

    player(playerX, playerY)
    display_Score(textX, testY)
    pygame.display.update()
    