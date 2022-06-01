import pygame
from math import sin, cos, atan2

class Fish(object):
    def __init__(self, x, y, v_x, v_y):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.radius = 10

    def slide(self, game):
        self.x += self.v_x
        self.y += self.v_y
        angle = atan2(self.v_y, self.v_x)
        vel = self.v_x**2 + self.v_y**2
        if self.x + self.v_x - self.radius < 0:
            self.v_x -= 1.5 * self.v_x
        if self.y + self.v_y - self.radius < 0:
            self.v_y -= 1.5 * self.v_y
        if self.x + self.v_x + self.radius > game.game_width:
            self.v_x -= 1.5 * self.v_x
        if self.y + self.v_y + self.radius > game.game_height:
            self.v_y -= 1.5 * self.v_y
        if vel < 1:
            self.v_x = 0
            self.v_y = 0
        else:
            friction = .1
            self.v_x -= friction * cos(angle)
            self.v_y -= friction * sin(angle)



    def draw(self, win):
        pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), 10)