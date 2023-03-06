import sys
import pygame
import random
import powers
from nave import Nave
from estrela_da_morte import Ds1
from planet import Planet
from config import Config
from bullet import Bullet
from hud_menu import Hud
from hud_menu import Menu
from pyvidplayer import Video
from sound_themes import Themes
from asteroides import Asteroid
from nave_colisao import collision_nave_or_bullet
from final_screen import FinalScreen
import keystrokes_joysticks


class Game:
    def __init__(self):
        self.__list_of_nave: list = []
        self.__list_of_limbo: list = []
        self.__list_of_powers: list = []
        self.__list_of_icon_powers: list = []
        self.__list_of_asteroids = []
        self.__counter: int = 0
        self.__bullet_list: list = [[], [], [], []]
        self.__up_wall = pygame.Rect(0, 0, Config.screen_w, 60)
        self.__left_wall = pygame.Rect(-20, 0, 20, Config.screen_h)
        self.__right_wall = pygame.Rect(Config.screen_w, 0, 20, Config.screen_h)
        self.__down_wall = pygame.Rect(0, Config.screen_h, Config.screen_w, 20)
        self.__list_of_walls: list = [self.__up_wall, self.__left_wall, self.__right_wall, self.__down_wall]
        self.__rebel_rect = pygame.Rect(0, 0, Config.screen_w/2, 60)
        self.__empire_rect = pygame.Rect(Config.screen_w/2 + 1, 0, Config.screen_w/2, 60)
        self.__rebel_point: int = 0
        self.__empire_point: int = 0
        self.__time_to_powers = 0
        self.__video_intro = "video"
        self.__menu_texts = Menu()
        self.__number_of_players = 2
        self.__winner_team = 0
        self.__ds1 = Ds1()
        self.__planet = Planet()
        self.__joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.__music = None

    def intro(self):
        if Config.loop_intro:
            self.__video_intro = Video("videos/video intro 1080.mp4")
            self.__video_intro.set_size((1366, 768))
        while Config.loop_intro:
            self.__video_intro.draw(Config.screen, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_5:
                        self.__video_intro.close()
                        Config.loop_intro = False
                    if event.key == pygame.K_ESCAPE:
                        self.__video_intro.close()
                        sys.exit()

    def menu(self):
        menu_texts = Menu()
        while Config.loop_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Config.loop_menu = False
                    Config.loop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_p:
                        Config.loop_menu = False
                    if event.key == pygame.K_UP:
                        menu_texts.pointer_move(2)
                        self.__number_of_players = 2
                    if event.key == pygame.K_DOWN:
                        menu_texts.pointer_move(4)
                        self.__number_of_players = 4
            self.update_screen()
            self.draw_and_move_asteroids()
            menu_texts.draw_text_menu()
            menu_texts.draw_pointer()
            pygame.display.flip()
            Config.clock.tick(60)
        self.__list_of_asteroids.clear()
        self.creat_asteroids()

    def creat_spacecraft(self):
        x = 0
        y = 0
        n = 0
        if self.__number_of_players == 4:
            n = 1
        elif self.__number_of_players == 2:
            n = 2
        for a in range(0, 4, n):
            ship = Nave(Config.list_of_naves[a], Config.list_of_naves_damage[a], Config.speed_nave, x, y, a)
            self.__list_of_nave.append(ship)
            ship.set_x(Config.list_init_spawn[a][0])
            ship.set_y(Config.list_init_spawn[a][1])
        for nave in self.__list_of_nave:
            self.identification_craft(nave)
        self.__music = Themes()

    def actions(self):
        for event in pygame.event.get():
            # print(event)
            self.__music.playing_music(event)
            if event.type == pygame.QUIT:
                Config.loop = False
            if event.type == pygame.KEYDOWN:
                keystrokes_joysticks.keys_down(event, self.__list_of_nave)
            if event.type == pygame.KEYUP:
                keystrokes_joysticks.keys_up(event, self.__list_of_nave)
            if event.type == pygame.JOYBUTTONUP:
                keystrokes_joysticks.buttonup(event, self.__list_of_nave)
            if event.type == pygame.JOYBUTTONDOWN:
                keystrokes_joysticks.buttondown(event, self.__list_of_nave)
            if event.type == pygame.JOYHATMOTION:
                keystrokes_joysticks.hatdown(event, self.__list_of_nave)
            if event.type == pygame.JOYAXISMOTION:
                keystrokes_joysticks.axis(event, self.__list_of_nave)
        keystrokes_joysticks.move_axis(self.__list_of_nave)

    def update_screen(self):
        Config.screen.blit(Config.image_screen, Config.screen_rect)
        self.__planet.draw_planet()
        self.__ds1.draw_img()
        self.__counter = pygame.time.get_ticks()

    def spacecraft_move(self):
        for nave in self.__list_of_nave:
            self.identification_craft(nave)
            self.__limbo()
            nave.move()
            self.__limit_move(nave)
            nave.accelerator()
            nave.decelerator()
            nave.spin_right()
            nave.spin_left()
            nave.still_immunity(self.__counter)
            self.__get_powers(nave.ship_rect, nave)

    def __limit_move(self, nave):
        nave.ship_rect = nave.get_photo().get_rect()
        nave.ship_rect.center = (nave.get_x(), nave.get_y())
        nave.ship_rect.inflate_ip(-nave.get_width()+45, -nave.get_height()+45)
        if nave.ship_rect.colliderect(self.__up_wall):
            nave.set_vector_y(0)
            nave.set_y(nave.get_y() + abs(nave.get_vector_max()[1]))
        if nave.ship_rect.colliderect(self.__left_wall):
            nave.set_vector_x(0)
            nave.set_x(nave.get_x() + abs(nave.get_vector_max()[0]))
        if nave.ship_rect.colliderect(self.__right_wall):
            nave.set_vector_x(0)
            nave.set_x(nave.get_x() - abs(nave.get_vector_max()[0]))
        if nave.ship_rect.colliderect(self.__down_wall):
            nave.set_vector_y(0)
            nave.set_y(nave.get_y() - abs(nave.get_vector_max()[1]))

    def shoot(self):
        for nave in self.__list_of_nave:
            if nave.get_shoot():
                if self.__counter - nave.get_time_to_recharge() > Config.recharge_time * 1000 or nave.get_bullet_power():
                    archive = pygame.image.load(Config.list_name_archive_ball[nave.get_id()])
                    bullet = Bullet(
                        archive, nave.get_x(), nave.get_y(), Config.speed_ball * nave.get_vector_max()[0],
                        Config.speed_ball * nave.get_vector_max()[1], Config.life_ball, nave.get_id(), nave.get_angle())
                    bullet.photo = pygame.transform.rotate(bullet.photo, -bullet.angle)
                    self.__bullet_list[nave.get_id()].append(bullet)
                    nave.set_time_to_recharge()
                    if nave.get_id() == 0:
                        Config.wings_shoot.play()
                    elif nave.get_id() == 1:
                        Config.falcon_shoot.play()
                    elif nave.get_id() > 1.5:
                        Config.ties_shoot.play()
                nave.set_shoot(False)

    def collision_bullet_naves(self):
        for b in self.__bullet_list:
            for bullet in b:
                for nave in self.__list_of_nave:
                    if bullet.get_id() != nave.get_id() and (bullet.get_id() > 1.5 > nave.get_id() or bullet.get_id() < 1.5 < nave.get_id()):
                        if bullet.rect.colliderect(nave.ship_rect):
                            self.__bullet_list[nave.get_id()].clear()
                            b.remove(bullet)
                            nave.set_time_of_animation()
                            nave.take_damage()
                            if nave.get_life() <= 0:
                                nave.set_time_to_spawn()
                                self.__list_of_limbo.append(nave)
                                self.__list_of_nave.remove(nave)
                                if bullet.get_id() > 1.5 > nave.get_id():
                                    self.__empire_point += 1
                                elif bullet.get_id() < 1.5 < nave.get_id():
                                    self.__rebel_point += 1
                            break

    def draw_naves(self):
        for nave in self.__list_of_nave:
            if nave.get_immunity():
                Config.list_n[nave.get_id()] += Config.list_m[nave.get_id()]
                if Config.list_n[nave.get_id()] >= 10:
                    nave.ship_rect = nave.get_photo().get_rect()
                    nave.ship_rect.center = (nave.get_x(), nave.get_y())
                    Config.screen.blit(nave.get_photo(), nave.ship_rect)
                if Config.list_n[nave.get_id()] < 10:
                    nave.ship_rect = nave.get_photo_damage().get_rect()
                    nave.ship_rect.center = (nave.get_x(), nave.get_y())
                    Config.screen.blit(nave.get_photo_damage(), nave.ship_rect)
                if Config.list_n[nave.get_id()] <= 0 or Config.list_n[nave.get_id()] >= 20:
                    Config.list_m[nave.get_id()] *= -1
            else:
                nave.ship_rect = nave.get_photo().get_rect()
                nave.ship_rect.center = (nave.get_x(), nave.get_y())
                Config.screen.blit(nave.get_photo(), nave.ship_rect)

            if nave.get_immunity_power() or nave.get_bullet_power():
                self.__draw_powers(nave.get_x(), nave.get_y(), nave.get_id(), nave)
                self.__limit_power()

    def draw_bullets(self):
        for b in self.__bullet_list:
            for bullet in b:
                bullet.rect.center = (bullet.x_position, bullet.y_position)
                bullet.move()
                Config.screen.blit(bullet.photo, bullet.rect)
                # limit bullet
                if bullet.x_position < -30 or bullet.x_position > Config.screen_w + 30:
                    bullet.life = 0
                if bullet.y_position < -30 or bullet.y_position > Config.screen_h + 30:
                    bullet.life = 0
                if bullet.life <= 0:
                    b.remove(bullet)

    def __draw_life(self):
        if self.__number_of_players >= 2:
            xwing_life_rect = pygame.draw.rect(Config.screen, Config.green, (38, 25, self.__wings.get_life(), 25))
            fighter_life_rect = pygame.draw.rect(Config.screen, Config.green, (850, 25, self.__fighter.get_life(), 25))
        if self.__number_of_players == 4:
            interception_life_rect = pygame.draw.rect(Config.screen, Config.green, (1126, 25, self.__interception.get_life(), 25))
            millenuim_life_rect = pygame.draw.rect(Config.screen, Config.green, (315, 25, self.__millenium.get_life(), 25))

    def update_hud_power(self):
        Config.screen.blit(Config.bord_xwing, Config.bord_xwing_rect)
        Config.screen.blit(Config.bord_millenium, Config.bord_interception_rect)
        Config.screen.blit(Config.bord_fighter, Config.bord_fighter_rect)
        Config.screen.blit(Config.bord_interception, Config.bord_interception_rect)
        logo_rebel = pygame.image.load("assets/bandeira_alianca_rebelde.jpg")
        logo_empire = pygame.image.load("assets/bandeira_imperio.jpg")
        Config.screen.blit(logo_rebel, self.__rebel_rect)
        Config.screen.blit(logo_empire, self.__empire_rect)
        pygame.draw.rect(Config.screen, Config.white, (Config.screen_w / 2, 0, 2, 60))

        if self.__number_of_players >= 2:
            Config.screen.blit(Config.bord_xwing, Config.bord_xwing_rect)
            Config.screen.blit(Config.bord_fighter, Config.bord_fighter_rect)

        if self.__number_of_players == 4:
            Config.screen.blit(Config.bord_interception, Config.bord_interception_rect)
            Config.screen.blit(Config.bord_millenium, Config.bord_millenium_rect)

        self.__draw_life()
        self.__draw_hud()
        self.__creat_icons_powers()
        self.__delete_power()
        self.__draw_icon()

    def __limbo(self):
        for nave in self.__list_of_limbo:
            if self.__counter - nave.get_time_to_spawn() > Config.time_in_limbo * 1000:
                nave.new_life()
                self.__list_of_nave.append(nave)
                self.__list_of_limbo.remove(nave)
                nave.new_location()
            else:
                nave.set_time_of_immunity()

    def identification_craft(self, nave):
        if nave.get_id() == 0:
            self.__wings = nave
        if nave.get_id() == 1:
            self.__millenium = nave
        if nave.get_id() == 2:
            self.__fighter = nave
        if nave.get_id() == 3:
            self.__interception = nave

    def __draw_hud(self):
        Hud.hud_text1 = Config.font_hud.render(str(self.__rebel_point), True, Config.white)
        Config.screen.blit(Hud.hud_text1, Hud.hud_text1_rect)
        Hud.hud_text2 = Config.font_hud.render(str(self.__empire_point), True, Config.black)
        Config.screen.blit(Hud.hud_text2, Hud.hud_text2_rect)
        # condiction_victory
        if self.__rebel_point >= Config.victory_point:
            Config.loop = False
            self.__winner_team = 1
            Config.loop_victory = True
        elif self.__empire_point >= Config.victory_point:
            Config.loop = False
            self.__winner_team = 2
            Config.loop_victory = True

    def __draw_powers(self, x, y, ide, nave):
        for power in self.__list_of_powers:
            print("verificando pintar")
            if power.get_id() == ide:
                print("o poder foi pintado")
                power.move_draw_power(x, y, self.__counter)
                if power.get_type_power() == 1:
                    nave.set_immunity_power(power.get_existence_power())
                elif power.get_type_power() == 2:
                    nave.set_bullet_power(power.get_existence_power())

    def __limit_power(self):
        n1, n2, n3, n4 = 0, 0, 0, 0
        for power in self.__list_of_powers:
            if power.get_id() == 0:
                if n1 != 0:
                    n1.set_delete()
                else:
                    n1 = power
            elif power.get_id() == 1:
                if n2 != 0:
                    n2.set_delete()
                else:
                    n2 = power
            elif power.get_id() == 2:
                if n3 != 0:
                    n3.set_delete()
                else:
                    n3 = power
            elif power.get_id() == 3:
                if n4 != 0:
                    n4.set_delete()
                else:
                    n4 = power

    def __get_powers(self, nave_rect, nave):
        for power in self.__list_of_icon_powers:
            power.nave_catch_icon(nave_rect, nave)
            if power.get_id() == 10 or power.get_id() == nave.get_id() or power.get_id() == 8:
                if not power.get_existence_icon():
                    self.__list_of_powers.append(power)
                    print("o poder foi adicionado")
                    self.__list_of_icon_powers.remove(power)
            elif power.get_id() == 9:
                pass

    def __creat_icons_powers(self):
        if self.__counter - self.__time_to_powers > Config.time_to_power * 1000:
            n = random.randint(1, 3)
            if n == 1:
                x = random.randint(200, Config.screen_w - 200)
                y = random.randint(160, Config.screen_h - 100)
                power = powers.Immunity(x, y)
                self.__time_to_powers = pygame.time.get_ticks()
                self.__list_of_icon_powers.append(power)
            elif n == 2:
                x = random.randint(200, Config.screen_w - 200)
                y = random.randint(160, Config.screen_h - 100)
                power = powers.Healing(x, y)
                self.__time_to_powers = pygame.time.get_ticks()
                self.__list_of_icon_powers.append(power)
            elif n == 3:
                x = random.randint(200, Config.screen_w - 200)
                y = random.randint(160, Config.screen_h - 100)
                power = powers.NoRecharge(x, y)
                self.__time_to_powers = pygame.time.get_ticks()
                self.__list_of_icon_powers.append(power)

    def __delete_power(self):
        for power in self.__list_of_powers:
            if power.get_delete():
                self.__list_of_powers.remove(power)
                break
        for power in self.__list_of_icon_powers:
            if power.get_delete():
                self.__list_of_icon_powers.remove(power)
                break

    def __draw_icon(self):
        for power in self.__list_of_icon_powers:
            if power.get_id() == 10:
                power.draw_icon_shield()
            elif power.get_id() == 9:
                power.draw_icon_heal()
            elif power.get_id() == 8:
                power.draw_icon()

    def creat_asteroids(self):
        for a in range(Config.number_of_asteroids):
            x = random.randint(200, Config.screen_w - 200)
            y = random.randint(160, Config.screen_h - 100)
            asteroid = Asteroid(x, y, 0)
            asteroid.select_img()
            dimension = random.choice(Config.list_of_dimensions)
            asteroid.select_angle()
            asteroid.turn_other_angle(dimension)
            self.__list_of_asteroids.append(asteroid)

    def draw_and_move_asteroids(self):
        for asteroid in self.__list_of_asteroids:
            asteroid.move()
            asteroid.draw_asteroid()
            self.__limit_asteroids(asteroid)

    def __limit_asteroids(self, asteroid):
        if asteroid.get_x() > 1400 or asteroid.get_x() < -40 or asteroid.get_y() > 808 or asteroid.get_y() < -40 or asteroid.get_delete():
            self.__list_of_asteroids.remove(asteroid)
            self.__creat_new_asteroids()

    def __creat_new_asteroids(self):
        p = random.choice(Config.list_of_dimensions)
        x, y = 0, 0
        if p == "up":
            x = random.randint(200, Config.screen_w - 200)
            y = 20
        elif p == "down":
            x = random.randint(200, Config.screen_w - 200)
            y = 808
        elif p == "left":
            x = -40
            y = random.randint(160, Config.screen_h - 100)
        elif p == "right":
            x = 1406
            y = random.randint(160, Config.screen_h - 100)

        asteroid = Asteroid(x, y, 0)
        asteroid.select_img()
        asteroid.select_angle()
        asteroid.turn_other_angle(p)
        self.__list_of_asteroids.append(asteroid)

    def collision_asteroid_nave_bullet(self):
        for asteroid in self.__list_of_asteroids:
            asteroid_rect = asteroid.get_rect_ast()
            asteroid_rect.inflate_ip(-asteroid.get_w() + 75, -asteroid.get_h() + 58)
            asteroid_rect.center = (asteroid.get_x(), asteroid.get_y())
            for nave in self.__list_of_nave:
                nave.ship_rect = nave.get_photo().get_rect()
                nave.ship_rect.center = (nave.get_x(), nave.get_y())
                nave.ship_rect.inflate_ip(-nave.get_width() + 45, -nave.get_height() + 45)
                if asteroid_rect.colliderect(nave.ship_rect):
                    var = collision_nave_or_bullet(
                        nave.get_x(), nave.get_y(), asteroid.get_vector()[0], asteroid.get_vector()[1],
                        nave.get_vector()[0], nave.get_vector()[1],
                        asteroid.get_x() - 40, asteroid.get_y() - 31, 80, 62, 0
                    )
                    nave.set_x(var[0][0])
                    nave.set_y(var[0][1])
                    nave.set_vector_x(var[1][0])
                    nave.set_vector_y(var[1][1])
                    asteroid.set_delete(True)
                    Config.asteroid_destroyed.play()
                    nave.take_damage_asteroid()
                    if nave.get_life() <= 0:
                        nave.set_time_to_spawn()
                        self.__list_of_limbo.append(nave)
                        self.__list_of_nave.remove(nave)
                        break
            for b in self.__bullet_list:
                for bullet in b:
                    if bullet.rect.colliderect(asteroid_rect):
                        b.remove(bullet)

    def screen_victory(self):
        time_of_screen = pygame.time.get_ticks()
        n = -10
        s = 0
        pygame.mixer.music.stop()
        text = " "
        cor = Config.white
        if self.__winner_team == 1:
            text = "Vitoria da aliança rebelde"
            cor = Config.red
        if self.__winner_team == 2:
            text = "Vitoria do imperio"
            cor = Config.green
        text_victory = Config.font_victory.render(text, True, cor)
        text_rect = text_victory.get_rect()

        while Config.loop_victory:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Config.loop_victory = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
            self.update_screen()
            self.draw_naves()
            self.draw_bullets()
            self.draw_and_move_asteroids()
            self.update_hud_power()
            n += 1
            if n >= s * 20 and s < 9:
                s += 1
            Config.screen.blit(FinalScreen.list_screens[s], (0, 0))
            text_rect.center = (Config.screen_w/2, Config.screen_h/2)
            Config.screen.blit(text_victory, text_rect)
            pygame.display.flip()
            Config.clock.tick(60)
            if self.__counter - time_of_screen > 15000:
                Config.loop_victory = False

    def last_video(self):
        video_final = "video"
        time = pygame.time.get_ticks()
        if Config.loop_last_video and self.__winner_team == 1:
            video_final = Video("videos/Death star explosion.mp4")
            video_final.set_size((1366, 768))
        elif Config.loop_last_video and self.__winner_team == 2:
            video_final = Video("videos/Death Star 3D Model Animation.mp4")
            video_final.set_size((1366, 768))
        while Config.loop_last_video:
            self.__counter = pygame.time.get_ticks()
            video_final.draw(Config.screen, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or self.__counter - time >= 11000:
                        video_final.close()
                        Config.loop_last_video = False
                    if event.key == pygame.K_ESCAPE:
                        video_final.close()
                        sys.exit()


