import pygame
import math
import random
from pygame import mixer

#  initialise the pygame
pygame.init()

#  create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("table.png")

# Background Sound
mixer.music.load("005 FLAVOUR.mp3")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Bird Feeder")
icon = pygame.image.load("bird.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("solidarity.png")
playerX = 368
playerY = 480
playerX_change = 0

# Birds and their movement
birdImg = []
birdX = []
birdY = []
birdX_change = []
birdY_change = []
num_of_birds = 6
image = pygame.image.load("bird.png")
flipped_image = pygame.transform.flip(image, True, False)

# creating the birds and their locations
for i in range(num_of_birds):
    birdImg.append(image)
    birdX.append(random.randint(0, 735))
    birdY.append(random.randint(50, 150))
    birdX_change.append(2)
    birdY_change.append(40)

# Seed
# Ready - you can't see seed on screen
# Fire - The seed is currently moving

seedImg = pygame.image.load("flax-seed.png")
seedX = 0
seedY = 480
seedX_change = 0
seedY_change = -15
seed_state = "ready"

# score

score_value = 0
font = pygame.font.Font("Impact Label.ttf", 40)

textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score:  " + str(score_value), True, (255, 200, 200))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def bird(x, y):
    screen.blit(birdImg[i], (x, y))


def fire_seed(x, y):
    global seed_state
    seed_state = "fire"
    screen.blit(seedImg, (x + 16, y + 10))


def isCollision(birdX, birdY, seedX, seedY):
    distance = math.sqrt((math.pow(birdX - seedX, 2)) + (math.pow(birdY - seedY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop

running = True
while running:

    # RGB - Red, Green, Blue max 255 each colour
    screen.fill((0, 0, 30))
    # Background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # quitting the game
        if event.type == pygame.QUIT:
            running = False
        # moving left and right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if seed_state is "ready":
                    seed_sound = mixer.Sound("doorbell.wav")
                    seed_sound.set_volume(0.2)
                    seed_sound.play()
                    seedX = playerX
                    fire_seed(seedX, seedY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                    or event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # checking for boundaries of player, so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # bird movement
    for i in range(num_of_birds):
        birdX[i] += birdX_change[i]
        if birdX[i] <= 0:
            birdX_change[i] = 2
            birdY[i] += birdY_change[i]
            birdImg[i] = image
        elif birdX[i] >= 736:
            birdX_change[i] = -2
            birdY[i] += birdY_change[i]
            birdImg[i] = flipped_image

        # Collision
        collision = isCollision(birdX[i], birdY[i], seedX, seedY)
        if collision:
            bird_sound = mixer.Sound("tweet.mp3")
            bird_sound.set_volume(0.5)
            bird_sound.play()
            seedY = 480
            seed_state = "ready"
            score_value += 1
            birdX[i] = random.randint(0, 735)
            birdY[i] = random.randint(50, 150)

        bird(birdX[i], birdY[i])

    # seed Movement
    if seedY <= -32:
        seedY = 480
        seed_state = "ready"
    if seed_state is "fire":
        fire_seed(seedX, seedY)
        seedY += seedY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
