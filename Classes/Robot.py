import pygame
from Classes.Wireframe import Wireframe
from math import cos, sin
from src.helper import deg_to_rad, rad_to_deg

class Robot(object):
    def __init__(self, game_height, game_width):
        self.x = int(game_width / 2)
        self.y = int(game_height / 2)
        self.radius = 35
        self.color = (128, 128, 128)
        self.angle = 46
        self.arrow_maker = Wireframe(game_width, game_height)
        self.angle_step = 2
        self.v_y = 0
        self.v_x = 0
        self.friction = .1
        self.acceleration = .2
        self.max_speed = .5
        pygame.init()

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 0)
        self.arrow_maker.draw_arrow(win, self.x, self.y, 100, self.angle, self.color)

    def move(self, instruction):
        if instruction == "right":
            self.angle += self.angle_step
        if instruction == "left":
            self.angle -= self.angle_step
        if instruction == "forward":
            self.v_x += self.acceleration * cos(deg_to_rad(self.angle))
            self.v_y += self.acceleration * sin(deg_to_rad(self.angle))
            if self.v_x >= self.max_speed:
                self.v_x = self.max_speed
            if self.v_y >= self.max_speed:
                self.v_y = self.max_speed

    def drift(self):
        self.x += self.v_x
        self.y += self.v_y
#        if self.v_x < self.friction:
#            self.v_x = 0
#        else:
#            self.v_x -= self.friction
#        if self.v_y < .1:
#            self.v_y = 0
#        else:
#            self.v_y -= self.friction
