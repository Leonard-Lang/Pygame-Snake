import pygame

from operator import itemgetter
from random import randint

pygame.init()

pygame.display.set_caption("Pygame Snake")

numberOfRows = 10
numberOfColumns = 10
numberOfTiles = numberOfRows * numberOfColumns

boxWidth = 50
boxHeight = 50

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

    def draw(self, snake):
        for i in range(snake.length):
            pygame.draw.rect(win, (0, 0, 150), (self.bodyx[i], self.bodyy[i], boxWidth, boxHeight))

    # Move the snake in the certain direction
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.newDirection = "left"
        if keys[pygame.K_RIGHT]:
            self.newDirection = "right"
        if keys[pygame.K_UP]:
            self.newDirection = "up"
        if keys[pygame.K_DOWN]:
            self.newDirection = "down"

        if self.newDirection == "left" and self.currentDirection != "right":
            self.currentDirection = self.newDirection

        if self.newDirection == "right" and self.currentDirection != "left":
            self.currentDirection = self.newDirection

        if self.newDirection == "up" and self.currentDirection != "down":
            self.currentDirection = self.newDirection

        if self.newDirection == "down" and self.currentDirection != "up":
            self.currentDirection = self.newDirection

        for i in range(self.length - 1, 0, -1):
            self.bodyx[i] = self.bodyx[i - 1]
            self.bodyy[i] = self.bodyy[i - 1]

        if self.currentDirection == "left":
            self.bodyx[0] -= boxWidth
        elif self.currentDirection == "right":
            self.bodyx[0] += boxWidth
        elif self.currentDirection == "up":
            self.bodyy[0] -= boxHeight
        elif self.currentDirection == "down":
            self.bodyy[0] += boxHeight

    # Check if snakes path is blocked
    def isBlocked(self):
        # Check if snake is in the gamefield
        if self.bodyx[0] < 0 or self.bodyx[0] >= windowSizeX or self.bodyy[0] < 0 + scoreboardSize or self.bodyy[0] >= windowSizeY + scoreboardSize:
            return False

        # Check if snake eats itself
        for i in range(1, self.length):
            if self.bodyx[0] == self.bodyx[i] and self.bodyy[0] == self.bodyy[i]:
                return False

        return True


class Apple(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    def spawn(self, snake):

        possible = False
        while not possible:
            possible = True
            self.x = randint(0, numberOfColumns - 1) * boxWidth
            self.y = randint(0, numberOfRows - 1) * boxHeight + scoreboardSize

            for i in range(snake.length):
                if snake.bodyx[i] == self.x and snake.bodyy[i] == self.y:
                    possible = False

    def draw(self, appleExists):
        if appleExists:
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, boxWidth, boxHeight))


def update(snake, apple, appleExists):
    win.fill((0, 150, 0))

    snake.draw(snake)
    apple.draw(appleExists)

    for i in range(numberOfColumns):
        pygame.draw.rect(win, (255, 255, 255), (boxWidth * i, scoreboardSize, 1, windowSizeX))

    for j in range(numberOfRows):
        pygame.draw.rect(win, (255, 255, 255), (0, boxHeight * j + scoreboardSize, windowSizeY, 1))

    text = font.render('Score: ' + str(snake.score), 1, (0, 0, 0))
    win.blit(text, (0, round(scoreboardSize / 5)))

    pygame.display.update()


def mainMenu():
    run = True
    selectedOption = "Play"
    selectionColor = (255, 150, 150)
    playText = font.render('Play', 1, selectionColor)
    highscoreText = font.render('Highscore', 1, (255, 255, 255))
    quitText = font.render('Quit', 1, (255, 255, 255))
    while run:

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            if selectedOption == "Quit":
                selectedOption = "Highscore"
                playText = font.render('Play', 1, (255, 255, 255))
                highscoreText = font.render('Highscore', 1, selectionColor)
                quitText = font.render('Quit', 1, (255, 255, 255))
            elif selectedOption == "Highscore":
                selectedOption = "Play"
                playText = font.render('Play', 1, selectionColor)
                highscoreText = font.render('Highscore', 1, (255, 255, 255))
                quitText = font.render('Quit', 1, (255, 255, 255))
        if keys[pygame.K_DOWN]:
            if selectedOption == "Highscore":
                selectedOption = "Quit"
                quitText = font.render('Quit', 1, selectionColor)
                highscoreText = font.render('Highscore', 1, (255, 255, 255))
                playText = font.render('Play', 1, (255, 255, 255))
            if selectedOption == "Play":
                selectedOption = "Highscore"
                quitText = font.render('Quit', 1, (255, 255, 255))
                highscoreText = font.render('Highscore', 1, selectionColor)
                playText = font.render('Play', 1, (255, 255, 255))

        pygame.time.delay(100)

        if keys[pygame.K_SPACE]:
            if selectedOption == "Quit":
                return False
            elif selectedOption == "Play":
                return True
            else:
                showHighscoreList()

        win.fill((0, 0, 0))
        win.blit(playText, (round(windowSizeX / 2), 10))
        win.blit(highscoreText, (round(windowSizeX / 2), 90))
        win.blit(quitText, (round(windowSizeX / 2), 170))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


def showHighscoreList():
    try:
        file = open('highscores.txt', 'r')
    except:
        print("File does not exists")
        return

    lines = file.readlines()
    file.close()

    win.fill((0, 0, 155))
    for i in range(len(lines)):
        record = lines[i].split('#')
        record[1] = int(record[1])
        recordText = font.render(str(i + 1) + ". " + record[0] + " " + str(record[1]) + "p", 1, (255, 255, 255))
        win.blit(recordText, (round(windowSizeX / 2), (i * 100) + 10))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            run = False


def updateHighscoreList(name, score):
    try:
        file = open('highscores.txt', 'r')
    except:
        print("File does not exists")

    lines = file.readlines()
    file.close()

    sepLines = list(list())

    sepLines.append([name, score])

    for line in lines:
        record = line.split('#')
        record[1] = int(record[1])
        sepLines.append(record)

    sortedRecords = sorted(sepLines, key=itemgetter(1), reverse=True)

    try:
        file = open('highscores.txt', 'w')
    except:
        print("File does not exists")

    length = len(sepLines)
    if len(sepLines) > 3:
        length = 3

    for i in range(length):
        file.write(sortedRecords[i][0] + '#' + str(sortedRecords[i][1]) + '\n')

    file.close()


def nameInput():
    win.fill((0, 0, 155))

    input_box = pygame.Rect(100, 100, 140, 32)

    name = font.render("Enter your name", 1, (255, 255, 255))

    win.blit(name, (100, 50))
    pygame.draw.rect(win, (255, 255, 255), input_box, 2)

    pygame.display.update()

    run = True
    text = ''
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                text += event.unicode

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            run = False

        txt_surface = font.render(text, True, (255, 255, 255))
        win.blit(txt_surface, (110, 100))

        pygame.display.flip()
        pygame.time.delay(100)

    return text


def gameOverScreen():
    win.fill((0, 0, 155))

    selectionColor = (255, 150, 150)
    selectionOption = 'highscore'

    gameOver = font.render("Game Over", 1, (255, 255, 255))
    highscore = font.render("Highscore", 1, selectionColor)
    retry = font.render("Retry", 1, (255, 255, 255))

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            run = False
        if pressed[pygame.K_DOWN]:
            highscore = font.render("Highscore", 1, (255, 255, 255))
            retry = font.render("Retry", 1, selectionColor)
            selectionOption = 'retry'
        if pressed[pygame.K_UP]:
            highscore = font.render("Highscore", 1, selectionColor)
            retry = font.render("Retry", 1, (255, 255, 255))
            selectionOption = 'highscore'
        if pressed[pygame.K_ESCAPE]:
            selectionOption = 'quit'
        if pressed[pygame.K_SPACE]:
            run = False

        win.fill((0, 0, 155))
        win.blit(gameOver, (100, 50))
        win.blit(highscore, (100, 100))
        win.blit(retry, (100, 150))

        pygame.display.update()
        pygame.time.delay(100)

    return selectionOption


def main(name):
    snake = Snake(xstartPoint, ystartPoint)
    apple = Apple()
    appleExists = False

    if name == '':
        name = nameInput()

    run = True

    while run:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

        snake.move(keys)

        run = snake.isBlocked()

        if not appleExists:
            appleExists = True
            apple.spawn(snake)

        if snake.bodyx[0] == apple.x and snake.bodyy[0] == apple.y:
            appleExists = False
            snake.bodyx.append(apple.x)
            snake.bodyy.append(apple.y)
            snake.length += 1
            snake.score += 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if keys[pygame.K_ESCAPE]:
            if not mainMenu():
                run = False

        if run:
            snake.score += 1
            update(snake, apple, appleExists)

        pygame.time.delay(250)

    updateHighscoreList(name, snake.score)

    run = True
    while run:
        decision = gameOverScreen()
        if decision == 'highscore':
            showHighscoreList()
        if decision == 'retry':
            main(name)
        if decision == 'quit':
            break

    pygame.quit()


if __name__ == "__main__":
    name = ''
    main(name)
