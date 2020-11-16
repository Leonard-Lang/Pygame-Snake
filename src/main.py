import pygame

from random import seed
from random import randint

pygame.init()

pygame.display.set_caption("Pygame Snake")

numberOfRows = 20
numberOfColumns = 20
numberOfTiles = numberOfRows * numberOfColumns

boxWidth = 25
boxHeight = 25

windowSizeX = numberOfColumns * boxWidth
windowSizeY = numberOfRows * boxHeight

scoreboardSize = 50

win = pygame.display.set_mode((windowSizeX, windowSizeY + scoreboardSize))

xstartPoint = - boxWidth
ystartPoint = scoreboardSize

font = pygame.font.SysFont('kievitoffcpro', round(scoreboardSize / 2), True)


class Snake(object):
    def __init__(self, x, y):
        self.bodyx = [1]
        self.bodyy = [1]
        self.bodyx[0] = x
        self.bodyy[0] = y
        self.length = 1
        self.newDirection = "right"
        self.currentDirection = "right"
        self.score = 0

    def draw(self, win):
        for i in range(snake.length):
            pygame.draw.rect(win, (0, 0, 150), (self.bodyx[i], self.bodyy[i], boxWidth, boxHeight))

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
            snake.bodyx[0] -= boxWidth
        elif snake.currentDirection == "right":
            snake.bodyx[0] += boxWidth
        elif snake.currentDirection == "up":
            snake.bodyy[0] -= boxHeight
        elif snake.currentDirection == "down":
            snake.bodyy[0] += boxHeight

    # Check if snakes path is blocked
    def isBlocked(self):
        # Check if snake is in the gamefield
        if snake.bodyx[0] < 0 or snake.bodyx[0] >= windowSizeX or snake.bodyy[0] < 0 + scoreboardSize or snake.bodyy[0] >= windowSizeY + scoreboardSize:
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
            self.x = randint(0, numberOfColumns - 1) * boxWidth
            self.y = randint(0, numberOfRows - 1) * boxHeight + scoreboardSize

            for i in range(snake.length):
                if snake.bodyx[i] == self.x and snake.bodyy[i] == self.y:
                    possible = False

    def draw(self, win):
        if self.exists:
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, boxWidth, boxHeight))


def update(win, snake):
    win.fill((0, 150, 0))

    snake.draw(win)
    apple.draw(win)

    for i in range(numberOfColumns):
        pygame.draw.rect(win, (255, 255, 255), (boxWidth * i, scoreboardSize, 1, windowSizeX))

    for j in range(numberOfRows):
        pygame.draw.rect(win, (255, 255, 255), (0, boxHeight * j + scoreboardSize, windowSizeY, 1))

    text = font.render('Score: ' + str(snake.score), 1, (0, 0, 0))
    win.blit(text, (0, round(scoreboardSize / 5)))

    pygame.display.update()


def mainMenu(win):
    run = True
    selectedOption = "Play"
    selectionColor = (255, 150, 150)
    playText = font.render('Play', 1, selectionColor)
    quitText = font.render('Quit', 1, (255, 255, 255))
    while run:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            selectedOption = "Play"
            playText = font.render('Play', 1, selectionColor)
            quitText = font.render('Quit', 1, (255, 255, 255))
        if keys[pygame.K_DOWN]:
            selectedOption = "Quit"
            quitText = font.render('Quit', 1, selectionColor)
            playText = font.render('Play', 1, (255, 255, 255))
        if keys[pygame.K_SPACE]:
            if selectedOption == "Quit":
                return False
            else:
                return True

        win.fill((0, 0, 0))
        win.blit(playText, (round(windowSizeX / 2), 10))
        win.blit(quitText, (round(windowSizeX / 2), 90))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


snake = Snake(xstartPoint, ystartPoint)
apple = Apple()
appleExists = False

run = True
while run:
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
        snake.score += 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if keys[pygame.K_ESCAPE]:
        if not mainMenu(win):
            run = False

    if run:
        snake.score += 1
        update(win, snake)

    pygame.time.delay(300)

pygame.quit()
