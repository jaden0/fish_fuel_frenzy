import pygame
from Classes.Wireframe import Wireframe

class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_width = 800
        self.game_height = 600
        self.wireframe = Wireframe(self.game_width,self.game_height)
        self.win = pygame.display.set_mode((self.game_width,self.game_height))
        pygame.init()


    def draw(self):
        self.win.fill((230,255,255))
        self.wireframe.draw_axes(self.win)

        pygame.display.update()


    def tick(self):
        self.clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return False

        self.draw()

        return True