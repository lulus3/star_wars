from config import Config


class Hud:
    hud_text1 = Config.font.render("0", True, Config.white, Config.black)
    hud_text2 = Config.font.render("0", True, Config.black)
    hud_text1_rect = hud_text1.get_rect()
    hud_text2_rect = hud_text2.get_rect()
    hud_text1_rect.center = (645, 30)
    hud_text2_rect.center = (710, 30)
    hd1 = [hud_text1, hud_text1_rect]
    hd2 = [hud_text2, hud_text2_rect]
    list_hud = [hd1, hd2]




class Menu:
    def __init__(self):
        self.title_text1 = Config.font_menu.render("combat tank asteroid:", True, Config.yellow)
        self.title_text2 = Config.font_menu.render("star wars", True, Config.yellow)
        self.menu_text1 = Config.font.render("2 players", True, Config.white)
        self.menu_text2 = Config.font.render("4 players", True, Config.white)
        self.title_text_rect1 = self.title_text1.get_rect()
        self.title_text_rect2 = self.title_text2.get_rect()
        self.menu_text_rect1 = self.menu_text1.get_rect()
        self.menu_text_rect2 = self.menu_text2.get_rect()
        self.title_text_rect1.center = (683, 30)
        self.title_text_rect2.center = (683, 80)
        self.menu_text_rect1.center = (683, 340)
        self.menu_text_rect2.center = (683, 390)
        self.cor_pointer = Config.pointer_y_up

    def draw_text_menu(self):
        Config.screen.blit(self.title_text1, self.title_text_rect1)
        Config.screen.blit(self.title_text2, self.title_text_rect2)
        Config.screen.blit(self.menu_text1, self.menu_text_rect1)
        Config.screen.blit(self.menu_text2, self.menu_text_rect2)

    def pointer_move(self, num):
        if num == 2:
            self.cor_pointer = Config.pointer_y_up
        else:
            self.cor_pointer = Config.pointer_y_down

    def draw_pointer(self):
        rect = Config.pointer.get_rect()
        rect.center = (550, self.cor_pointer)
        Config.screen.blit(Config.pointer, rect)
