import pygame
from Classes.Wireframe import Wireframe
from Classes.Robot import Robot
from Classes.Fishhole import Fishhole
from time import time
from Classes.Fuel import Fuel

class Game(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_width = 1300
        self.game_height = 700
        self.min_robot_distance = 150
        self.wireframe_active = True
        self.render_active = False
        self.change_ready = False
        pygame.init()
        self.font = pygame.font.SysFont("comicsa nsms", 40)
        self.wireframe = Wireframe()
        self.win = pygame.display.set_mode((self.game_width, self.game_height))
        self.robot = Robot(int(self.game_width / 2), int(self.game_height / 2), 60)
        self.fishholes = [Fishhole(100, 300), Fishhole(1100, 500), Fishhole(300, 600), Fishhole(600, 400),
                          Fishhole(1150, 150)]
        self.fuel = Fuel(500, 500)

    def draw(self):
        self.win.fill((230, 255, 255))

        if self.render_active:
            # draw using objects
            for fishhole in self.fishholes:
                if fishhole.has_fish:
                    fishhole.fish.draw(self.win)
        if self.wireframe_active:
            self.wireframe.draw_axes(self.win, self.game_width / 4)
            self.wireframe.draw_info(50, 50, self)
            if self.fuel is not None:
                self.wireframe.draw_fuel(self.win, self.fuel)
            for fishhole in self.fishholes:
                self.wireframe.draw_fishhole(self.win, fishhole)
            self.robot.draw(self.win)
            self.wireframe.draw_robot(self.win, self.robot)
        pygame.display.update()

    def draw_game_over(self):
        self.win.fill((0, 0, 139))
        text = self.font.render("GAME OVER", False, (200, 0, 0))
        self.win.blit(text, (int(self.game_width / 2 - text.get_width() / 2), int(self.game_height / 2 - text.get_height() / 2)))
        pygame.display.update()


    def check_fuel(self):
        if self.fuel is None:
            return()
        if self.robot.suck_fuel(self.fuel):
            self.fuel = None
            #TODO: start new fuel timer and make new fuel


    def check_fish(self):
        for fishhole in self.fishholes:
            if fishhole.has_fish:
                continue

            # is robot near hole
            if (self.robot.x - fishhole.x) ** 2 + (self.robot.y - fishhole.y) ** 2 < self.min_robot_distance ** 2:

                if not fishhole.stop_timer:
                    fishhole.time_left = fishhole.next_fish_time - time()
                    print("too close")
                    print("stopping timer, with %.0f second(s)" % fishhole.time_left)
                    fishhole.stop_timer = True
            elif fishhole.stop_timer:
                fishhole.stop_timer = False
                fishhole.next_fish_time = time() + fishhole.time_left
                print("starting timer with %.0f second(s) left" % fishhole.time_left)

            # make new fish
            if time() > fishhole.next_fish_time and not fishhole.stop_timer:
                fishhole.make_fish()


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
        if keys[pygame.K_i]:
            if self.change_ready:
                self.wireframe_active = not self.wireframe_active
                self.render_active = not self.render_active
                self.change_ready = False
        else:
            self.change_ready = True

        for fishhole in self.fishholes:
            if fishhole.has_fish:
                fishhole.fish.slide(self)

        if self.robot.fuel < 1 and self.robot.v_x == 0 and self.robot.v_y == 0:
            self.draw_game_over()
        else:
            self.robot.drift(self.game_width, self.game_height)
            self.fishholes = self.robot.suck_fish(self.fishholes)
            self.check_fish()
            self.check_fuel()
            self.draw()
        return True
