import random

import pygame
from config import Config


class Nave:
    def __init__(self, photo, photo_damage, speed: int, x: float, y: float, ide: int):
        self.__photo = pygame.image.load(photo)
        self.__photo_damage = pygame.image.load(photo_damage)
        self.__photo_fixed = self.__photo
        self.__photo_damage_fixed = self.__photo_damage
        self.__surface = pygame.Surface((self.__photo.get_width(), self.__photo.get_height()))
        self.__surface.blit(self.__photo, (0, 0))
        self.__w = self.__photo.get_width()
        self.__h = self.__photo.get_height()
        self.__xcor = x
        self.__ycor = y
        self.__speed = speed
        self.__angle = 0
        self.__vecto_max = pygame.Vector2(0, -self.__speed)
        self.__vecto = pygame.Vector2(0, 0)
        self.movement = 0
        self.__time_to_recharge = 0
        self.__time_to_spawn = 0
        self.__time_to_damage = 0
        self.__time_of_animation = 0
        self.__time_of_immunity = 0
        self.__immunity = False
        self.__immunity_power = False
        self.__spin_right = False
        self.__spin_left = False
        self.__shoot = False
        self.__id = ide
        self.__life = 200
        self.__point = 0

    def move(self):
        self.__xcor += self.__vecto[0]
        self.__ycor += self.__vecto[1]

    def accelerator(self):
        if self.movement == 1:
            self.__vecto[0] += self.__vecto_max[0] * 0.03
            self.__vecto[1] += self.__vecto_max[1] * 0.03

            if abs(self.__vecto[0]) > abs(self.__vecto_max[0]):
                if self.__vecto[0] > 0:
                    self.__vecto[0] -= abs(self.__vecto[0]) * 0.04
                if self.__vecto[0] < 0:
                    self.__vecto[0] += abs(self.__vecto[0]) * 0.04

            if abs(self.__vecto[1]) > abs(self.__vecto_max[1]):
                if self.__vecto[1] > 0:
                    self.__vecto[1] -= abs(self.__vecto[1]) * 0.02
                if self.__vecto[1] < 0:
                    self.__vecto[1] += abs(self.__vecto[1]) * 0.02

    def decelerator(self):
        if self.movement == 2:
            self.__vecto[0] -= self.__vecto[0] * 0.02
            self.__vecto[1] -= self.__vecto[1] * 0.02

    def spin_right(self) -> None:
        if self.__spin_right:
            self.__angle += -self.__speed
            if self.__angle <= -360:
                self.__angle = 0
            self.__photo = pygame.transform.rotate(self.__photo_fixed, self.__angle)
            self.__photo_damage = pygame.transform.rotate(self.__photo_damage_fixed, self.__angle)
            self.__vecto_max = self.__vecto_max.rotate(self.__speed)

    def spin_left(self) -> None:
        if self.__spin_left:
            self.__angle += self.__speed
            if self.__angle >= 360:
                self.__angle = 0
            self.__photo = pygame.transform.rotate(self.__photo_fixed, self.__angle)
            self.__photo_damage = pygame.transform.rotate(self.__photo_damage_fixed, self.__angle)
            self.__vecto_max = self.__vecto_max.rotate(-self.__speed)

    def still_immunity(self, counter):
        if counter - self.__time_of_immunity < Config.immunity_time * 1000 and self.__time_of_immunity != 0:
            self.set_shoot(False)
            self.__immunity = True
        else:
            self.__immunity = False

    def healed(self, effect):
        self.__life += effect
        if self.__life > 200:
            self.__life = 200

    def new_location(self):
        n = random.choice(["up", "down", "left", "right"])
        if n == "up":
            self.__xcor = random.randint(100, Config.screen_w - 100)
            self.__ycor = 100
        elif n == "down":
            self.__xcor = random.randint(100, Config.screen_w - 100)
            self.__ycor = Config.screen_h - 100
        elif n == "left":
            self.__xcor = 100
            self.__ycor = random.randint(160, Config.screen_h - 100)
        elif n == "right":
            self.__xcor = Config.screen_w - 100
            self.__ycor = random.randint(160, Config.screen_h - 100)

    def get_immunity(self):
        return self.__immunity

    def set_time_of_immunity(self):
        self.__time_of_immunity = pygame.time.get_ticks()

    def get_time_of_immunity(self):
        return self.__time_of_immunity

    def take_damage(self):
        e = True
        if self.__immunity or self.__immunity_power:
            e = False
        if e:
            self.__life -= Config.damage_bullet

    def take_damage_asteroid(self):
        e = True
        if self.__immunity or self.__immunity_power:
            e = False
        if e:
            self.__life -= Config.damage_asteroid

    def get_immunity_power(self):
        return self.__immunity_power

    def set_immunity_power(self, tf):
        self.__immunity_power = tf

    def get_life(self):
        return self.__life

    def new_life(self):
        self.__life = 200

    def get_photo(self):
        return self.__photo

    def get_photo_damage(self):
        return self.__photo_damage

    def get_surface(self):
        return self.__surface

    def get_rect_n(self):
        rect = self.__photo.get_rect()
        rect.update(0, 0, 45, 45)
        rect.center = (self.__xcor, self.__ycor)
        return rect

    def get_id(self):
        return self.__id

    def set_movement(self, tf):
        self.movement = tf

    def set_spin_right(self, tf):
        self.__spin_right = tf

    def set_spin_left(self, tf):
        self.__spin_left = tf

    def get_x(self):
        return self.__xcor

    def get_y(self):
        return self.__ycor

    def set_x(self, x):
        self.__xcor = x

    def set_y(self, y):
        self.__ycor = y

    def get_angle(self):
        return self.__angle

    def get_width(self):
        return self.__w

    def get_height(self):
        return self.__h

    def get_vector_max(self):
        return self.__vecto_max

    def get_vector(self):
        return self.__vecto

    def set_vector_x(self, a):
        self.__vecto[0] = a

    def set_vector_y(self, a):
        self.__vecto[1] = a

    def get_shoot(self):
        return self.__shoot

    def set_shoot(self, tf):
        self.__shoot = tf

    def get_time_to_recharge(self):
        return self.__time_to_recharge

    def set_time_to_recharge(self):
        self.__time_to_recharge = pygame.time.get_ticks()

    def set_time_of_animation(self):
        self.__time_of_animation = pygame.time.get_ticks()

    def set_time_to_spawn(self):
        self.__time_to_spawn = pygame.time.get_ticks()

    def get_time_to_spawn(self):
        return self.__time_to_spawn
