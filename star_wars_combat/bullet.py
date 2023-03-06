import pygame


class Bullet:
    def __init__(self, photo, x, y, x_speed, y_speed, life, ide, angle):
        self.photo = photo
        self.rect = self.photo.get_rect()
        self.img = photo
        self.surface = pygame.Surface((self.photo.get_width(), self.photo.get_height()))
        self.x_position = x
        self.y_position = y
        self.speed_x = x_speed
        self.speed_y = y_speed
        self.life = life
        self.__id = ide
        self.angle = angle

    def move(self):
        self.x_position += self.speed_x
        self.y_position += self.speed_y

    def get_id(self):
        return self.__id

    def get_rect(self):
        rect = self.photo.get_rect()
        return rect
