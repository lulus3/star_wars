import sys
from config import Config
import pygame


def keys_down(event, list_of_naves):

    if event.key == pygame.K_ESCAPE:
        sys.exit()

    for nave in list_of_naves:
        if nave.get_id() == 0:
            move_front = pygame.K_w
            spin_left = pygame.K_a
            spin_right = pygame.K_d
            stop = pygame.K_s
            shoot = pygame.K_r

        elif nave.get_id() == 1:
            move_front = pygame.K_UP
            spin_left = pygame.K_LEFT
            spin_right = pygame.K_RIGHT
            stop = pygame.K_DOWN
            shoot = pygame.K_9

        elif nave.get_id() == 2:
            move_front = pygame.K_t
            spin_left = pygame.K_f
            spin_right = pygame.K_h
            stop = pygame.K_g
            shoot = pygame.K_u

        elif nave.get_id() == 3:
            move_front = pygame.K_i
            spin_left = pygame.K_j
            spin_right = pygame.K_l
            stop = pygame.K_k
            shoot = pygame.K_p
        else:
            move_front = 0
            spin_right = 0
            spin_left = 0
            stop = 0
            shoot = 0

        if event.key == move_front:
            nave.set_movement(1)
        if event.key == spin_right:
            nave.set_spin_right(True)
        if event.key == spin_left:
            nave.set_spin_left(True)
        if event.key == stop:
            nave.set_movement(2)
        if event.key == shoot:
            nave.set_shoot(True)


def keys_up(event, list_of_naves):
    for nave in list_of_naves:
        if nave.get_id() == 0:
            move_front = pygame.K_w
            spin_left = pygame.K_a
            spin_right = pygame.K_d

        elif nave.get_id() == 1:
            move_front = pygame.K_UP
            spin_left = pygame.K_LEFT
            spin_right = pygame.K_RIGHT

        elif nave.get_id() == 2:
            move_front = pygame.K_t
            spin_left = pygame.K_f
            spin_right = pygame.K_h

        elif nave.get_id() == 3:
            move_front = pygame.K_i
            spin_left = pygame.K_j
            spin_right = pygame.K_l
        else:
            move_front = 0
            spin_right = 0
            spin_left = 0

        if event.key == move_front:
            nave.set_movement(0)
        if event.key == spin_right:
            nave.set_spin_right(False)
        if event.key == spin_left:
            nave.set_spin_left(False)


def hatdown(event, list_of_tank):
    n = 7
    for tank in list_of_tank:
        if len(list_of_tank) == 2 and tank.get_id() == 2:
            n = 1
        if tank.get_id() == event.joy or n == event.joy:
            if event.value[0] == 1:
                tank.set_spin_right(True)
            if event.value[0] == 0:
                tank.set_spin_right(False)
            if event.value[0] == -1:
                tank.set_spin_left(True)
            if event.value[0] == 0:
                tank.set_spin_left(False)


def buttondown(event, list_of_tank):
    n = 7
    for tank in list_of_tank:
        if len(list_of_tank) == 2 and tank.get_id() == 2:
            n = 1
        if tank.get_id() == event.joy or n == event.joy:
            if event.button == 0:
                tank.set_shoot(True)
            if event.button == 1:
                tank.set_movement(1)
            if event.button == 2:
                tank.set_movement(2)


def buttonup(event, list_of_tank):
    n = 9
    for tank in list_of_tank:
        if len(list_of_tank) == 2 and tank.get_id() == 2:
            n = 1
        if tank.get_id() == event.joy or n == 1:
            if event.button == 1:
                tank.set_movement(0)


def axis(event, list_of_naves):
    for nave in list_of_naves:
        n = 9
        if len(list_of_naves) == 2 and nave.get_id() == 2:
            n = 1
        if nave.get_id() == event.joy or n == event.joy:
            if event.axis == 0:
                horizontal = event.value * 10
                Config.list_axis[nave.get_id()][0] = horizontal
            if event.axis == 1:
                vertical = event.value * 10
                Config.list_axis[nave.get_id()][1] = vertical
            nave.set_spin_axis(True)


def move_axis(list_of_naves):
    for nave in list_of_naves:
        horizontal = Config.list_axis[nave.get_id()][0]
        vertical = Config.list_axis[nave.get_id()][1]
        if abs(horizontal) < 1 and (abs(vertical) < 1 or abs(vertical) > 10.1):
            continue
        nave.spin_by_axis(Config.list_axis[nave.get_id()])
