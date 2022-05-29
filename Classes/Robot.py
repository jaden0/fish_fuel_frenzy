import pygame
from Classes.Wireframe import Wireframe
from math import cos, sin, sqrt, atan2
from src.helper import deg_to_rad, rad_to_deg
from time import time


class Robot(object):
    def __init__(self, x, y, radius):
        self.score = 0
        self.x = x
        self.y = y
        self.radius = radius
        self.fishtube_radius = radius * .5
        self.fishtube_length = radius * 1.
        self.color = (128, 128, 128)
        self.angle = -46
        self.tread_1_state = 0
        self.tread_2_state = 0
        self.tread_count_max = 3
        self.tread_1_counter = int(self.tread_count_max / 2)
        self.tread_2_counter = int(self.tread_count_max / 2)
        self.wireframe = Wireframe()
        self.angle_step = 2
        self.v_y = 0
        self.v_x = 0
        self.friction = .05
        self.acceleration = .2
        self.back_acceleration = self.acceleration / 2
        self.max_speed = 10
        self.images = []
        for i in range(0, 3):
            temp = []
            for j in range(0, 3):
                image_filename = "Images/robot_%d_%d.png" % (i, j)
                image = pygame.image.load(image_filename)
                image = pygame.transform.scale(image, (self.radius * 2, self.radius * 2))
                image = pygame.transform.rotate(image, -90)
                temp.append(image)

            self.images.append(temp)
        print("robot constructed")
        self.image = self.images[0][0]
        self.update_image()

    def update_image(self):
        self.image = self.images[self.tread_2_state][self.tread_1_state]
        self.image = pygame.transform.rotate(self.image, -self.angle)

    def draw(self, win: pygame.Surface):
        win.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2))

    def move(self, instruction):
        changed_state = False
        if instruction == "right":  # inside each of these, you need to increase the counter
            self.angle += self.angle_step
            self.tread_1_counter -= 1
            self.tread_2_counter += 1
            changed_state = True
        if instruction == "left":
            self.angle -= self.angle_step
            self.tread_1_counter += 1
            self.tread_2_counter -= 1
            changed_state = True
        if instruction == "forward":
            self.v_x += self.acceleration * cos(deg_to_rad(self.angle))
            self.v_y += self.acceleration * sin(deg_to_rad(self.angle))
            if sqrt(self.v_x ** 2 + self.v_y ** 2) >= self.max_speed:
                self.v_x -= self.acceleration * cos(deg_to_rad(self.angle))
                self.v_y -= self.acceleration * sin(deg_to_rad(self.angle))
            self.tread_1_counter += 1
            self.tread_2_counter += 1
            changed_state = True
        if instruction == "backwards":
            self.v_x -= self.back_acceleration * cos(deg_to_rad(self.angle))
            self.v_y -= self.back_acceleration * sin(deg_to_rad(self.angle))
            if sqrt(self.v_x ** 2 + self.v_y ** 2) >= self.max_speed:
                self.v_x += self.back_acceleration * cos(deg_to_rad(self.angle))
                self.v_y += self.back_acceleration * sin(deg_to_rad(self.angle))
            self.tread_1_counter -= .75
            self.tread_2_counter -= .75
            changed_state = True
        if self.tread_1_counter < 0:
            self.tread_1_state -= 1
            changed_state = True
            self.tread_1_counter = self.tread_count_max
        if self.tread_1_counter > self.tread_count_max:
            self.tread_1_state += 1
            changed_state = True
            self.tread_1_counter = 0
        if self.tread_2_counter < 0:
            self.tread_2_state -= 1
            changed_state = True
            self.tread_2_counter = self.tread_count_max
        if self.tread_2_counter > self.tread_count_max:
            self.tread_2_state += 1
            changed_state = True
            self.tread_2_counter = 0
        if self.tread_2_state > 2:
            self.tread_2_state = 0
        if self.tread_1_state > 2:
            self.tread_1_state = 0
        if self.tread_2_state < 0:
            self.tread_2_state = 2
        if self.tread_1_state < 0:
            self.tread_1_state = 2
        # if counter is less than 0, or more than max time steps, then change state, and counter
        if changed_state:
            self.update_image()

    def drift(self, game_width, game_height):
        if self.x + self.v_x - self.radius < 0:
            self.v_x -= 2 * self.v_x
        if self.y + self.v_y - self.radius < 0:
            self.v_y -= 2 * self.v_y
        if self.x + self.v_x + self.radius > game_width:
            self.v_x -= 2 * self.v_x
        if self.y + self.v_y + self.radius > game_height:
            self.v_y -= 2 * self.v_y
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
    def suck_fish(self, fishholes):
        for fishhole in fishholes:
            if fishhole.has_fish:
                fish = fishhole.fish
            else:
                continue
            sucked = False
            fishtube_x = self.x + self.fishtube_length * cos(deg_to_rad(self.angle))
            fishtube_y = self.y + self.fishtube_length * sin(deg_to_rad(self.angle))
            if (fish.x - self.x) ** 2 + (fish.y - self.y) ** 2 < self.radius ** 2:
                sucked = True
            if (fish.x - fishtube_x) ** 2 + (fish.y - fishtube_y) ** 2 < self.fishtube_radius ** 2:
                sucked = True
            if sucked:
                fishhole.lose_fish()
                self.score += 1
                print("sucked fish, total: %d" % self.score)
                print( "next fish time: %d seconds" % int( fishhole.next_fish_time - time()))