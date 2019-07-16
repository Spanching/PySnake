import pygame
from Utils import Utils

class Snake(object):
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

    def draw(self, win):
        # draw snake1
        for b in self.blocks:
            x = b[0]
            y = b[1]
            pygame.draw.rect(win, self.color, (
                Utils.offsetX + x * Utils.pixelSquare + 1, Utils.offsetY + y * Utils.pixelSquare + 1,
                Utils.pixelSquare - 2,
                Utils.pixelSquare - 2), 0)