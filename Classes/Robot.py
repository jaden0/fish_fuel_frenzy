import pygame
from Classes.Wireframe import Wireframe
from math import cos, sin, sqrt, atan2
from src.helper import deg_to_rad, rad_to_deg


class Robot(object):
    def __init__(self, game_height, game_width):
        self.x = int(game_width / 2)
        self.y = int(game_height / 2)
        self.radius = 10
        self.color = (128, 128, 128)
        self.angle = 46
        self.wireframe = Wireframe(game_width, game_height)
        self.angle_step = 2
        self.v_y = 0
        self.v_x = 0
        self.friction = .01
        self.acceleration = .1
        self.max_speed = 5

    def draw(self, win, wireframe_active):
        pygame.draw.circle(win,(0,0,0),(40,40),40)

    def move(self, instruction):
        if instruction == "right":
            self.angle += self.angle_step
        if instruction == "left":
            self.angle -= self.angle_step
        if instruction == "forward":
            self.v_x += self.acceleration * cos(deg_to_rad(self.angle))
            self.v_y += self.acceleration * sin(deg_to_rad(self.angle))
            if sqrt(self.v_x ** 2 + self.v_y ** 2) >= self.max_speed:
                self.v_x -= self.acceleration * cos(deg_to_rad(self.angle))
                self.v_y -= self.acceleration * sin(deg_to_rad(self.angle))

    def drift(self):
        self.x += self.v_x
        self.y += self.v_y
        v_x = self.v_x
        v_y = self.v_y
        if sqrt(v_x ** 2 + v_y ** 2) > self.friction:
            self.v_x -= self.friction * cos(atan2(v_y, v_x))
            self.v_y -= self.friction * sin(atan2(v_y, v_x))
        else:
            self.v_x = 0
            self.v_y = 0
