import pygame
from math import cos, sin
from src.helper import deg_to_rad, rad_to_deg

class Wireframe(object):
    def __init__(self, game_width, game_height):
        self.game_width = game_width
        self.game_height = game_height
    
    def draw_arrow(self,win,x,y,length,theta,color):
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
        pygame.draw.line(win, color, (x_i, y_i), (x_f, y_f), 2)
        pygame.draw.line(win, color, (x_l, y_l), (x_f, y_f), 2)
        pygame.draw.line(win, color, (x_r, y_r), (x_f, y_f), 2)

    def draw_axes(self,win):
        arrow_length = self.game_height / 4
        self.draw_arrow(win, 25, 25, arrow_length, 0, (0, 0, 0))
        self.draw_arrow(win, 25, 25, arrow_length, 90, (0, 0, 0))
        font = pygame.font.SysFont("comicsa nsms",20)
        text = font.render("X",False, (0,0,0))
        win.blit( text, (25+ arrow_length+ 15 - text.get_width() / 2, 25 - text.get_height() / 2  ) )
        text = font.render("Y",False, (0,0,0))
        win.blit( text, ( 25 - text.get_width() / 2 ,25+ arrow_length+ 15 - text.get_height() / 2 ) )