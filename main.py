import pygame
import random

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

class Snake:
    def __init__(self):
        self.blocks = [(20,20),(21,20)]
        self.color = (255,0,0)
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

    def collides(self):
        for i, b1 in enumerate(self.blocks,1):
            if b1[0]<0 or b1[0]>39 or b1[1]<0 or b1[1]>34:
                return True
            for j in range(i, len(self.blocks)-1):
                b2 = self.blocks[j]
                if b1[0] == b2[0] and b1[1] == b2[1]:
                    return True
        return False

    def eats(self, food):
        for b in self.blocks:
            if b[0] == food[0] and b[1]== food[1]:
                self.food.append(food)
                return True
        return False


class main:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.win = pygame.display.set_mode((1000, 800))
        self.width = 800
        self.height = 700
        self.snake = Snake()
        self.food = (-1,-1)
        self.isfood = False
        self.pixelOfRect = 20
        self.offsetX = 100
        self.offsetY = 50
        self.width = 800
        self.height = 700
        self.points = 0
        self.timer = 0
        pygame.display.set_caption('Snake')

    def main(self):
        run = True
        while(run):
            self.clock.tick(8)
            self.timer += 1
            if self.timer >= 230:
                self.timer = 0
                self.points+=1
            self.snake.move()
            if not(self.isfood):
                self.food = self.getrndfood()
                self.isfood = True
            if self.snake.collides():
                run = False
                print("You Lost")
                break
            if self.snake.eats(self.food):
                self.points+=10
                self.isfood = False
            self.draw(self.win)
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    run= False
                if(event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_UP):
                        if (self.snake.direction != 1):
                            self.snake.direction = 3
                            break
                    elif (event.key == pygame.K_DOWN):
                        if (self.snake.direction != 3):
                            self.snake.direction = 1
                            break
                    elif (event.key == pygame.K_LEFT):
                        if (self.snake.direction != 2):
                            self.snake.direction = 0
                            break
                    elif (event.key == pygame.K_RIGHT):
                        if (self.snake.direction != 0):
                            self.snake.direction = 2
                            break
            pygame.display.update()
        pygame.quit()

    def getrndfood(self):
        f = (random.randrange(40), random.randrange(35))
        while f in self.snake.blocks:
            f = (random.randrange(40), random.randrange(35))
        return f

    def draw(self, win):

        pygame.draw.rect(win, (0, 0, 0), (0, 0, 1000, 800), 0)

        # draw the outer line
        pygame.draw.rect(win, (128, 128, 128), (self.offsetX, self.offsetY, self.width, self.height), 1)

        surfaceText = myfont.render("Score: "+str(self.points), False, (255,255,255))
        win.blit(surfaceText, (self.offsetX, 10))

        # draw the grid
        for i in range(1,40):
            pygame.draw.line(win, (128,128,128),(self.offsetX+i*self.pixelOfRect,self.offsetY),(self.offsetX+i*self.pixelOfRect,750),1)

        for i in range(1, 35):
            pygame.draw.line(win, (128, 128, 128), (self.offsetX, self.offsetY+i*self.pixelOfRect), (900, self.offsetY+i*self.pixelOfRect), 1)

        #draw the food
        pygame.draw.rect(win, (0,255,0), (self.offsetX+self.food[0]*self.pixelOfRect, self.offsetY+self.food[1]*self.pixelOfRect, self.pixelOfRect,self.pixelOfRect), 0)


        # draw snake
        for i, b in enumerate(self.snake.blocks):
            x = b[0]
            y = b[1]
            pygame.draw.rect(win, self.snake.color, (self.offsetX+x*self.pixelOfRect, self.offsetY+y*self.pixelOfRect, self.pixelOfRect, self.pixelOfRect), 0)


    def textOnScreen(self, win, text):
        surfaceText = myfont.render(text, False, (255,255,255))
        win.blit(surfaceText, (500-surfaceText.get_width()/2, 400-surfaceText.get_height()))


m = main()
m.main()
