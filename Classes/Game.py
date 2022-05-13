import pygame
from Classes.Wireframe import Wireframe
from Classes.Robot import Robot


class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_width = 800
        self.game_height = 600
        self.wireframe_active = True
        self.change_ready = False
        pygame.init()
        self.wireframe = Wireframe(self.game_width, self.game_height)
        self.win = pygame.display.set_mode((self.game_width, self.game_height))
        self.Robot = Robot(self.game_height, self.game_width)

    def draw(self):
        self.win.fill((230, 255, 255))
        if self.wireframe_active:

            self.wireframe.draw_robot(self.win,self.Robot)

            self.wireframe.draw_axes(self.win)
        else:
            # draw using objects
            self.Robot.draw(self.win, self.wireframe_active)
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
        if keys[pygame.K_i]:
            print( "i")
            if self.change_ready:
                print( "changing")
                self.wireframe_active = not self.wireframe_active
                self.change_ready = False
        else:
            self.change_ready = True
        self.Robot.drift()
        self.draw()


        return True
