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
        self.mu = 5
        self.sigma = 5
        self.fish_distance = 10
        self.has_fish = False
        self.next_fish_time = time() + random.gauss(self.mu, self.sigma)
        self.time_left = None
        self.fish = None
        self.stop_timer = False



    def make_fish(self):
        angle = random.randint(0, 360)
        fish_x = self.x + self.fish_distance * cos(deg_to_rad(angle))
        fish_y = self.y + self.fish_distance * sin(deg_to_rad(angle))
        fish = Fish(fish_x, fish_y)
        self.has_fish = True
        self.fish = fish
        print( "new fish")

    def lose_fish(self):
        self.has_fish = False
        self.fish = None
        self.next_fish_time = time() + random.gauss(self.mu, self.sigma)
