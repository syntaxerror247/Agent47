import pygame
from settings import*
import sys
from os import path
class Help:
    def __init__(self):
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.game_folder = path.dirname(__file__)
        img_folder = path.join(self.game_folder, 'img')
        self.font = path.join(img_folder, "DeadFontWalking-X2Ka.ttf")
        self.load_help()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)
    
    def load_help(self):
        self.file = open(path.join(self.game_folder,"help.txt"),"r")
        

    def run(self):
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running=False
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(BLACK)
        i=1
        for line in self.file:
            self.draw_text(line,self.font,30,WHITE,0,80*i)
            pygame.display.flip()
            i+=1
