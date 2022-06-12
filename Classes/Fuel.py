import pygame
from time import time
import random
from math import sin


class Fuel(object):
    def __init__(self, game):
        self.game_width = game.game_width
        self.game_height = game.game_height
        self.score_height = game.score_height
        self.x = 50
        self.y = 500
        self.y_shift = 0
        self.visible = True
        self.suckable = True
        image_filename = "Images/fuel.png"
        image = pygame.image.load(image_filename)
        image = pygame.transform.scale(image, (40, 63))
        self.image = image
        self.parachute_image = pygame.image.load( "Images/parachute.png")
        self.parachute_image = pygame.transform.scale(self.parachute_image, (60,63))
        self.fuel_time_scaler = 5
        self.fuel_time_scaler2 = 10
        self.next_fuel_time = None
        self.fall_timer = 0
        self.appear_sound = pygame.mixer.Sound("Sounds/new_can.mp3")
        self.suck_sound = pygame.mixer.Sound("Sounds/get_fuel.mp3")
        print( "only once!")
        self.drop_fuel()

    def new_location(self):
        print( "this happened" )
        self.x = random.randint(int(self.image.get_width()/2), int(self.game_width -self.image.get_width()/2))
        self.y = random.randint(int(self.score_height+self.image.get_height()/2), int(self.game_height-self.image.get_height()/2))
        self.next_fuel_time = time() + random.randint(self.fuel_time_scaler, self.fuel_time_scaler2)
        self.fuel_time_scaler2 += 5
        self.fuel_time_scaler += 1
        print( "next fuel time: %d seconds" % (self.next_fuel_time - time()))

    def land(self):
        self.state = "landed"
        pygame.mixer.Sound.play(self.appear_sound)

    def drop_fuel(self):
        self.new_location()
        self.state = "dropping"
        self.fall_timer = 300

    def fall(self, win):
        self.fall_timer -= 1
        self.y_shift = self.fall_timer * 2
        self.x_shift = sin( self.fall_timer / 20 ) * 200
        if self.fall_timer < 1:
            self.land()

    def sucked(self):
        pygame.mixer.Sound.play(self.suck_sound)
        self.state = "waiting"
        self.new_location()

    def draw(self, win):
        if self.state in ["dropping", "landed"]:
            shadow_width = self.fall_timer / 10  + self.image.get_width()*1.2
            #color = (int(80+125*self.fall_timer/200),int(80+125* self.fall_timer/200),int(100+105*self.fall_timer/200))
            color = (80,80,100)
            pygame.draw.ellipse(win,color, (self.x - shadow_width/2- self.x_shift, self.y + self.image.get_height()/2 - 10, shadow_width, shadow_width/4 ))
            w = self.image.get_width() * (1 + self.fall_timer / 100)
            h = self.image.get_height()* (1 + self.fall_timer / 100)
            win.blit(pygame.transform.scale(self.image, (w,h)), (int(self.x - self.image.get_width() / 2 - self.x_shift), self.y - self.image.get_height() / 2 - self.y_shift))
            if self.state == "dropping":
                wp = self.parachute_image.get_width() * (1 + self.fall_timer / 100)
                hp = self.parachute_image.get_height() * (1 + self.fall_timer / 100)
                win.blit(pygame.transform.scale(self.parachute_image, (wp,hp)),(int(self.x - self.image.get_width() / 2 - self.x_shift - w*.35),self.y - self.image.get_height() / 2 - self.y_shift- hp + h*.15))