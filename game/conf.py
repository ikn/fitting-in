from os import sep

import pygame as pg

# paths
DATA_DIR = ''
IMG_DIR = DATA_DIR + 'img' + sep
SOUND_DIR = DATA_DIR + 'sound' + sep
MUSIC_DIR = DATA_DIR + 'music' + sep
FONT_DIR = DATA_DIR + 'font' + sep

# display
WINDOW_ICON = None #IMG_DIR + 'icon.png'
WINDOW_TITLE = ''
MOUSE_VISIBLE = True
FLAGS = 0
FULLSCREEN = False
RESIZABLE = False # also determines whether fullscreen togglable
RES_W = (960, 540)
RES_F = pg.display.list_modes()[0]
MIN_RES_W = (320, 180)
ASPECT_RATIO = None

# timing
FPS = 60
FRAME = 1. / FPS

# input
KEYS_NEXT = (pg.K_RETURN, pg.K_SPACE, pg.K_KP_ENTER)
KEYS_BACK = (pg.K_ESCAPE, pg.K_BACKSPACE)
KEYS_MINIMISE = (pg.K_F10,)
KEYS_FULLSCREEN = (pg.K_F11, (pg.K_RETURN, pg.KMOD_ALT, True),
                   (pg.K_KP_ENTER, pg.KMOD_ALT, True))
KEYS_LEFT = (pg.K_LEFT,)
KEYS_UP = (pg.K_UP,)
KEYS_RIGHT = (pg.K_RIGHT,)
KEYS_DOWN = (pg.K_DOWN,)
KEYS_MOVE = (KEYS_LEFT, KEYS_UP, KEYS_RIGHT, KEYS_DOWN)
KEYS_JUMP = (pg.K_SPACE, pg.K_UP)
KEYS_RESET = (pg.K_r,)

# audio
MUSIC_VOLUME = 50
SOUND_VOLUME = 50
EVENT_ENDMUSIC = pg.USEREVENT
SOUNDS = {}
SOUND_VOLUMES = {}

# gameplay
GRAVITY = .3
DAMP_AIR = .9
DAMP_GROUND = .7
PLAYER_SIZE = (2, 3)
GROWTH = 2
SPEED_AIR = .1
SPEED_GROUND = .3
SPEED_GROWTH = 1.2
JUMP_START = .6
JUMP_CONTINUE = .3
AUTO_JUMP = 4 # extra jump_start for this long
JUMP_TIME = 10
NUM_ALLOWED_JUMPS = 1
OBJ_SIZE = (2, 2)
COLLISION_ACCURACY = .1

# levels
LEVELS = [{
    'size': (100, 50),
    'rects': [(70, 20, 10, 25), (90, 35, 10, 2)],
    'objs': [(30, 45), (90, 40)],
    'player': (15, 47)
}, {
    'size': (150, 80),
    'rects': [(0, 50, 10, 30), (20, 33, 10, 21), (20, 58, 110, 7),
              (33, 26, 35, 4), (65, 20, 15, 5), (80, 15, 15, 10),
              (105, 15, 25, 10), (128, 25, 2, 33), (25, 69, 3, 11),
              (130, 55, 6, 2), (144, 60, 6, 2), (144, 35, 6, 2)],
    'objs': [(31, 50), (40, 53), (20, 75), (30, 75)],
    'player': (110, 47)
}, {
    'size': (150, 80),
    'rects': [(0, 0, 20, 25), (10, 35, 30, 20), (10, 55, 55, 10),
              (105, 40, 55, 40)],
    'objs': [(5, 30), (130, 30), (140, 30)],
    'player': (120, 37)
}]