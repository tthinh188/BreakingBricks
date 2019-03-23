import pygame
import math

pygame.init()

win = pygame.display.set_mode((1000, 500))

pygame.display.set_caption("Breakout")

x = 50
y = 50
width = 40
height = 60
vel = 10  #velocity


# this is for the paddle
run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < 1000 - width - vel: # second video 3: 56
        x += vel

    win.fill((0,0,0))
    pygame.draw.rect(win, (255, 0,0), (x,y,width, height))
    pygame.display.update()

# so it would not go off the screen

pygame.quit()




