
# Tom's Pong
# A simple pong game with realistic physics and AI
# http://www.tomchance.uklinux.net/projects/pong.shtml
#
# Released under the GNU General Public License
#
##############################################################
#
# Modified for educational purposes for the
# CNU Department of Physics, Computer Science and Engineering
#
# Spring 2019 Semester
# Mathew Bartgis, David Conner
#

VERSION = "0.4"

import sys
import random
import math
import os
import pygame
from pygame.locals import *


def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('../img', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        return image
    except pygame.error:
        print('Cannot load image:', fullname)


def calcnewpos(rect, vector):
    (angle, z) = vector
    (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
    return rect.move(dx, dy)


class Ball(pygame.sprite.Sprite):
    """A ball that will move across the screen
    Returns: ball object
    Functions: update, calcnewpos
    Attributes: area, vector"""

    def __init__(self, vector):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('ball.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.hit = 0
        self.rect.midbottom = player1.rect.midtop

    def update(self):
        newpos = calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector

        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if (tr and tl) or (br and bl):
                angle = -angle
            if (tl and bl) or (tr and br):
                angle = math.pi - angle
            # Lose a life
            # it is for the resetting
            # if br and bl:
            #     self.rect.x = 325
            #     self.rect.y = 300
            #     angle = math.pi/2.6
            #     z = 5

        else:
            # Deflate the rectangles so you can't catch a ball behind the bat
            player1.rect.inflate(-3, -3)

            # Do ball and bat collide?
            # Note I put in an odd rule that sets self.hit to 1 when they collide, and unsets it in the next
            # iteration. this is to stop odd ball behaviour where it finds a collision *inside* the
            # bat, the ball reverses, and is still inside the bat, so bounces around inside.
            # This way, the ball can always escape and bounce away cleanly
            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                if self.rect.centerx > player1.rect.centerx:
                    angle = angle - math.pi/3
                elif self.rect.centerx < player1.rect.centerx:
                    angle = angle + math.pi/3

                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit

            for brick in bricks:
                if self.rect.colliderect(brick.rect) == 1:
                    if brick.rect.bottom > self.rect.centery > brick.rect.top: # -> when the ball hit the brick on the side
                        angle = math.pi-angle  # ---> the direction of the angle when the deflects back
                    else:    #  -----> if it hits the top or the bottom
                        if angle < 90:
                            angle = 90 - (angle % 90)
                        else:
                            angle = angle - 60
                    #     if angle < 0:
                    #         angle = angle - math.pi/4
                    #     else:
                    #         angle = angle + math.pi/4
                    brick.health -= 1
                    if (brick.health == 0):
                        brick.rect.topleft= (-128,0)  # move it outside

        self.vector = (angle, z)


class Paddle(pygame.sprite.Sprite):
    """Movable tennis 'bat' with which one hits the ball
    Returns: bat object
    Functions: reinit, update, moveup, movedown
    Attributes: which, speed"""

    X = 0
    Y = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png('paddle.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 10
        self.state = "still"
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.movepos = [0, 0]
        self.rect.midbottom = self.area.midbottom

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pygame.event.pump()

    def moveleft(self):
        self.movepos[Paddle.X] = self.movepos[Paddle.X] - self.speed
        self.state = "moveleft"

    def moveright(self):
        self.movepos[Paddle.X] = self.movepos[Paddle.X] + self.speed
        self.state = "moveright"

    def still(self):
        self.movepos = [0, 0]
        self.state = "still"


class BasicBrick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../img/basic_block.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.health = 1
        self.hit = False


class MediumBrick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../img/med_block.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.health = 3
        self.hit = False



class HardBrick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../img/hard_block.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.rect.topleft = (x, y)
#        self.basic_brick = pygame.image.load('img/basic_block.png')
        self.area = screen.get_rect()
#        self.rect = self.basic_brick
        self.health = 4
        self.hit = False


def main():
    # Initialize screen
    pygame.init()
    screen = pygame.display.set_mode((680, 480))
    pygame.display.set_caption('Tom\'s Pong: v' + str(VERSION))

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    # Initialize players
    global player1
    player1 = Paddle()

    # Initialize ball
    speed = 13
    rand = 0.1 * random.randint(5, 8)
    ball = Ball((0.47, speed))

    # initialize bricks
    global bricks
    bricks = []

    for i in range(5):
        bricks.append(HardBrick(136 * i, 0))

    for i in range(5):
        bricks.append(MediumBrick(136 * i,68))

    for i in range(5):
        bricks.append(BasicBrick(136 * i, 136))
    # bricks.append(BasicBrick(0, 0))
    # bricks.append(BasicBrick(128, 0))
    # # brick = BasicBrick()



    # Initialize sprites
    bricksprite = pygame.sprite.RenderPlain(bricks)
    playersprites = pygame.sprite.RenderPlain(player1)
    ballsprite = pygame.sprite.RenderPlain(ball)

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Initialize clock
    clock = pygame.time.Clock()



    # Event loop
    while True:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1.moveleft()
                if event.key == pygame.K_RIGHT:
                    player1.moveright()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player1.still()


        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, player1.rect, player1.rect)
        for brick in bricks:
            screen.blit(background, brick.rect, brick.rect)
        ballsprite.update()
        playersprites.update()
        ballsprite.draw(screen)
        playersprites.draw(screen)
        bricksprite.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
