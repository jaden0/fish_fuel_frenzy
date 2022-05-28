import pygame
from Classes.Wireframe import Wireframe
from Classes.Robot import Robot
from Classes.Fish import Fish


class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_width = 1300
        self.game_height = 700
        self.wireframe_active = True
        self.render_active = True
        self.change_ready = False
        pygame.init()
        self.wireframe = Wireframe()
        self.win = pygame.display.set_mode((self.game_width, self.game_height))
        self.robot = Robot(int(self.game_width / 2), int(self.game_height / 2), 60)
        self.fishes = [Fish(800, 400), Fish(500, 400), Fish(500, 300), Fish(850, 450), Fish(550, 450), Fish(550, 350)]
        self.fishholes = []

    def draw(self):
        self.win.fill((230, 255, 255))
        if self.render_active:
            # draw using objects
            for fish in self.fishes:
                fish.draw(self.win)
            self.robot.draw(self.win)
        if self.wireframe_active:
            for fish in self.fishes:
                self.wireframe.draw_fish(self.win, fish)

            self.wireframe.draw_robot(self.win, self.robot)

            self.wireframe.draw_axes(self.win, self.game_width / 4)

        pygame.display.update()


    def check_fish(self):
        for fishhole in self.Fishholes:
            if fishhole.has_fish:
                continue

            # is robot near hole
                # set fishhole time left, and wait until robot not near hole, then "reset"
            # if reset
                # reset next_fish_time to now plus time left

            # make new fish

    def tick(self):
        self.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            return False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.robot.move("right")
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.robot.move("left")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.robot.move("forward")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.robot.move("backwards")
        if keys[pygame.K_i] or keys[pygame.K_o]:
            if self.change_ready:
                if keys[pygame.K_i]:
                    self.wireframe_active = not self.wireframe_active
                if keys[pygame.K_o]:
                    self.render_active = not self.render_active
                self.change_ready = False
        else:
            self.change_ready = True


        self.robot.drift(self.game_width, self.game_height)
        self.fishes = self.robot.suck_fish(self.fishes, self.fishholes)
        self.draw()

        return True
