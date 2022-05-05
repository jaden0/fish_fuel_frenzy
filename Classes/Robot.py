import pygame
from Classes.Wireframe import Wireframe


class Robot(object):
    def __init__(self, game_height, game_width):
        self.x = int(game_width / 2)
        self.y = int(game_height / 2)
        self.radius = 35
        self.color = (128, 128, 128)
        self.angle = 46
        self.arrow_maker = Wireframe(game_width, game_height)
        self.angle_step = 2
        pygame.init()

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 0)
        self.arrow_maker.draw_arrow(win, self.x, self.y, 100, self.angle, self.color)

    def move(self, instruction):
        if instruction == "right":
            self.angle += self.angle_step
        if instruction == "left":
            self.angle -= self.angle_step
