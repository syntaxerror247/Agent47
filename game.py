import pygame as pg
from sys import exit as sys_exit
from random import choice, random
from csv import DictReader,DictWriter
from os import path,mkdir
from settings import *
from sprites import *
from tilemap import *
from time import sleep as t_sleep

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
    
class Game:
    def __init__(self):
        self.audio_device = True
        try:
            pg.mixer.init()
        except:
            pass
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.running = True
        self.level = 1

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def save(self):
        with open(path.join(self.data_folder,"data.mg"),"w") as csvfile:
            fname=["level","weapon1","weapon1_bullets","weapon2","weapon2_bullets","weapon3","weapon3_bullets"]
            writer=DictWriter(csvfile,fname)
            #writer.writeheader()
            writer.writerow({"weapon1":rot13(str(self.player.weapon1)),
                             "weapon1_bullets":rot13(WEAPONS['pistol']['bullets']),
                             "weapon2":rot13(str(self.player.weapon2)),
                             "weapon2_bullets":rot13(WEAPONS['shotgun']['bullets']),
                             "weapon3":rot13(str(self.player.weapon3)),
                             "weapon3_bullets":rot13(WEAPONS['machinegun']['bullets']),
                             "level":rot13(self.level)
                        })

    def load_data(self):
        self.data_folder = path.expanduser("~/Agent47/")
        if not path.isdir(self.data_folder):
            mkdir(self.data_folder)
            with open(path.join(self.data_folder,"data.mg"),"w") as csvfile:
                fname=["level","weapon1","weapon1_bullets","weapon2","weapon2_bullets","weapon3","weapon3_bullets"]
                writer=DictWriter(csvfile,fname)
                writer.writerow({"level":rot13(0)})
            self.data_folder = path.expanduser("~/Agent47/")

        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.text_font = path.join(img_folder, "DeadFontWalking-X2Ka.ttf")

        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.player_img_gun = pg.image.load(path.join(img_folder, PLAYER_IMG_GUN)).convert_alpha()
        self.player_img_shotgun = pg.image.load(path.join(img_folder, PLAYER_IMG_SHOTGUN)).convert_alpha()
        self.player_img_machinegun = pg.image.load(path.join(img_folder, PLAYER_IMG_MACHINEGUN)).convert_alpha()
        self.player_img = self.player_img_gun
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.bullet_images['md'] = pg.transform.scale(self.bullet_images['lg'], (12, 12))
        self.spider_img = pg.image.load(path.join(img_folder, MOBS['spider']['image'])).convert_alpha()
        self.monster_img = pg.image.load(path.join(img_folder, MOBS['monster']['image'])).convert_alpha()
        self.zombie_img = pg.image.load(path.join(img_folder, MOBS['zombie']['image'])).convert_alpha()
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        # lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # Sound loading
        try:
            pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
            self.effects_sounds = {}
            for type in EFFECTS_SOUNDS:
                self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
            self.weapon_sounds = {}
            for weapon in WEAPON_SOUNDS:
                self.weapon_sounds[weapon] = []
                for snd in WEAPON_SOUNDS[weapon]:
                    s = pg.mixer.Sound(path.join(snd_folder, snd))
                    s.set_volume(0.3)
                    self.weapon_sounds[weapon].append(s)
            
            self.player_hit_sounds = []
            for snd in PLAYER_HIT_SOUNDS:
                self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
            self.mob_hit_sounds = []
            for snd in MOB_HIT_SOUNDS:
                self.mob_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        except:
            pass
    def new(self):
        #load starting file
        
        # initialize all variables and do all the setup for a new game
        self.walls = pg.sprite.Group()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, f"level{self.level}.tmx"))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'spider':
                Mob(self, obj_center.x, obj_center.y,"spider")
            if tile_object.name == 'monster':
                Mob(self, obj_center.x, obj_center.y,"monster")
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y,"zombie")
            if tile_object.name in ['health', 'shotgun','pistol','machinegun']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False
        self.night = False
        try:
            self.effects_sounds['level_start'].play()
        except:
            pass

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        try:
            pg.mixer.music.play(loops=-1)
        except:
            pass
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # game over?
        if len(self.mobs) == 0:
            self.level+=1
            self.save()
            if not self.is_completed():
                self.draw_loading()
                self.new()
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                try:
                    self.effects_sounds['health_up'].play()
                except:
                    pass
                self.player.add_health(HEALTH_PACK_AMOUNT)

            if hit.type == 'pistol':
                hit.kill()
                try:
                    self.effects_sounds['gun_pickup'].play()
                except:
                    pass
                if self.player.weapon1 == 'pistol':
                    WEAPONS['pistol']['bullets'] += 100
                else:
                    self.player.weapon1 = 'pistol'

            if hit.type == 'shotgun':
                hit.kill()
                try:
                    self.effects_sounds['gun_pickup'].play()
                except:
                    pass
                if self.player.weapon2 == 'shotgun':
                    WEAPONS['shotgun']['bullets'] += 200
                else:
                    self.player.weapon2 = 'shotgun'
            
            if hit.type == 'machinegun':
                hit.kill()
                try:
                    self.effects_sounds['gun_pickup'].play()
                except:
                    pass
                if self.player.weapon3 == 'machinegun':
                    WEAPONS['machinegun']['bullets'] += 200
                else:
                    self.player.weapon3 = 'machinegun'

        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for mob in hits:
            if random() < 0.7:
                try:
                    choice(self.player_hit_sounds).play()
                except:
                    pass
            
            self.player.health -= MOBS[mob.type]['damage']
            mob.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel -= vec(mob.vel.x//3,mob.vel.y//3)
        
        # choose player image
        self.choose_image()

    def choose_image(self):
        if self.player.weapon == "pistol":
            self.player_img = self.player_img_gun
        elif self.player.weapon == "shotgun":
            self.player_img = self.player_img_shotgun
        elif self.player.weapon == "machinegun":
            self.player_img = self.player_img_machinegun

    def draw_loading(self):
        self.screen.blit(self.dim_screen, (0, 0))
        self.draw_text("Loading..", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.update()
        t_sleep(3)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        if self.night:
            self.render_fog()
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text('ALIVE: {}'.format(len(self.mobs)), self.hud_font, 30, BLACK,
                       WIDTH - 10, 10, align="topright")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        # draw bullets
        self.draw_text(f"{self.player.weapon} :{WEAPONS[self.player.weapon]['bullets']}", self.hud_font, 30, BLACK,
                       10, 100, align="topleft")
        pg.display.flip()

    def quit(self):
        self.playing = False
        self.running = False

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys_exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused
                #if event.key == pg.K_n:
                   # self.night = not self.night

    def resume(self):
        with open(path.join(self.data_folder,"data.mg"),"r") as csvfile:
            fname=["level","weapon1","weapon1_bullets","weapon2","weapon2_bullets","weapon3","weapon3_bullets"]
            reader=DictReader(csvfile,fname)
            for row in reader:
                level = int(rot13(row["level"]))
            if level > self.level:
                self.level = level

    def is_completed(self):
        self.screen.blit(self.dim_screen,(0,0))
        pg.event.clear()
        if self.level > LAST_LEVEL:
            self.level = 0
            self.save()
            self.draw_text("You are just GREAT",self.hud_font,30,RED,WIDTH//2,100,align="center")
            self.draw_text("You have killed all the mindless dirty creatures alone...",self.hud_font,30,RED,WIDTH//2,200,align="center")
            self.draw_text("We have great respect for you.",self.hud_font,30,RED,WIDTH//2,300,align="center")
            self.draw_text("press any key to continue.",self.hud_font,30,RED,WIDTH//2,500,align="center")
            pg.display.flip()
            self.wait_for_key()
            self.quit()
            return True

    def show_start_screen(self):
        pg.event.clear()
        self.screen.fill(BLACK)
        game_folder = path.dirname(__file__)
        f = open(path.join(game_folder,"story.txt"),"r")
        i=1
        for line in f:
            self.draw_text(line,self.text_font,33,BLUE,WIDTH//2,55*i,align="center")
            pg.display.flip()
            i+=1
        self.wait_for_key()
        f.close()

    def show_go_screen(self):
        if self.running:
            self.screen.fill(BLACK)
            self.draw_text("GAME OVER", self.title_font, 100, RED,
                        WIDTH / 2, HEIGHT / 2, align="center")
            self.draw_text("Press a key to start", self.title_font, 75, WHITE,
                        WIDTH / 2, HEIGHT * 3 / 4, align="center")
            pg.display.flip()
            self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()
                    sys_exit()
                if event.type == pg.KEYUP:
                    waiting = False
