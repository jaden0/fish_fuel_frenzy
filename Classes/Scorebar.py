import pygame

class Scorebar(object):
    def __init__(self):
        self.fuel_bar_height = 30
        self.fuel_bar_width = 1000
        self.fuel_bar_font = pygame.font.SysFont("comicsa nsms", 20)


    def draw_fuel_bar(self, win, fuel, x, y):
        fuel_color = (0, 255, 0)
        if fuel < 10:
            fuel_color = (255, 0, 0)
        text = self.fuel_bar_font.render("Diesel:", False, (0, 0, 0))
        win.blit(text, (x, y) )
        y_space = 30
        pygame.draw.rect(win, fuel_color, (x, y + y_space, self.fuel_bar_width * fuel / 100, self.fuel_bar_height))
        pygame.draw.rect(win, (0,0,0), (x,y + y_space,self.fuel_bar_width,self.fuel_bar_height), 1)