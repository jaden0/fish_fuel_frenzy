import pygame


class Fuel(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        image_filename = "Images/fuel.png"
        image = pygame.image.load(image_filename)
        image = pygame.transform.scale(image, (60, 84))
        self.image = image

    def draw(self, win):
        win.blit(self.image, (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2))
