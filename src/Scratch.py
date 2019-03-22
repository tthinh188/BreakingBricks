import os
import pygame
import math


class Ball(pygame.sprite.Sprite):
    # location of the ball
    x = 0.0
    y = 180.0
    direction = 200  # direction of the ball (in degrees)

    def __init__(self, speed):
        player1 = Paddle()                                 # TP 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../img/ball.png')  # TP fix cannot load image ('img/paddle.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = speed
        self.hit = 0
        self.rect.midbottom = player1.rect.midtop          # TP (place the ball on the top of the Paddle)

    def bounce(self, x):
        self.direction = (180- self.direction) % 360
        self.direction -= x

    def update(self):
        direction_radians = math.radians(self.direction)

        self.x += self.speed  * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # Do we bounce of the right side of the screen?
        if self.x >= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # Did we fall off the bottom edge of the screen?
        if self.y > 600:
            return True
        else:
            return False


class Paddle(pygame.sprite.Sprite):
    x = 0
    y = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../img/paddle.png')               # TP fix cannot load paddle ('img/paddle.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 10
        self.state = "still"
        self.position()

    def position(self):
        self.state = "still"
        self.move_position = [0, 0]
        self.rect.bottom = self.area.bottom

    def update(self):
        new_position = self.rect.move(self.move_position)
        if self.area.contains(new_position):
            self.rect = new_position
        pygame.event.pump()


class Brick:
    pass

def main():
    # initialize the screen of the game
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    pygame.display.set_caption("Breakout")

    screen.fill((56, 53, 186)) # <- filled the background screen

    ball = Ball(15)

    global player1                                            # TP instance paddle
    player1 = Paddle()

    playersprites = pygame.sprite.RenderPlain(player1)        # TP displace Paddle
    playersprites.draw(screen)

    ballsprite = pygame.sprite.RenderPlain(ball)              # TP display ball
    ballsprite.draw(screen)

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            pygame.display.flip()
            pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    main()
