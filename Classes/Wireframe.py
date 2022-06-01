import pygame
from math import cos, sin, atan2, sqrt
from src.helper import deg_to_rad, rad_to_deg


class Wireframe(object):
    def __init__(self):
        self.vector_font = pygame.font.SysFont("comicsa nsms", 20)
        self.info_font = pygame.font.SysFont("consolas", 20)

    def draw_arrow(self, win, x, y, length, theta, color):
        delta_theta = 4
        per_length = .9
        x_i = x
        y_i = y
        x_f = x_i + length * cos(deg_to_rad(theta))
        y_f = y_i + length * sin(deg_to_rad(theta))
        x_l = x_i + per_length * length * cos(deg_to_rad(theta - delta_theta))
        y_l = y_i + per_length * length * sin(deg_to_rad(theta - delta_theta))
        x_r = x_i + per_length * length * cos(deg_to_rad(theta + delta_theta))
        y_r = y_i + per_length * length * sin(deg_to_rad(theta + delta_theta))
        pygame.draw.line(win, color, (x_i, y_i), (x_f, y_f), 3)
        pygame.draw.line(win, color, (x_l, y_l), (x_f, y_f), 3)
        pygame.draw.line(win, color, (x_r, y_r), (x_f, y_f), 3)

    def draw_axes(self, win, arrow_length):
        self.draw_arrow(win, 25, 25, arrow_length, 0, (0, 0, 0))
        self.draw_arrow(win, 25, 25, arrow_length, 90, (0, 0, 0))
        font = pygame.font.SysFont("comicsa nsms", 20)
        text = font.render("X", False, (0, 0, 0))
        win.blit(text, (25 + arrow_length + 15 - text.get_width() / 2, 25 - text.get_height() / 2))
        text = font.render("Y", False, (0, 0, 0))
        win.blit(text, (25 - text.get_width() / 2, 25 + arrow_length + 15 - text.get_height() / 2))


    def draw_robot(self, win, robot):
        pygame.draw.circle(win, robot.color, (robot.x, robot.y), robot.radius, 1)
        fishtube_x = robot.x + robot.fishtube_length * cos(deg_to_rad(robot.angle))
        fishtube_y = robot.y + robot.fishtube_length * sin(deg_to_rad(robot.angle))
        pygame.draw.circle(win, robot.color, (fishtube_x, fishtube_y), robot.fishtube_radius, 1)
        self.draw_arrow(win, robot.x, robot.y, 100, robot.angle, robot.color)
        drift_angle = atan2( robot.v_y, robot.v_x)
        drift_vel = sqrt( robot.v_y**2 +robot.v_x**2 )
        self.draw_vectors(win, robot.x, robot.y, rad_to_deg(drift_angle), drift_vel*40, (255,0,0), "Vel")
        self.draw_vectors(win, robot.x, robot.y, rad_to_deg(drift_angle) + 180,  40*(drift_vel>0), (0,255,0), "f"  )


    def draw_vectors(self, win, x, y, angle, length, color, input_text):
        self.draw_arrow(win, x, y, length, angle, color)
        x_text = x + (length + 20)  * cos(deg_to_rad(angle))
        y_text = y + (length + 20)  * sin(deg_to_rad(angle))
        text = self.vector_font.render(input_text, False, color)
        win.blit(text, (x_text - text.get_width() / 2, y_text - text.get_height() / 2))
        pygame.draw.circle(win, color, (x, y), length, 2)
        x_arrow_tip = x + length  * cos(deg_to_rad(angle))
        y_arrow_tip = y + length  * sin(deg_to_rad(angle))
        pygame.draw.line(win, color, (x_arrow_tip, y), (x, y), 1)
        pygame.draw.line(win, color, (x_arrow_tip, y), (x_arrow_tip, y_arrow_tip), 1)

    def draw_fishhole(self, win, fishhole):
        pygame.draw.circle(win, (0, 0, 0), (fishhole.x, fishhole.y), 15, 1)
        text = self.vector_font.render("Loch", False, (0, 0, 0))
        win.blit(text, (fishhole.x - text.get_width() / 2, fishhole.y + 15))
        if fishhole.has_fish:
            fish = fishhole.fish
            pygame.draw.circle(win, (0, 0, 255), (fish.x, fish.y), fish.radius)
            text = self.vector_font.render("Fisch", False, (0, 0, 255))
            win.blit(text, (fish.x - text.get_width() / 2, fish.y + 15))

    def draw_info(self, x, y, game):
        delta_y = 20
        text = self.info_font.render("Roboter pos: x: %d y: %d" % (game.robot.x, game.robot.y), False, (0, 0, 0))
        game.win.blit(text, (x, y + 0 * delta_y))
        text = self.info_font.render("Roboter Winkel: %d" % game.robot.angle, False, (0, 0, 0))
        game.win.blit(text, (x, y + 1 * delta_y))
        vel = sqrt(game.robot.v_x**2 + game.robot.v_y**2)*10
        vel_angle = rad_to_deg(atan2(game.robot.v_y, game.robot.v_x))
        text = self.info_font.render("Geschwindigkeit: %d,  %d grad" % (vel,vel_angle), False, (0, 0, 0))
        game.win.blit(text, (x, y + 2 * delta_y))
        text = self.info_font.render("Punkte: %d" % game.robot.score, False, (0, 0, 0))
        game.win.blit(text, (x, y + 3 * delta_y))
        fish_on_screen = sum([i.has_fish for i in game.fishholes])
        text = self.info_font.render("Fish on screen: %d" % fish_on_screen, False, (0, 0, 0))
        game.win.blit(text, (x, y + 4 * delta_y))
        text = self.info_font.render("Fuel: %d" % game.robot.fuel, False, (0, 0, 0))
        game.win.blit(text, (x, y + 5 * delta_y))

    def draw_fuel(self, win, fuel):
        pygame.draw.rect(win, (255, 0, 0), (fuel.x - 10, fuel.y - 14, 20, 28), 4)
        text = self.vector_font.render("Diesel", False, (255, 0, 0))
        win.blit(text, (fuel.x - text.get_width() / 2, fuel.y + 15))