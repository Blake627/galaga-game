# Galaga Main V 0.1.3
# Kevin & Blake
# 7/20/21 9:31

import pygame
import math
import random

win_width = 600
win_height = 800
pygame.init()
surface = pygame.display.set_mode((win_width, win_height))
done = False
clock = pygame.time.Clock()
green = 0, 255, 0
red = 255, 0, 0
blue = 0, 0, 255
yellow = 255, 255, 0
white = 255, 255, 255
black = 0, 0, 0


class Square:
    def __init__(self, color, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.direction = 'E'
        self.speed = speed

    def move(self):
        if self.direction == 'E':
            self.rect.x = self.rect.x + self.speed
        if self.direction == 'W':
            self.rect.x = self.rect.x - self.speed
        if self.direction == 'N':
            self.rect.y = self.rect.y - self.speed
        if self.direction == 'S':
            self.rect.y = self.rect.y + self.speed

    def moveDirection(self, direction):
        if direction == 'E':
            self.rect.x = self.rect.x + self.speed
        if direction == 'W':
            self.rect.x = self.rect.x - self.speed
        if direction == 'N':
            self.rect.y = self.rect.y - self.speed
        if direction == 'S':
            self.rect.y = self.rect.y + self.speed

    def collided(self, other_rect):
        return self.rect.colliderect(other_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


# Inheritance
class Bullet(Square):
    def __init__(self, color, x, y, width, height, speed, targetx, targety):
        super().__init__(color, x, y, width, height, speed)
        angle = math.atan2(targety - y, targetx - x)  # get angle to target in radians
        print('Angle in degrees:', int(angle * 180 / math.pi))
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.x = x
        self.y = y

    # Override
    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


# Build a square
sq = Square(green, 200, 200, 50, 50, 10)

bullets = []
enemies = []

# Main program loop
while not done:
    # @@@@@@@@@@@
    # @ Updates @
    # @@@@@@@@@@@
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire a bullet
                spawnx = sq.rect.x + sq.rect.width / 2 - 10
                b = Square(red, spawnx, sq.rect.y, 20, 20, 20)
                b.direction = 'N'
                bullets.append(b)
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # print(x,y)
            b = Bullet(red, sq.rect.centerx, sq.rect.centery, 20, 20, 20, x, y)
            bullets.append(b)

    # @@@@@@@@@
    # @ Input @
    # @@@@@@@@@
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        sq.moveDirection('N')
    if pressed[pygame.K_a]:
        sq.moveDirection('W')
    if pressed[pygame.K_s]:
        sq.moveDirection('S')
    if pressed[pygame.K_d]:
        sq.moveDirection('E')

    # Update game objects
    for b in bullets:
        b.move()
    for e in enemies:
        e.move()
    # spawn enemies on the top of the screen and tell them to move down
    if random.randint(1, 30) == 15:  # 15 doesn't matter
        x = random.randint(0, win_width - 40)
        e = Square(yellow, x, -40, 40, 40, 10)
        e.direction = 'S'
        enemies.append(e)
    # Check for collisions
    for i in reversed(range(len(bullets))):
        for j in reversed(range(len(enemies))):
            if bullets[i].collided(enemies[j].rect):
                del enemies[j]
                del bullets[i]
                break

    # @@@@@@@@@@@
    # @ Drawing @
    # @@@@@@@@@@@

    surface.fill(black)
    for b in bullets:
        b.draw(surface)
    for e in enemies:
        e.draw(surface)
    sq.draw(surface)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
exit()
