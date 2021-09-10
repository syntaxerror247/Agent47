import pygame as pg
vec = pg.math.Vector2
rot13trans = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890)(*&^%$#@!',
        'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm)(*&^%$#@!1234567890')
def rot13(text):
    text=str(text)
    return text.translate(rot13trans)
LAST_LEVEL=3

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
BLUE = (0,0,255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Agent47"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG_GUN = 'soldier1_gun.png'
PLAYER_IMG_SHOTGUN = 'soldier1_shotgun.png'
PLAYER_IMG_MACHINEGUN = 'soldier1_machinegun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 45, 45)
BARREL_OFFSET = vec(45, 15)

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullets':100,
                     'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullets':100*12,
                      'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12}
WEAPONS['machinegun'] = {'bullets':100*10,
                      'bullet_speed': 500,
                      'bullet_lifetime': 1000,
                      'rate': 20,
                      'kickback': 100,
                      'spread': 5,
                      'damage': 20,
                      'bullet_size': 'sm',
                      'bullet_count': 1}

# Mob settings
MOBS = {}
MOBS['spider'] = {
                    'image': 'spider.png',
                    'hit_rect': pg.Rect(0, 0, 26, 35),
                    'speed':[150,200,175,125],
                    'health': 100,
                    'damage': 10,
                }
MOBS['monster'] = {
                    'image': 'monster.png',
                    'hit_rect': pg.Rect(0, 0, 60, 60),
                    'speed':[250, 200, 175, 225],
                    'health': 150,
                    'damage': 10,
                }
MOBS['zombie'] = {
                    'image': 'zombie.png',
                    'hit_rect': pg.Rect(0, 0, 50, 70),
                    'speed':[200, 100, 175, 225],
                    'health': 200,
                    'damage': 25,
                }
# MOB_IMG_SPIDER = 'spider.png'
# MOB_SPEEDS = [250, 200, 175, 225]
# SPIDER_HIT_RECT = pg.Rect(0, 0, 30, 30)
# MOB_HEALTH = 100
# MOB_DAMAGE_SPIDER = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
SPLAT = 'splat green.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_soft.png"

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'health_pack.png',
               'pistol': 'obj_pistol.png',
               'shotgun': 'obj_shotgun.png',
               'machinegun': 'obj_shotgun.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 10
BOB_SPEED = 0.3

# Sounds
BG_MUSIC = "Dark Intro.ogg"
MENU_MUSIC = "Dark Intro.ogg"
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
MOB_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'machinegun': ['pistol.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav'}

