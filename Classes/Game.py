import pygame
from Classes.Wireframe import Wireframe

class Game(object):
    def __init__(self):
        self.wireframe = Wireframe()
        self.clock = pygame.time.Clock()
        self.game_width = 800
        self.game_height = 600
        self.win = pygame.display.set_mode((self.game_width,self.game_height))
        pygame.init()


    def draw(self):
        self.win.fill((230,255,255))
        self.wireframe.draw_arrow(self.win, 50, 50, 100, 45, (0, 0, 0))
        self.wireframe.draw_arrow(self.win, 500, 500, 200, -80, (0, 0, 255))
        self.wireframe.draw_arrow(self.win, 50, 300, 150, 0, (0, 255, 0))
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