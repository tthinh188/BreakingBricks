import os
import pygame
import math


class Ball(pygame.sprite.Sprite):
    #location of the ball
    x = 0.0
    y = 180.0
    direction = 200  # direction of the ball (in degrees)

    def __init__(self, speed):
        player1 = Paddle()  #
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'img/ball.png')  # ('../img/ball.png')  # fix cannot load image ('img/paddle.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = speed
        self.hit = 0
        self.rect.midbottom = player1.rect.midtop  # place the ball on the top of the Paddle

    def bounce(self, x):
        self.direction = (180 - self.direction) % 360
        self.direction -= x

    # Experiment consists of codes from pygames.org #
    def update(self):
        direction_radians = math.radians(self.direction)

        self.x += self.speed * math.sin(direction_radians)
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
    #  #####################################


class Paddle(pygame.sprite.Sprite):
    x = 0
    y = 1

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            'img/paddle.png')  # ('../img/paddle.png')  # fix cannot load paddle ('img/paddle.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.speed = 10
        self.state = "still"
        self.position()

    def position(self):
        self.state = "still"
        self.move_position = [0, 0]
        self.rect.midbottom = self.area.midbottom

    def update(self):
        new_position = self.rect.move(self.move_position)
        if self.area.contains(new_position):
            self.rect = new_position
        pygame.event.pump()

    def moveleft(self):
        self.move_position[Paddle.x] = self.move_position[Paddle.x] - self.speed
        self.state = "moveleft"

    def moveright(self):
        self.move_position[Paddle.x] = self.move_position[Paddle.x] + self.speed
        self.state = "moveright"

    def still(self):
        self.move_position = [0, 0]
        self.state = "still"

#
# class Brick(pygame.sprite.Sprite):
#     def __init__(self):
#         pygame.sprite.Sprite.__init__(self)


class BasicBrick(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/basic_block.png')
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
#        self.basic_brick = pygame.image.load('img/basic_block.png')
        self.area = screen.get_rect()
#        self.rect = self.basic_brick
        self.health = 1
        self.hit = False

    def health(self):
        # if the basic block was hit health will reduced by one and when it reaches zero
        # it will disappear
        if self.hit is True:
            self.health -= 1
        if self.health == 0:
            self.alive()


def main():
    # initialize the screen of the game
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    pygame.display.set_caption("Breakout")

    screen.fill((0, 0, 0))  # ((56, 53, 186))  # <- filled the background screen
    # Sorry! The blue screen just look too bright
    ball = Ball(15)

    global player1  # instance paddle
    player1 = Paddle()
    brick = BasicBrick()
    brick2 = BasicBrick()

    print(screen.get_width)

    playersprites = pygame.sprite.RenderPlain(player1)  # displace Paddle
    playersprites.draw(screen)

    ballsprite = pygame.sprite.RenderPlain(ball)  # display ball
    ballsprite.draw(screen)

    bricksprite = pygame.sprite.RenderPlain(brick)
    bricksprite.draw(screen)

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            pygame.display.flip()
            pygame.display.update()

    clock = pygame.time.Clock()

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
        # screen.blit(background, ball.rect, ball.rect)
        # screen.blit(background, player1.rect, player1.rect)
        # screen.blit(background, brick.rect, brick.rect)
        ballsprite.update()
        playersprites.update()
        ballsprite.draw(screen)
        playersprites.draw(screen)
        bricksprite.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
