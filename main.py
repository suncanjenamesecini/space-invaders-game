import pygame
from pygame import mixer
import random
import math

#initialize the pygame
pygame.init()


#create the screen
screen = pygame.display.set_mode((800,600))

#background
background = pygame.image.load("space.jpg")

#background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#game over text
game_over_font = pygame.font.Font('freesansbold.ttf',64)

def show_score(x, y):
    score = font.render("Bodovi: "+ str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over = game_over_font.render("KRAJ IGRE", True, (255,255,255))
    screen.blit(over, (200, 250))

#player
playerImage = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImage, (x, y))

#enemy
enemyImage = [pygame.image.load("enemy.png"),pygame.image.load("enemy2.png"), pygame.image.load("enemy3.png"),\
                pygame.image.load("enemy4.png"), pygame.image.load("enemy5.png"), pygame.image.load("enemy6.png")]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for n in range(num_of_enemies):
    #enemyImage.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 750))
    enemyY.append(random.randint(0, 50))
    enemyX_change.append(2)
    enemyY_change.append(40)

def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))

#bullet
bulletImage = pygame.image.load("bullet.png")
bulletX = playerX
bulletY = playerY
bulletX_change = 0
bulletY_change = -6
#ready-you can't see the bullet on the screen
#fire-the bullet is currently moving
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y - 10))

def isCollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt(math.pow((bulletX - enemyX), 2) + math.pow((bulletY - enemyY), 2))
    if distance < 27:
        return True
    else:
        return False

#game loop
running = True
while running:

    screen.fill((0,0,0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4

            if event.key == pygame.K_RIGHT:
                playerX_change = 4

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    #checking for boundaries
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    #enemy movement
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]

            #Collision
        collision = isCollision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bullet_state = "ready"
            bulletY = playerY
            score_value += 1
            
            enemyX[i] = random.randint(0, 750)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    player(playerX, playerY) 

    #bullet movement
    if bulletY <= 0:
        bullet_state ="ready"
        bulletY = 480

    if bullet_state == "fire":
        fire_bullet(playerX, bulletY -10)
        bulletY += bulletY_change

    show_score(textX, textY)
    pygame.display.update()