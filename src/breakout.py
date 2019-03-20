import sys
import random
import math
import os
import pygame

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


class Ball (pygame.sprite.Sprite):
    def __init__(self, ball_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('ball.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.ball_speed = ball_speed
        self.hit = False

    def ball_hit(self, boolean):
        self.hit = boolean

    def ball_direction(self):
        

