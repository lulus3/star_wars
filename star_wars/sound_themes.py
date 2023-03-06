import pygame


class Themes:
    def __init__(self):
        self.music_theme1 = "sounds/Aerial Combat - Super Star Wars (SNES)(MP3_320K).wav"
        self.music_theme2 = "sounds/DUEL OF THE FATES 16 bit - SNES Chiptune Cover ( werc85 ) OpenMPT(MP3_320K).wav"
        self.music_theme3 = "sounds/Luke Skywalker_s Theme - Super Star Wars (SNES)(MP3_320K).wav"
        self.music_theme4 = "sounds/Star Wars Main Theme - Super Star Wars (SNES)(MP3_320K).wav"
        self.n = 1
        pygame.mixer.music.load(self.music_theme1)
        pygame.mixer.music.play()

    def playing_music(self, event):
        SONG_END = pygame.USEREVENT
        if event.type == SONG_END:
            pygame.mixer.music.load(self.new_music())
            pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(SONG_END)

    def new_music(self):
        self.n += 1
        if self.n > 4:
            self.n = 1
        if self.n == 1:
            return self.music_theme1
        elif self.n == 2:
            return self.music_theme2
        elif self.n == 3:
            return self.music_theme3
        elif self.n == 4:
            return self.music_theme4
