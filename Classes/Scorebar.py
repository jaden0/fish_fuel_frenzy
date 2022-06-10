import pygame

class Scorebar(object):
    def __init__(self, game):
        self.fuel_bar_height = 30
        self.game_width = game.game_width
        self.fuel_bar_width = game.game_width / 2 - 50
        self.fuel_bar_font = pygame.font.SysFont("comicsa nsms", 20)
        self.fish_image = pygame.transform.scale(pygame.image.load("Images/fish_3.png"), (90,3*90/4) )


    def draw_score(self, win, score, highscore):
        x = self.game_width / 2 + 60
        y = 65
        text = self.fuel_bar_font.render("Punktzahl: %d X" % score, False, (0, 0, 0))
        win.blit(self.fish_image, (x + text.get_width() , y - self.fish_image.get_height()/2-5))
        win.blit(text, (x, y - text.get_height()/2) )
        text = self.fuel_bar_font.render("Highscore: %d X" % highscore, False, (0, 0, 0))
        win.blit(self.fish_image, (x + text.get_width() + self.game_width/4, y - self.fish_image.get_height()/2-5))
        win.blit(text, (x+ self.game_width/4, y - text.get_height()/2) )

    def draw_fuel_bar(self, win, fuel):
        x = 50
        y = 20
        fuel_color = (0, 255, 0)
        if fuel < 10:
            fuel_color = (255, 0, 0)
        text = self.fuel_bar_font.render("Benzin:", False, (0, 0, 0))
        win.blit(text, (x, y) )
        y_space = 30
        pygame.draw.rect(win, fuel_color, (x, y + y_space, self.fuel_bar_width * fuel / 100, self.fuel_bar_height))
        pygame.draw.rect(win, (0,0,0), (x,y + y_space,self.fuel_bar_width,self.fuel_bar_height), 1)