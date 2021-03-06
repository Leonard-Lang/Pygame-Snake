import pygame

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

    def draw(self, win, snake):
        for i in range(snake.length):
            pygame.draw.rect(win, (0, 0, 150), (self.bodyx[i], self.bodyy[i], boxWidth, boxHeight))

    def move(self, keys, snake):
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
    def isBlocked(self, snake):
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


def update(win, snake, apple):
    win.fill((0, 150, 0))

    snake.draw(win, snake)
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

    run = True

    file1 = open('highscores.txt', 'r')
    lines = file1.readlines()

    firstRecord = lines[0].split('#')
    secondRecord = lines[1].split('#')
    thirdRecord = lines[2].split('#')

    file1.close()

    win.fill((0, 0, 155))

    firstPlaceText = font.render("1. " + firstRecord[0] + " " + firstRecord[1][:-1] + "p", 1, (255, 255, 255))
    secondPlaceText = font.render("2. " + secondRecord[0] + " " + secondRecord[1][:-1] + "p", 1, (255, 255, 255))
    thirdPlaceText = font.render("3. " + thirdRecord[0] + " " + thirdRecord[1] + "p", 1, (255, 255, 255))

    win.blit(firstPlaceText, (round(windowSizeX / 2), 10))
    win.blit(secondPlaceText, (round(windowSizeX / 2), 90))
    win.blit(thirdPlaceText, (round(windowSizeX / 2), 170))

    pygame.display.update()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


def updateHighscoreList(name, score):
    file1 = open('highscores.txt', 'r')
    lines = file1.readlines()
    file1.close()

    firstRecord = lines[0].split('#')
    secondRecord = lines[1].split('#')
    thirdRecord = lines[2].split('#')
    fourthRecord = [name, score]

    file1 = open('highscores.txt', 'w')

    if int(fourthRecord[1]) > int(firstRecord[1]):
        file1.write(str(fourthRecord[0]) + "#" + str(fourthRecord[1]) + "\n")
        file1.write(str(firstRecord[0]) + "#" + str(firstRecord[1]))
        file1.write(str(secondRecord[0]) + "#" + str(secondRecord[1]))
    elif int(fourthRecord[1]) > int(secondRecord[1]):
        file1.write(str(firstRecord[0]) + "#" + str(firstRecord[1]))
        file1.write(str(fourthRecord[0]) + "#" + str(fourthRecord[1]) + "\n")
        file1.write(str(secondRecord[0]) + "#" + str(secondRecord[1]))
    elif int(fourthRecord[1]) > int(thirdRecord[1]):
        file1.write(str(firstRecord[0]) + "#" + str(firstRecord[1]))
        file1.write(str(secondRecord[0]) + "#" + str(secondRecord[1]))
        file1.write(str(fourthRecord[0]) + "#" + str(fourthRecord[1]))
    else:
        file1.write(str(firstRecord[0]) + "#" + str(firstRecord[1]))
        file1.write(str(secondRecord[0]) + "#" + str(secondRecord[1]))
        file1.write(str(thirdRecord[0]) + "#" + str(thirdRecord[1]))

    file1.close()


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


def gameOverScreen(win):
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
                return ''

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
        if pressed[pygame.K_SPACE]:
            run = False

        win.fill((0, 0, 155))
        win.blit(gameOver, (100, 50))
        win.blit(highscore, (100, 100))
        win.blit(retry, (100, 150))

        pygame.display.update()
        pygame.time.delay(100)

    return selectionOption

def main():
    snake = Snake(xstartPoint, ystartPoint)
    apple = Apple()
    appleExists = False

    name = nameInput()

    run = True

    while run:
        keys = pygame.key.get_pressed()

        snake.move(keys, snake)

        run = snake.isBlocked(snake)

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
            update(win, snake, apple)

        pygame.time.delay(300)

    updateHighscoreList(name, snake.score)

    decision = gameOverScreen(win)
    if decision == 'highscore':
        showHighscoreList()
        gameOverScreen(win)
    elif decision == 'retry':
        main()

    pygame.quit()


if __name__ == "__main__":
    main()