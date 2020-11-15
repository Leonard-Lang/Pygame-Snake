import pygame

from random import seed
from random import randint

pygame.init()

pygame.display.set_caption("Pygame Snake")

numberOfRows = 10
numberOfColumns = 10
numberOfTiles = numberOfRows * numberOfColumns

width = 50
height = 50


class Snake(object):
    def __init__(self, x, y):
        self.bodyx = [1]
        self.bodyy = [1]
        self.bodyx[0] = x
        self.bodyy[0] = y
        self.length = 1
        self.newDirection = "right"
        self.currentDirection = "right"

    def draw(self, win):
        for i in range(snake.length):
            pygame.draw.rect(win, (0, 255, 0), (self.bodyx[i], self.bodyy[i], width, height))

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            snake.newDirection = "left"
        if keys[pygame.K_RIGHT]:
            snake.newDirection = "right"
        if keys[pygame.K_UP]:
            snake.newDirection = "up"
        if keys[pygame.K_DOWN]:
            snake.newDirection = "down"

        if snake.newDirection == "left" and snake.currentDirection != "right":
            snake.currentDirection = snake.newDirection

        if snake.newDirection == "right" and snake.currentDirection != "left":
            snake.currentDirection = snake.newDirection

        if snake.newDirection == "up" and snake.currentDirection != "down":
            snake.currentDirection = snake.newDirection

        if snake.newDirection == "down" and snake.currentDirection != "up":
            snake.currentDirection = snake.newDirection

        for i in range(snake.length - 1, 0, -1):
            snake.bodyx[i] = snake.bodyx[i-1]
            snake.bodyy[i] = snake.bodyy[i-1]

        if snake.currentDirection == "left":
            snake.bodyx[0] -= 50
        elif snake.currentDirection == "right":
            snake.bodyx[0] += 50
        elif snake.currentDirection == "up":
            snake.bodyy[0] -= 50
        elif snake.currentDirection == "down":
            snake.bodyy[0] += 50

    # Check if snakes path is blocked
    def isBlocked(self):
        # Check if snake is in the gamefield
        if snake.bodyx[0] < 0 or snake.bodyx[0] >= 500 or snake.bodyy[0] < 0 or snake.bodyy[0] >= 500:
            return False

        # Check if snake eats itself
        for i in range(1, snake.length):
            if snake.bodyx[0] == snake.bodyx[i] and snake.bodyy[0] == snake.bodyy[i]:
                return False

        return True


class Apple(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.exists = True

    def spawn(self, snake):

        possible = False
        while not possible:
            possible = True
            self.x = randint(0, 9) * 50
            self.y = randint(0, 9) * 50

            for i in range(snake.length):
                if snake.bodyx[i] == self.x and snake.bodyy[i] == self.y:
                    possible = False

    def draw(self, win):
        if self.exists:
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, width, height))


def update(win):
    win.fill((0, 0, 0))

    snake.draw(win)
    apple.draw(win)

    for i in range(numberOfColumns):
        pygame.draw.rect(win, (255, 255, 255), (50 * i, 0, 1, 500))

    for j in range(numberOfRows):
        pygame.draw.rect(win, (255, 255, 255), (0, 50 * j, 500, 1))

    pygame.display.update()


win = pygame.display.set_mode((500, 500))

xstartPoint = 0
ystartPoint = 0

snake = Snake(xstartPoint, ystartPoint)
apple = Apple()
appleExists = False

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    snake.move(keys)

    run = snake.isBlocked()

    if not appleExists:
        apple.exists = True
        appleExists = True
        apple.spawn(snake)

    if snake.bodyx[0] == apple.x and snake.bodyy[0] == apple.y:
        appleExists = False
        apple.exists = False
        snake.bodyx.append(apple.x)
        snake.bodyy.append(apple.y)
        snake.length += 1

    update(win)

    pygame.time.delay(300)

pygame.quit()
