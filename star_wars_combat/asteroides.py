import pygame
import random
from config import Config


class Asteroid:
    def __init__(self, x, y, angle):
        self.__img_1 = pygame.image.load("assets/asteroid0_3.png")
        self.__img_2 = pygame.image.load("assets/asteroid1_3.png")
        self.__img_3 = pygame.image.load("assets/asteroid2_3.png")
        self.__list_img = [self.__img_1, self.__img_2, self.__img_3]
        self.__img = self.__img_1
        self.__w = 80
        self.__h = 62
        self.__img_rect = self.__img.get_rect()
        self.__x_cor = x
        self.__y_cor = y
        self.__vector = pygame.Vector2(0, -Config.speed_asteroid)
        self.__speed = self.__vector
        self.__angle = angle
        self.__delete = False

    def move(self):
        self.__x_cor += self.__speed[0]
        self.__y_cor += self.__speed[1]

    def turn_other_angle(self, dimension):
        if dimension == "up":
            self.__speed = pygame.Vector2.rotate(self.__vector, 180)
        elif dimension == "down":
            pass
        elif dimension == "left":
            self.__speed = pygame.Vector2.rotate(self.__vector, 270)
        elif dimension == "right":
            self.__speed = pygame.Vector2.rotate(self.__vector, 90)
        self.__speed = pygame.Vector2.rotate(self.__speed, self.__angle)

    def select_img(self):
        self.__img = random.choice(self.__list_img)

    def select_angle(self):
        list_of_angles = [40, 30, 20, 10, 0, -10, -20, -30, -40]
        self.__angle = random.choice(list_of_angles)

    def draw_asteroid(self):
        self.__img_rect = self.__img.get_rect()
        self.__img_rect.center = (self.__x_cor, self.__y_cor)
        Config.screen.blit(self.__img, self.__img_rect)

    def get_x(self):
        return self.__x_cor

    def get_y(self):
        return self.__y_cor

    def get_rect_ast(self):
        return self.__img_rect

    def get_w(self):
        return self.__w

    def get_h(self):
        return self.__h

    def set_delete(self, tf):
        self.__delete = tf

    def get_delete(self):
        return self.__delete

    def get_vector(self):
        return self.__speed
