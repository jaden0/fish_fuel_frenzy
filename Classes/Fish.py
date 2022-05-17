import pygame

class Fish(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), 10)