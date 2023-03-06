import pygame
from game import Game
from config import Config
pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
game = Game()
game.intro()
game.creat_asteroids()
game.menu()
game.creat_spacecraft()

while Config.loop:
    game.actions()
    game.update_screen()
    game.spacecraft_move()
    game.shoot()
    game.collision_bullet_naves()
    game.draw_naves()
    game.draw_bullets()
    game.draw_and_move_asteroids()
    game.collision_asteroid_nave_bullet()
    game.update_hud_power()
    pygame.display.flip()
    Config.clock.tick(60)

game.screen_victory()
pygame.quit()
