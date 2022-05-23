import pygame
from Classes.Wireframe import Wireframe
from Classes.Robot import Robot
from Classes.Fish import Fish


class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_width = 1200
        self.game_height = 700
        self.wireframe_active = True
        self.change_ready = False
        pygame.init()
        self.wireframe = Wireframe()
        self.win = pygame.display.set_mode((self.game_width, self.game_height))
        self.Robot = Robot(int(self.game_height / 2), int(self.game_width / 2), 60)
        self.Fishes = [Fish(800, 400), Fish(500, 400), Fish(500, 300)]

    def draw(self):
        self.win.fill((230, 255, 255))
        if self.wireframe_active:
            for fish in self.Fishes:
                self.wireframe.draw_fish(self.win, fish)

            self.wireframe.draw_robot(self.win, self.Robot)

            self.wireframe.draw_axes(self.win, self.game_width / 4)
        else:
            # draw using objects
            for fish in self.Fishes:
                fish.draw(self.win)
            self.Robot.draw(self.win)
        pygame.display.update()

    def tick(self):
        self.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            return False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.Robot.move("right")
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.Robot.move("left")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.Robot.move("forward")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.Robot.move("backwards")
        if keys[pygame.K_i]:
            if self.change_ready:
                self.wireframe_active = not self.wireframe_active
                self.change_ready = False
        else:
            self.change_ready = True
        self.Robot.drift(self.game_width, self.game_height)
        self.draw()

        return True
