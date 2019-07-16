import pygame
import random

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

class Snake:
    def __init__(self, x, y , color):
        self.points = 0
        self.blocks = [(x,y),(x+1,y)]
        self.color = color
        self.direction = 0 # 0: left  1: down  2: right  3: up
        self.food = []

    def move(self):
        direction = self.direction
        x = 0
        y = 0
        if direction==0:
            x=-1
        elif direction==1:
            y=1
        elif direction==2:
            x=1
        elif direction==3:
            y=-1
        if len(self.food)>0:
            last = self.blocks[0]
            if last[0] != self.food[0][0] or last[1] != self.food[0][1]:
                self.blocks.pop(0)
            else:
                self.food.pop(0)
        else:
            self.blocks.pop(0)
        b = self.blocks[len(self.blocks)-1]
        self.blocks.append((b[0]+x, b[1]+y))

    def collides(self, enemy):
        for i, b1 in enumerate(self.blocks,1):
            if b1[0]<0 or b1[0]>39 or b1[1]<0 or b1[1]>34:
                return True
            for j in range(i, len(self.blocks+enemy.blocks)-1):
                b2 = (self.blocks+enemy.blocks)[j]
                if b1[0] == b2[0] and b1[1] == b2[1]:
                    return True
        return False

    def eats(self, food):
        for f in food:
            b = self.blocks[len(self.blocks)-1]
            if b[0] == f[0] and b[1]== f[1]:
                self.food.append(f)
                return True
        return False


class main:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.win = pygame.display.set_mode((1000, 800))
        self.width = 800
        self.height = 700
        self.snake1 = Snake(20, 20 , (255,0,0))
        self.snake2 = Snake(20, 30, (0,0,255))
        self.food = (-1,-1)
        self.isfood = False
        self.pixelOfRect = 20
        self.offsetX = 100
        self.offsetY = 50
        self.width = 800
        self.height = 700
        self.timer = 0
        pygame.display.set_caption('Snake')

    def reset(self):
        self.snake1 = Snake(20,20, (255,0,0))
        self.snake2 = Snake(20,30, (0,0,255))
        self.food = []
        self.isfood = False
        self.points = 0
        self.timer = 0

    def main(self):
        run = True
        game = True
        lost = 0
        while game:
            while(run):
                self.clock.tick(6)
                clickone = False
                clicktwo = False
                self.timer += 1
                if self.timer >= 230:
                    self.timer = 0
                    self.snake1.points+=1
                    self.snake2.points+=1
                self.snake1.move()
                self.snake2.move()
                if not(self.isfood):
                    self.food = self.getrndfood()
                    self.isfood = True
                one = self.snake1.collides(self.snake2)
                two = self.snake2.collides(self.snake1)
                if one or two :
                    head1 = self.snake1.blocks[len(self.snake1.blocks)-1]
                    head2 = self.snake2.blocks[len(self.snake2.blocks)-1]
                    if head1 == head2:
                        lost = 3
                    elif one and two:
                        lost = 3
                    elif head1 in self.snake2.blocks:
                        lost = 1
                    elif head2 in self.snake1.blocks:
                        lost = 2
                    elif one:
                        lost = 1
                    elif two:
                        lost = 2
                    else:
                        lost = 0
                    run = False
                    break
                if self.snake1.eats(self.food):
                    self.snake1.points += 10
                    self.isfood = False
                if self.snake2.eats(self.food):
                    self.snake2.points+=10
                    self.isfood = False
                self.draw(self.win)
                for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        game= False
                    if(event.type == pygame.KEYDOWN):
                        if event.key == pygame.K_SPACE:
                            lost = 0
                            run = False
                        if not clickone:
                            if (event.key == pygame.K_UP):
                                if (self.snake1.direction != 1):
                                    self.snake1.direction = 3
                                    clickone = True
                                    continue
                            elif (event.key == pygame.K_DOWN):
                                if (self.snake1.direction != 3):
                                    self.snake1.direction = 1
                                    clickone = True
                                    continue
                            elif (event.key == pygame.K_LEFT):
                                if (self.snake1.direction != 2):
                                    self.snake1.direction = 0
                                    clickone = True
                                    continue
                            elif (event.key == pygame.K_RIGHT):
                                if (self.snake1.direction != 0):
                                    self.snake1.direction = 2
                                    clickone = True
                                    continue
                        if not clicktwo:
                            if event.key == 119:
                                if self.snake2.direction != 1:
                                    self.snake2.direction = 3
                                    clicktwo = True
                                    continue
                            elif (event.key == 115):
                                if (self.snake2.direction != 3):
                                    self.snake2.direction = 1
                                    clicktwo = True
                                    continue
                            elif (event.key == 97):
                                if (self.snake2.direction != 2):
                                    self.snake2.direction = 0
                                    clicktwo = True
                                    continue
                            elif (event.key == 100):
                                if (self.snake2.direction != 0):
                                    self.snake2.direction = 2
                                    clicktwo = True
                                    continue
                pygame.display.update()
            pygame.display.update()
            if lost==1:
                self.textOnScreen(self.win, "Player 1 lost the Game with "+ str(self.snake1.points) + " points against Player 2 with "+ str(self.snake2.points)+".")
            elif lost==2:
                self.textOnScreen(self.win, "Player 2 lost the Game with "+ str(self.snake2.points) + " points against Player 1 with "+ str(self.snake1.points)+".")
            elif lost==3:
                self.textOnScreen(self.win, "You both suck! 1: "+ str(self.snake1.points) + " 2: "+ str(self.snake2.points)+".")
            else:
                self.textOnScreen(self.win, "Pause")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = True
                        if lost == 1 or lost == 2 or lost == 3:
                            lost = False
                            self.reset()
        pygame.quit()

    def getrndfood(self):
        f = [(random.randrange(40), random.randrange(35)),(random.randrange(40), random.randrange(35)),(random.randrange(40), random.randrange(35)),(random.randrange(40), random.randrange(35)),(random.randrange(40), random.randrange(35))]
        for foo in f:
            while foo in self.snake2.blocks+self.snake1.blocks:
                foo = (random.randrange(40), random.randrange(35))
        return f

    def draw(self, win):

        pygame.draw.rect(win, (0, 0, 0), (0, 0, 1000, 800), 0)

        # draw the outer line
        pygame.draw.rect(win, (128, 128, 128), (self.offsetX, self.offsetY, self.width, self.height), 1)

        surfaceText = myfont.render("Player 1 : "+str(self.snake1.points) + " Player 2 : "+str(self.snake2.points), False, (255,255,255))
        win.blit(surfaceText, (self.offsetX, 10))

        # draw the grid
        for i in range(1,40):
            pygame.draw.line(win, (128,128,128),(self.offsetX+i*self.pixelOfRect,self.offsetY),(self.offsetX+i*self.pixelOfRect,750),1)

        for i in range(1, 35):
            pygame.draw.line(win, (128, 128, 128), (self.offsetX, self.offsetY+i*self.pixelOfRect), (900, self.offsetY+i*self.pixelOfRect), 1)

        #draw the food
        for f in self.food:
            pygame.draw.rect(win, (0,255,0), (self.offsetX+f[0]*self.pixelOfRect, self.offsetY+f[1]*self.pixelOfRect, self.pixelOfRect,self.pixelOfRect), 0)


        # draw snake1
        for b in self.snake1.blocks:
            x = b[0]
            y = b[1]
            pygame.draw.rect(win, self.snake1.color, (
            self.offsetX + x * self.pixelOfRect + 1, self.offsetY + y * self.pixelOfRect + 1, self.pixelOfRect - 2,
            self.pixelOfRect - 2), 0)
        # draw snake2
        for b in self.snake2.blocks:
            x = b[0]
            y = b[1]
            pygame.draw.rect(win, self.snake2.color, (
            self.offsetX + x * self.pixelOfRect + 1, self.offsetY + y * self.pixelOfRect + 1, self.pixelOfRect - 2,
            self.pixelOfRect - 2), 0)

    def textOnScreen(self, win, text):
        surfaceText = myfont.render(text, False, (255,255,255))
        win.blit(surfaceText, (500-surfaceText.get_width()/2, 400-surfaceText.get_height()))


m = main()
m.main()