import pygame
from config import Config


class Immunity:
    def __init__(self, x, y):
        self.__immunity_time_power = 0
        self.__icon_time = pygame.time.get_ticks()
        self.__photo = pygame.image.load("assets/escudo_energia.png")
        self.__rect_shield = self.__photo.get_rect()
        self.__icon_1 = pygame.image.load("assets/shield_cube.png")
        self.__icon_2 = pygame.image.load("assets/shield_cube0.png")
        self.__icon = self.__icon_1
        self.__rect_icon = self.__icon.get_rect()
        self.__n = 0
        self.__m = 1
        self.__icon_cor_x = x
        self.__icon_cor_y = y
        self.__existence_shield = False
        self.__existence_icon = True
        self.__delete_object = False
        self.__life_shield = 2
        self.__id = 10
        self.__type_power = 1

    def move_draw_power(self, x, y, counter):
        if counter - self.__immunity_time_power < Config.time_shield * 1000 and self.__life_shield > 0:
            self.__rect_shield.center = (x, y)
            Config.screen.blit(self.__photo, self.__rect_shield)
        elif (counter - self.__immunity_time_power > Config.time_shield * 1000) or self.__life_shield <= 0:
            self.__existence_shield = False
            self.__delete_object = True

    def draw_icon_shield(self):
        if self.__existence_icon:
            self.__rect_icon.center = (self.__icon_cor_x, self.__icon_cor_y)
            self.__n += self.__m
            if self.__n < 30:
                self.__icon = self.__icon_1
            elif self.__n >= 30:
                self.__icon = self.__icon_2
            if self.__n <= 0 or self.__n >= 40:
                self.__m *= -1

            Config.screen.blit(self.__icon, self.__rect_icon)

    def nave_catch_icon(self, rect, nave):
        if self.__existence_icon:
            self.__delete_icon(rect, nave)

    def __delete_icon(self, rect, nave):
        if self.__rect_icon.colliderect(rect):
            self.__existence_icon = False
            self.__existence_shield = True
            nave.set_immunity_power(True)
            self.__id = nave.get_id()
            self.__immunity_time_power = pygame.time.get_ticks()

    def get_delete(self):
        return self.__delete_object

    def set_delete(self):
        self.__delete_object = True

    def get_existence_power(self):
        return self.__existence_shield

    def get_existence_icon(self):
        return self.__existence_icon

    def get_id(self):
        return self.__id

    def get_type_power(self):
        return self.__type_power


class Healing:
    def __init__(self, x, y):
        self.__effect = Config.heal
        self.__icon_1 = pygame.image.load("assets/heath.png")
        self.__icon_2 = pygame.image.load("assets/heath0.png")
        self.__icon = self.__icon_1
        self.__rect_icon = self.__icon.get_rect()
        self.__icon_cor_x = x
        self.__icon_cor_y = y
        self.__existence_icon = True
        self.__delete_object = False
        self.__id = 9

    def draw_icon_heal(self):
        self.__rect_icon.center = (self.__icon_cor_x, self.__icon_cor_y)
        Config.screen.blit(self.__icon, self.__rect_icon)

    def nave_catch_icon(self, rect, nave):
        if self.__rect_icon.colliderect(rect):
            nave.healed(self.__effect)
            self.__delete_object = True

    def get_delete(self):
        return self.__delete_object

    def get_id(self):
        return self.__id


class NoRecharge:
    def __init__(self, x, y):
        self.__power_time = 0
        self.__icon_img = pygame.image.load("assets/relogio.png")
        self.__icon_rect = self.__icon_img.get_rect()
        self.__symbol_img = pygame.image.load("assets/symbol.png")
        self.__symbol_rect = self.__symbol_img.get_rect()
        self.__icon_cor_x = x
        self.__icon_cor_y = y
        self.__existence_icon = True
        self.__existence_symbol = False
        self.__delete_icon = False
        self.__delete_object = False
        self.__id = 8
        self.__type_power = 2

    def draw_icon(self):
        if self.__existence_icon:
            self.__icon_rect.center = (self.__icon_cor_x, self.__icon_cor_y)
            Config.screen.blit(self.__icon_img, self.__icon_rect)

    def nave_catch_icon(self, rect, nave):
        if self.__icon_rect.colliderect(rect) and self.__existence_icon:
            self.__existence_icon = False
            self.__existence_symbol = True
            nave.set_bullet_power(True)
            self.__id = nave.get_id()
            self.__power_time = pygame.time.get_ticks()

    def move_draw_power(self, x, y, counter):
        if counter - self.__power_time < Config.time_shield * 1000:
            self.__symbol_rect.center = (x+25, y-25)
            Config.screen.blit(self.__symbol_img, self.__symbol_rect)
        elif counter - self.__power_time > Config.time_shield * 1000:
            self.__existence_symbol = False
            self.__delete_object = True

    def get_delete(self):
        return self.__delete_object

    def set_delete(self):
        self.__delete_object = True

    def get_existence_power(self):
        return self.__existence_symbol

    def get_existence_icon(self):
        return self.__existence_icon

    def get_id(self):
        return self.__id

    def get_type_power(self):
        return self.__type_power
