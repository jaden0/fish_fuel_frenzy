import pygame
from math import cos, sin
from src.helper import deg_to_rad, rad_to_deg

class Wireframe(object):
    def __init__(self):
        pass
    
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