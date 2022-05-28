import pygame

class Fish(object):
    def __init__(self, x, y, hole_ID = 3):
        self.x = x
        self.y = y
        self.hole_ID = hole_ID

    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), 10)