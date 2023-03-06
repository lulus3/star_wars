import pygame


class Config:

    # colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    ice_blue = (199, 207, 221)
    gray_blued = (146, 161, 185)
    yellow = (255, 255, 0)
    red = (255, 0, 0)

    # naves
    speed_nave = 4
    recharge_time = 0   # 0.4
    immunity_time = 3
    time_in_limbo = 5

    # powers
    time_shield = 7
    time_to_power = 5
    heal = 60

    # bullet
    speed_ball = 2.5
    life_ball = 1
    damage_bullet = 40

    # asteroids
    speed_asteroid = 0.5
    number_of_asteroids = 10
    damage_asteroid = 20
    multiplier = 5

    screen_w = 1366
    screen_h = 768
    screen_size = (screen_w, screen_h)
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN | pygame.SCALED)

    image_screen = pygame.image.load("assets/universo0.png")
    image_surface = pygame.Surface((image_screen.get_width(), image_screen.get_height()))
    image_rect = image_screen.get_rect()
    screen_rect = pygame.draw.rect(screen, white, (0, 0, 1366, 768))
    logo_game = pygame.image.load("assets/logo_game.png")
    pointer = pygame.image.load("assets/ponteiro.png")
    pointer_y_up = 340
    pointer_y_down = 390

    pygame.font.init()
    font = pygame.font.Font("assets/PressStart2P.ttf", 25)
    font_hud = pygame.font.Font("assets/PressStart2P.ttf", 25)
    font_menu = pygame.font.Font("assets/PressStart2P.ttf", 50)
    font_victory = pygame.font.Font("assets/PressStart2P.ttf", 50)

    list_of_naves = [
        "assets/xwings.png", "assets/milennium_falcon.png", "assets/tie_fighter.png", "assets/tie_interceptor.png"
    ]
    list_of_naves_damage = ["assets/xwings_damage.png", "assets/milennium_falcon_damage.png",
                            "assets/tie_fighter_damage.png", "assets/tie_interceptor_damage.png"]
    list_name_archive_ball = ["assets/bala2.png", "assets/bala2.png", "assets/bala1.png", "assets/bala1.png"]

    bord_xwing = pygame.image.load("assets/life_bar_xwing.png")
    bord_millenium = pygame.image.load("assets/life_bar_millenuim.png")
    bord_fighter = pygame.image.load("assets/life_bar_fighter.png")
    bord_interception = pygame.image.load("assets/life_bar_intercepition.png")
    bord_xwing_rect = pygame.Rect(36, 23, 10, 10)
    bord_millenium_rect = pygame.Rect(313, 23, 10, 10)
    bord_fighter_rect = pygame.Rect(848, 23, 10, 10)
    bord_interception_rect = pygame.Rect(1124, 23, 10, 10)

    list_init_spawn = [(90, 270), (90, 510), (1276, 270), (1276, 510)]
    list_of_dimensions = ["up", "down", "left", "right"]
    list_n = [0, 0, 0, 0]
    list_m = [1, 1, 1, 1]

    victory_point = 10
    loop_intro = False
    loop_menu = True
    loop = True
    loop_victory = False
    clock = pygame.time.Clock()

