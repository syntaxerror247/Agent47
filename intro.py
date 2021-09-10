import pygame as pg
import sys
from settings import *
from os import path
from time import sleep as t_sleep
def intro():
    pg.init()
    game_folder = path.dirname(__file__)
    img_folder = path.join(game_folder, 'img')
    font = path.join(img_folder, 'Impacted2.0.ttf')
    def draw_text(text, font_name, size, color, x, y, align="topleft"):
            font = pg.font.Font(font_name, size)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(**{align: (x, y)})
            screen.blit(text_surface, text_rect)

    screen = pg.display.set_mode((WIDTH,HEIGHT))
    pg.display.set_caption(TITLE)
    screen.fill(BLACK)
    draw_text("MISHRA GAMES", font, 100, WHITE,WIDTH // 2, 300, align="center")
    draw_text("PRESENTS..", font, 50, RED,(WIDTH // 2)+200, 400)
    pg.display.flip()
    t_sleep(2)
    screen.fill(BLACK)
    draw_text("Agent 47", font, 100, RED,WIDTH // 2,350,align="center")
    pg.display.flip()
    t_sleep(2)
