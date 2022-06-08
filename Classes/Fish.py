import pygame
from math import sin, cos, atan2

class Fish(object):
    def __init__(self, x, y, v_x, v_y):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.radius = 10
        self.image = []
        self.image_counter = 0
        self.image_count_max = 3
        self.image_index = 0

    def slide(self, game):
        self.x += self.v_x
        self.y += self.v_y
        angle = atan2(self.v_y, self.v_x)
        vel = self.v_x**2 + self.v_y**2
        if self.x + self.v_x - self.radius < 0:
            self.v_x -= 1.5 * self.v_x
        if self.y + self.v_y - self.radius < game.score_height:
            self.v_y -= 1.5 * self.v_y
        if self.x + self.v_x + self.radius > game.game_width:
            self.v_x -= 1.5 * self.v_x
        if self.y + self.v_y + self.radius > game.game_height:
            self.v_y -= 1.5 * self.v_y
        if vel < 1:
            self.v_x = 0
            self.v_y = 0
        else:
            friction = .01
            self.v_x -= friction * cos(angle)
            self.v_y -= friction * sin(angle)



    def draw(self, win):
        #pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), 10)
        self.image_counter += 1
        if self.image_counter >= self.image_count_max:
            self.image_counter = 0
            self.image_index += 1
            if self.image_index >= 9:
                self.image_index = 0
        win.blit(self.image[self.image_index], (self.x - self.image[self.image_index].get_width() / 2,
                                                self.y - self.image[self.image_index].get_height()/2))