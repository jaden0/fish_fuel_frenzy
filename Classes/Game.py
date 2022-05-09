import pygame
from Classes.Wireframe import Wireframe
from Classes.Robot import Robot


class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_width = 1000
        self.game_height = 1000
        self.wireframe = Wireframe(self.game_width, self.game_height)
        self.win = pygame.display.set_mode((self.game_width, self.game_height))
        self.Robot = Robot(self.game_height, self.game_width)
        pygame.init()

    def draw(self):
        self.win.fill((230, 255, 255))
        self.wireframe.draw_axes(self.win)
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
        if keys[pygame.K_RIGHT]:
            self.Robot.move("right")
        if keys[pygame.K_LEFT]:
            self.Robot.move("left")
        if keys[pygame.K_UP]:
            self.Robot.move("forward")

        self.Robot.drift()
        self.draw()

        return True
