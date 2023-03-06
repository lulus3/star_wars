import random
import pygame
from config import Config


class Ds1:
    def __init__(self):
        self.__img = pygame.image.load("assets/estrela1.png")
        self.__rect = self.__img.get_rect()
        self.__vector_init = pygame.Vector2(0, -0.1)
        self.__xcor = Config.screen_w * 0.65
        self.__ycor = Config.screen_h * 0.32
        self.__vector = self.__vector_init.rotate(240)

    def __move(self):
        self.__xcor += self.__vector[0]
        self.__ycor += self.__vector[1]

    def __change_vector(self):
        if self.__xcor > Config.screen_w * 0.9:
            angle = random.randint(225, 315)
            self.__vector = self.__vector_init.rotate(angle)
        if self.__xcor < Config.screen_w * 0.1:
            angle = random.randint(45, 135)
            self.__vector = self.__vector_init.rotate(angle)
        if self.__ycor > Config.screen_h * 0.9:
            self.__vector[1] = -abs(self.__vector[1])
        if self.__ycor < ((Config.screen_h-60) * 0.1) + 60:
            self.__vector[1] = abs(self.__vector[1])

    def draw_img(self):
        # self.__move()
        self.__change_vector()
        self.__rect.center = (self.__xcor, self.__ycor)
        Config.screen.blit(self.__img, self.__rect)
