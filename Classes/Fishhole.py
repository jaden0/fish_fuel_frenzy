import pygame
from Classes.Fish import Fish
import random
from src.helper import deg_to_rad
from math import cos, sin
from time import time


class Fishhole(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mu = 15
        self.sigma = 10
        self.fish_distance = 30
        self.has_fish = False
        self.next_fish_time = time() + random.gauss(self.mu, self.sigma)
        self.time_left = None
        self.fish = None
        self.stop_timer = False
        self.radius = 15
        image_filename = "Images/hole_new.png"
        image = pygame.image.load(image_filename)
        image = pygame.transform.scale(image, (self.radius * 4, self.radius * 4))
        self.image = image
        self.fish_image = []
        self.fish_width = self.radius*4
        self.fish_height = self.radius *3
        self.splash_sound = pygame.mixer.Sound("Sounds/splash.mp3")
        for i in range(0,9):
            image_filename = "Images/fish_%d.png" % i
            self.fish_image.append(pygame.transform.scale(pygame.image.load(image_filename), (self.fish_width, self.fish_height)))


    def make_fish(self):
        angle = random.randint(0, 360)
        vel = 1.5 + random.random() * .5
        # fish_x = self.x + self.fish_distance * cos(deg_to_rad(angle))
        # fish_y = self.y + self.fish_distance * sin(deg_to_rad(angle))
        v_x = vel * cos(deg_to_rad(angle))
        v_y = vel * sin(deg_to_rad(angle))
        fish = Fish(self.x, self.y, v_x, v_y)
        fish.image = self.fish_image
        self.has_fish = True
        self.fish = fish
        pygame.mixer.Sound.play(self.splash_sound)

    def lose_fish(self):
        self.has_fish = False
        self.fish = None
        self.next_fish_time = time() + random.gauss(self.mu, self.sigma)

    def draw(self, win):
        win.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2))
