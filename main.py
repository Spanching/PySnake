import pygame
import random
from Snake import Snake
from Utils import Utils

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


class main:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.win = pygame.display.set_mode((Utils.winWidth, Utils.winHeight))
        self.snake1 = Snake(20, 20 , (255,0,0))
        self.snake2 = Snake(20, 30, (0,0,255))
        self.food = []
        self.isfood = False
        self.timer = 0
        self.lost = 0
        self.run = True
        self.game = True
        self.clickone = False
        self.clicktwo = False
        pygame.display.set_caption('Snake')

    def reset(self):
        self.snake1 = Snake(20,20, (255,0,0))
        self.snake2 = Snake(20,30, (0,0,255))
        self.food = []
        self.isfood = False
        self.points = 0
        self.timer = 0

    def main(self):
        while self.game:
            while self.run:
                self.clickone = self.clicktwo = False
                self.clock.tick(6)
                self.timer += 1
                if self.timer >= 230:
                    self.timer = 0
                    self.snake1.points+=1
                    self.snake2.points+=1
                self.snake1.move()
                self.snake2.move()

                self.handleFood()

                if self.handleCollision():
                    break;

                self.handleEats(self.snake1)
                self.handleEats(self.snake2)

                self.draw(self.win)
                self.handleEvents(pygame.event.get())
                pygame.display.update()
            pygame.display.update()

            self.handleLost()

            self.handleGameEvents(pygame.event.get())
        pygame.quit()

    def handleEats(self, snake):
        if snake.eats(self.food):
            snake.points += 10
            self.isfood = False

    def handleCollision(self):
        one = self.snake1.collides(self.snake2)
        two = self.snake2.collides(self.snake1)
        if one or two:
            head1 = self.snake1.blocks[len(self.snake1.blocks) - 1]
            head2 = self.snake2.blocks[len(self.snake2.blocks) - 1]
            if head1 == head2:
                self.lost = 3
            elif one and two:
                self.lost = 3
            elif head1 in self.snake2.blocks:
                self.lost = 1
            elif head2 in self.snake1.blocks:
                self.lost = 2
            elif one:
                self.lost = 1
            elif two:
                self.lost = 2
            else:
                self.lost = 0
            self.run = False
            return True
        return False

    def handleFood(self):
        if not self.isfood:
            self.food = self.getrndfood()
            self.isfood = True

    def getrndfood(self):
        f = [(random.randrange(40), random.randrange(35)),(random.randrange(40), random.randrange(35)),(random.randrange(40), random.randrange(35)),(random.randrange(40), random.randrange(35)),(random.randrange(40), random.randrange(35))]
        for foo in f:
            while foo in self.snake2.blocks+self.snake1.blocks:
                foo = (random.randrange(40), random.randrange(35))
        return f

    def draw(self, win):

        pygame.draw.rect(win, (0, 0, 0), (0, 0, 1000, 800), 0)

        # draw the outer line
        pygame.draw.rect(win, (128, 128, 128), (Utils.offsetX, Utils.offsetY, Utils.gridWidth, Utils.gridHeight), 1)

        surfaceText = myfont.render("Player 1 : "+str(self.snake1.points) + " Player 2 : "+str(self.snake2.points), False, (255,255,255))
        win.blit(surfaceText, (Utils.offsetX, 10))

        # draw the grid
        for i in range(1,40):
            pygame.draw.line(win, (128,128,128),(Utils.offsetX+i*Utils.pixelSquare,Utils.offsetY),(Utils.offsetX+i*Utils.pixelSquare,750),1)

        for i in range(1, 35):
            pygame.draw.line(win, (128, 128, 128), (Utils.offsetX, Utils.offsetY+i*Utils.pixelSquare), (900, Utils.offsetY+i*Utils.pixelSquare), 1)

        #draw the food
        for f in self.food:
            pygame.draw.rect(win, (0,255,0), (Utils.offsetX+f[0]*Utils.pixelSquare+1, Utils.offsetY+f[1]*Utils.pixelSquare+1, Utils.pixelSquare-2,Utils.pixelSquare-2), 0)

        self.snake1.draw(win)
        self.snake2.draw(win)

    def textOnScreen(self, win, text):
        surfaceText = myfont.render(text, False, (255,255,255))
        win.blit(surfaceText, (500-surfaceText.get_width()/2, 400-surfaceText.get_height()))

    def handleGameEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.run = True
                    if self.lost == 1 or self.lost == 2 or self.lost == 3:
                        self.lost = 0
                        self.reset()

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.lost = 0
                    self.run = False
                if not self.clickone:
                    if event.key == pygame.K_UP:
                        if (self.snake1.direction != 1):
                            self.snake1.direction = 3
                            self.clickone = True
                            continue
                    elif (event.key == pygame.K_DOWN):
                        if (self.snake1.direction != 3):
                            self.snake1.direction = 1
                            self.clickone = True
                            continue
                    elif (event.key == pygame.K_LEFT):
                        if (self.snake1.direction != 2):
                            self.snake1.direction = 0
                            self.clickone = True
                            continue
                    elif (event.key == pygame.K_RIGHT):
                        if (self.snake1.direction != 0):
                            self.snake1.direction = 2
                            self.clickone = True
                            continue
                if not self.clicktwo:
                    if event.key == 119:
                        if self.snake2.direction != 1:
                            self.snake2.direction = 3
                            self.clicktwo = True
                            continue
                    elif (event.key == 115):
                        if (self.snake2.direction != 3):
                            self.snake2.direction = 1
                            self.clicktwo = True
                            continue
                    elif (event.key == 97):
                        if (self.snake2.direction != 2):
                            self.snake2.direction = 0
                            self.clicktwo = True
                            continue
                    elif (event.key == 100):
                        if (self.snake2.direction != 0):
                            self.snake2.direction = 2
                            self.clicktwo = True
                            continue

    def handleLost(self):
        if self.lost == 1:
            self.textOnScreen(self.win, "Player 1 lost the Game with " + str(
                self.snake1.points) + " points against Player 2 with " + str(self.snake2.points) + ".")
        elif self.lost == 2:
            self.textOnScreen(self.win, "Player 2 lost the Game with " + str(
                self.snake2.points) + " points against Player 1 with " + str(self.snake1.points) + ".")
        elif self.lost == 3:
            self.textOnScreen(self.win,
                              "You both suck! 1: " + str(self.snake1.points) + " 2: " + str(self.snake2.points) + ".")
        else:
            self.textOnScreen(self.win, "Pause")

m = main()
m.main()