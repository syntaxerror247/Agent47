import pygame as pg
from sys import exit as sys_exit
from os import path
from settings import*

class Menu:
    def __init__(self):
        pg.init()
        try:
            pg.mixer.pre_init(44100, -16, 4, 2048)
        except:
            pass
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.options = {}
        self.clicked = False
        self.command = None
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        music_folder = path.join(game_folder, 'music')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        try:
            pg.mixer.music.load(path.join(music_folder, MENU_MUSIC))
        except:
            pass
    
    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    
    def add_option(self,label,width,height,x,y,command):
        surface = pg.Surface((width,height))
        surface.fill((255,255,255))
        rect = pg.Rect(x,y,width,height)
        self.options[label] = {
                                'label':label,
                                'surface':surface,
                                'rect':rect,
                                'command':command
                            }



    def run(self):
        self.running = True
        try:
            pg.mixer.music.play(loops=-1)
        except:
            pass
        while self.running:
            self.events()
            self.update()
            self.draw()
        return self.command
    def events(self):
        self.mx,self.my = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys_exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.clicked=True
            else:
                self.clicked=False
    def update(self):
        for option in self.options:

            if self.options[option]['rect'].collidepoint((self.mx,self.my)):
                self.options[option]['surface'].set_alpha(255)
                if self.clicked:
                    self.running = False
                    self.command = self.options[option]['command']
            else:
                self.options[option]['surface'].set_alpha(0)
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_text("Agent 47", self.title_font, 100, RED,
                        WIDTH / 2, 100, align="center")
        for option in self.options:
            self.screen.blit(self.options[option]['surface'],self.options[option]['rect'])
            self.draw_text(self.options[option]['label'],self.title_font,self.options[option]['rect'].height - 10,(255,0,0),self.options[option]['rect'].x,self.options[option]['rect'].y)
        pg.display.flip()
