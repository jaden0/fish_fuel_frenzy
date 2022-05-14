import pygame
from Classes.Wireframe import Wireframe
from math import cos, sin, sqrt, atan2
from src.helper import deg_to_rad, rad_to_deg


class Robot(object):
    def __init__(self, x,y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (128, 128, 128)
        self.angle = 46
        self.wireframe = Wireframe()
        self.angle_step = 2
        self.v_y = 0
        self.v_x = 0
        self.friction = .01
        self.acceleration = .1
        self.max_speed = 5
        self.images = []
        for i in range(0,3):
            temp = []
            for j in range(0,3):
                image_filename = "Images/robot_%d_%d.png" % (i,j)
                image = pygame.image.load(image_filename)

                temp.append(image)

            self.images.append(temp)
        print( "robot constructed")
        self.image = None
        self.update_image()

    def update_image(self):
        self.image = self.images[0][0]


    def draw(self, win: pygame.Surface):
        pygame.draw.circle(win,(0,0,0),(self.x,self.y),40)
        win.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2))
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
