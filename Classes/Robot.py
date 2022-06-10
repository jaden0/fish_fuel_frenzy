import pygame
from Classes.Wireframe import Wireframe
from math import *
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
        self.fuel = 0
        self.fuel_count_max = 100
        self.fuel_counter = 0
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
        self.suck_fish_sound = pygame.mixer.Sound("Sounds/fish_suck_1.mp3")
        self.motor_low_sound = pygame.mixer.Sound("Sounds/motor.mp3")
        self.motor_high_sound = pygame.mixer.Sound("Sounds/motor_high.mp3")
        self.motor_low_sound.set_volume(.2)
        self.motor_high_sound.set_volume(.4)
        self.motor_running = True
        self.motor_running_high = False

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
        if self.fuel < 1:
            return ()
        if instruction == "right":  # inside each of these, you need to increase the counter
            self.angle += self.angle_step
            self.tread_1_counter -= 1
            self.tread_2_counter += 1
            changed_state = True
            self.fuel_counter += 1
        if instruction == "left":
            self.angle -= self.angle_step
            self.tread_1_counter += 1
            self.tread_2_counter -= 1
            changed_state = True
            self.fuel_counter += 1
        if instruction == "forward":
            self.v_x += self.acceleration * cos(deg_to_rad(self.angle))
            self.v_y += self.acceleration * sin(deg_to_rad(self.angle))
            if sqrt(self.v_x ** 2 + self.v_y ** 2) >= self.max_speed:
                self.v_x -= self.acceleration * cos(deg_to_rad(self.angle))
                self.v_y -= self.acceleration * sin(deg_to_rad(self.angle))
            self.tread_1_counter += 1
            self.tread_2_counter += 1
            changed_state = True
            self.fuel_counter += 3
        if instruction == "backwards":
            self.v_x -= self.back_acceleration * cos(deg_to_rad(self.angle))
            self.v_y -= self.back_acceleration * sin(deg_to_rad(self.angle))
            if sqrt(self.v_x ** 2 + self.v_y ** 2) >= self.max_speed:
                self.v_x += self.back_acceleration * cos(deg_to_rad(self.angle))
                self.v_y += self.back_acceleration * sin(deg_to_rad(self.angle))
            self.tread_1_counter -= .75
            self.tread_2_counter -= .75
            changed_state = True
            self.fuel_counter += 2
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
            if not self.motor_running_high:
                self.motor_high_sound.play()
                self.motor_running_high = True
            self.update_image()
        else:
            if self.motor_running_high:
                self.motor_high_sound.fadeout(250)
                self.motor_running_high = False

    def drift(self, game_width, score_height, game_height):
        self.fuel_counter += 1
        if self.fuel_counter >= self.fuel_count_max:
            self.fuel_counter = 0
            self.fuel -= 1
        if self.fuel < 0:
            self.fuel = 0
        if self.x + self.v_x - self.radius < 0:
            self.v_x -= 1.5 * self.v_x
        if self.y + self.v_y - self.radius < score_height:
            self.v_y -= 1.5 * self.v_y
        if self.x + self.v_x + self.radius > game_width:
            self.v_x -= 1.5 * self.v_x
        if self.y + self.v_y + self.radius > game_height:
            self.v_y -= 1.5 * self.v_y
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
        if self.angle < 0:
            self.angle += 360
        if self.angle > 360:
            self.angle -= 360


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
                pygame.mixer.Sound.play(self.suck_fish_sound)
                fishhole.lose_fish()
                self.score += 1
                print("sucked fish, total: %d" % self.score)
                print("next fish time: %d seconds" % int(fishhole.next_fish_time - time()))
        return fishholes

    def suck_fuel(self, fuel):
        sucked = False
        fishtube_x = self.x + self.fishtube_length * cos(deg_to_rad(self.angle))
        fishtube_y = self.y + self.fishtube_length * sin(deg_to_rad(self.angle))
        if (fuel.x - self.x) ** 2 + (fuel.y - self.y) ** 2 < self.radius ** 2:
            sucked = True
        if (fuel.x - fishtube_x) ** 2 + (fuel.y - fishtube_y) ** 2 < self.fishtube_radius ** 2:
            sucked = True
        if sucked:
            self.fuel += 20
        return sucked
