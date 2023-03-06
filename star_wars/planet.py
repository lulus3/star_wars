import pygame
from config import Config


class Planet:
    def __init__(self):
        self.__img = pygame.image.load("assets/planet0.png")
        self.__rect = self.__img.get_rect()
        self.__rect.center = (Config.screen_w * 0.3, Config.screen_h * 0.7)

    def draw_planet(self):
        Config.screen.blit(self.__img, self.__rect)