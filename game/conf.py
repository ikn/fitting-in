from platform import system
import os
from os.path import sep, expanduser, join as join_path
from collections import defaultdict
from glob import glob

import pygame as pg

import settings
from util import dd


class Conf (object):

    IDENT = 'fitting-in'
    USE_SAVEDATA = False
    USE_FONTS = False

    # save data
    SAVE = ()
    # need to take care to get unicode path
    if system() == 'Windows':
        try:
            import ctypes
            n = ctypes.windll.kernel32.GetEnvironmentVariableW(u'APPDATA',
                                                               None, 0)
            if n == 0:
                raise ValueError()
        except Exception:
            # fallback (doesn't get unicode string)
            CONF_DIR = os.environ[u'APPDATA']
        else:
            buf = ctypes.create_unicode_buffer(u'\0' * n)
            ctypes.windll.kernel32.GetEnvironmentVariableW(u'APPDATA', buf, n)
            CONF_DIR = buf.value
        CONF_DIR = join_path(CONF_DIR, IDENT)
    else:
        CONF_DIR = join_path(os.path.expanduser(u'~'), '.config', IDENT)
    CONF = join_path(CONF_DIR, 'conf')

    # data paths
    DATA_DIR = ''
    IMG_DIR = DATA_DIR + 'img' + sep
    SOUND_DIR = DATA_DIR + 'sound' + sep
    MUSIC_DIR = DATA_DIR + 'music' + sep
    FONT_DIR = DATA_DIR + 'font' + sep

    # display
    WINDOW_ICON = IMG_DIR + 'icon.png'
    WINDOW_TITLE = 'Fitting In'
    MOUSE_VISIBLE = dd(True) # per-backend
    FLAGS = 0
    FULLSCREEN = False
    RESIZABLE = True # also determines whether fullscreen togglable
    RES_W = (960, 540)
    RES_F = pg.display.list_modes()[0]
    RES = RES_W
    MIN_RES_W = (320, 180)
    ASPECT_RATIO = None

    # timing
    FPS = dd(60) # per-backend

    # debug
    DEBUG = False
    PROFILE_STATS_FILE = '.profile_stats'
    DEFAULT_PROFILE_TIME = 5

    # input
    KEYS_NEXT = (pg.K_RETURN, pg.K_SPACE, pg.K_KP_ENTER)
    KEYS_BACK = (pg.K_ESCAPE, pg.K_BACKSPACE)
    KEYS_MINIMISE = (pg.K_F10,)
    KEYS_FULLSCREEN = (pg.K_F11, (pg.K_RETURN, pg.KMOD_ALT, True),
                    (pg.K_KP_ENTER, pg.KMOD_ALT, True))
    KEYS_LEFT = (pg.K_LEFT, pg.K_a, pg.K_q)
    KEYS_RIGHT = (pg.K_RIGHT, pg.K_d, pg.K_e, pg.K_s)
    KEYS_UP = (pg.K_UP, pg.K_w, pg.K_z, pg.K_COMMA)
    KEYS_JUMP = KEYS_UP + (pg.K_SPACE,)
    KEYS_RESET = (pg.K_r, pg.K_p)

    # audio
    MUSIC_AUTOPLAY = False # just pauses music
    MUSIC_VOLUME = dd(.5) # per-backend
    SOUND_VOLUME = .5
    EVENT_ENDMUSIC = pg.USEREVENT
    SOUND_VOLUMES = dd(1)
    # generate SOUNDS = {ID: num_sounds}
    SOUNDS = {}
    ss = glob(join_path(SOUND_DIR, '*.ogg'))
    base = len(join_path(SOUND_DIR, ''))
    for fn in ss:
        fn = fn[base:-4]
        for i in xrange(len(fn)):
            if fn[i:].isdigit():
                # found a valid file
                ident = fn[:i]
                if ident:
                    n = SOUNDS.get(ident, 0)
                    SOUNDS[ident] = n + 1

    # text rendering
    # per-backend, each a {key: value} dict to update fonthandler.Fonts with
    REQUIRED_FONTS = dd({})

    # gameplay
    GRAVITY = .15
    DAMP_AIR = (.9, .9)
    DAMP_GROUND = .7
    PLAYER_SIZE = (2, 3)
    GROWTH = 2
    SPEED_AIR = .07
    SPEED_GROUND = .18
    SPEED_GROWTH = 1.6
    JUMP_GROWTH = 1.2
    JUMP = lambda t: .6 - .12 * t ** .5
    JUMP_TIME = 18
    OBJ_SIZE = (2, 2)
    COLLISION_ACCURACY = .1

    # levels
    LEVELS = [{
        'size': (100, 50),
        'rects': [(70, 20, 10, 25), (90, 35, 10, 2)],
        'gobjs': [(30, 46), (90, 40)],
        'player': (15, 47)
    }, {
        'size': (150, 80),
        'rects': [(0, 0, 20, 25), (10, 35, 30, 20), (10, 55, 55, 10),
                  (105, 40, 55, 40)],
        'gobjs': [(5, 30), (130, 30), (140, 30)],
        'player': (120, 37)
    }, {
        'size': (150, 80),
        'rects': [(0, 50, 10, 30), (20, 33, 10, 21), (20, 58, 110, 7),
                  (33, 26, 35, 4), (65, 20, 15, 5), (80, 15, 15, 10),
                  (105, 15, 25, 10), (128, 25, 2, 33), (25, 69, 3, 11),
                  (130, 55, 6, 2), (144, 60, 6, 2), (144, 35, 6, 2)],
        'gobjs': [(31, 50), (40, 54), (20, 75), (30, 75)],
        'player': (110, 55)
    }, {
        'size': (50, 30),
        'rects': [(19, 15, 7, 15), (20, 0, 5, 13), (30, 10, 15, 2)],
        'gobjs': [(15, 25), (40, 27)],
        'sobjs': [(40, 7), (14, 20)],
        'player': (35, 7)
    }]


def translate_dd (d):
    if isinstance(d, defaultdict):
        return defaultdict(d.default_factory, d)
    else:
        # should be (default, dict)
        return dd(*d)
conf = dict((k, v) for k, v in Conf.__dict__.iteritems()
            if k.isupper() and not k.startswith('__'))
types = {
    defaultdict: translate_dd
}
if Conf.USE_SAVEDATA:
    conf = settings.SettingsManager(conf, Conf.CONF, Conf.SAVE, types)
else:
    conf = settings.DummySettingsManager(conf, types)
