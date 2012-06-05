from math import log

import pygame as pg
from .ext import evthandler as eh

import conf

ir = lambda x: int(round(x))
err = 10 ** -5

class Level:
    def __init__ (self, game, event_handler, ID):
        self.game = game
        self.event_handler = event_handler
        self.frame = conf.FRAME
        self.load(ID)
        self.l = []
        def print_l (*args):
            x = min(x[0] for x in self.l)
            y = min(x[1] for x in self.l)
            w = max(x[0] for x in self.l) - x
            h = max(x[1] for x in self.l) - y
            x = ir(float(x - self.pos[0]) / self.scale)
            y = ir(float(y - self.pos[1]) / self.scale)
            w = ir(float(w) / self.scale)
            h = ir(float(h) / self.scale)
            print (x, y, w, h)
        # controls
        event_handler.add_key_handlers([
            (conf.KEYS_LEFT, ((self.move, (-1,)),), eh.MODE_HELD),
            (conf.KEYS_RIGHT, ((self.move, (1,)),), eh.MODE_HELD),
            (conf.KEYS_JUMP, self.jump_start, eh.MODE_ONDOWN),
            (conf.KEYS_JUMP, self.jump_continue, eh.MODE_HELD),
            (conf.KEYS_RESET, self.reset, eh.MODE_ONDOWN),
            ((pg.K_s,), lambda *args: setattr(self, 'l', []), eh.MODE_ONDOWN),
            ((pg.K_p,), print_l, eh.MODE_ONDOWN)
        ])
        event_handler.add_event_handlers({pg.MOUSEBUTTONDOWN: lambda e: self.l.append(e.pos)})

    def load (self, ID):
        self.ID = ID
        self.reset()

    def reset (self, *args):
        data = conf.LEVELS[self.ID]
        w, h = self.size = data['size']
        # determine display pos
        sw, sh = conf.RES
        self.scale = s = min(sw / float(w), sh / float(h))
        w *= s
        h *= s
        self.pos = (ir((sw - w) / 2), ir((sh - h) / 2))
        self.rect = pg.Rect(self.pos, (ir(w), ir(h)))
        # get other stuff
        self.rects = list(data['rects'])
        self.objs = [o + conf.OBJ_SIZE for o in data['objs']]
        self.player = list(data['player']) + list(conf.PLAYER_SIZE)
        # init player
        self.v = [0, 0]
        self.jumping = 0
        self.jumps_left = conf.NUM_ALLOWED_JUMPS
        self.player_size = 1
        self.speed = 1

    def to_screen (self, r):
        l, t = self.pos
        s = self.scale
        x = ir(l + s * r[0])
        y = ir(t + s * r[1])
        if len(r) == 2:
            return (x, y)
        else:
            return (x, y, ir(r[2] * s), ir(r[3] * s))

    def move (self, k, t, m, d):
        v = conf.SPEED_GROUND if self.grounded else conf.SPEED_AIR
        self.v[0] += d * self.speed * v

    def jump_start (self, k, t, m):
        if self.grounded or self.jumps_left:
            if self.grounded:
                self.jumps_left = conf.NUM_ALLOWED_JUMPS
            self.v[1] -= conf.JUMP_START * self.speed
            self.jumping = conf.JUMP_TIME
            self.jumps_left -= 1

    def jump_continue (self, k, t, m):
        if self.jumping:
            self.v[1] -= conf.JUMP_CONTINUE * self.speed

    def collect (self, p, s):
        for i, o in enumerate(self.objs):
            if p[0] < o[0] + o[2] and p[0] + s[0] > o[0] and \
               p[1] < o[1] + o[3] and p[1] + s[1] > o[1] :
                return i

    def collision (self, p, s):
        for r in self.rects:
            if p[0] + err < r[0] + r[2] and p[0] + s[0] > r[0] + err and \
               p[1] + err < r[1] + r[3] and p[1] + s[1] > r[1] + err:
                return True
        return p[0] + err < 0 or p[0] + s[0] > self.size[0] + err or \
               p[1] + err < 0 or p[1] + s[1] > self.size[1] + err

    def update (self):
        if self.jumping:
            if self.jumping > conf.JUMP_TIME - conf.AUTO_JUMP:
                self.v[1] -= conf.JUMP_START * self.speed
            self.jumping -= 1
        p = self.player[:2]
        s = self.player[2:]
        v = self.v
        grounded = False
        acc = conf.COLLISION_ACCURACY
        for i in (0, 1):
            d = acc * (1 if v[i] > 0 else -1)
            p[i] += v[i]
            while v[i] != 0 and self.collision(p, s):
                if i and d > 0:
                    grounded = True
                diff = v[i]
                if abs(diff) <= abs(d):
                    p[i] -= diff
                    v[i] = 0
                else:
                    p[i] -= d
                    v[i] -= d
        # collect
        obj = self.collect(p, s)
        if obj is not None:
            self.objs.pop(obj)
            self.player_size *= conf.GROWTH
            self.speed = conf.SPEED_GROWTH ** (log(self.player_size) / log(2))
            # grow player around centre
            for i in (0, 1):
                c = p[i] + float(s[i]) / 2
                s[i] = conf.PLAYER_SIZE[i] * self.player_size
                p[i] = c - float(s[i]) / 2
            # finish level
            if not self.objs:
                ID = self.ID + 1
                if len(conf.LEVELS) <= ID:
                    self.game.quit()
                else:
                    self.load(ID)
                return
            # move out of rects
            w = [0, 0]
            if self.collision(p, s):
                done = False
                w = 0
                while not done:
                    for d1 in (-1, 0, 1):
                        for d2 in (-1, 0, 1):
                            q = (p[0] + w * d1 * acc, p[1] + w * d2 * acc)
                            if not self.collision(q, s):
                                done = True
                                break
                        if done:
                            break
                    w += 1
                p = list(q)
        self.grounded = grounded
        self.player = p + s
        self.v = [v[0] * (conf.DAMP_GROUND if grounded else conf.DAMP_AIR),
                  v[1] * conf.DAMP_AIR + conf.GRAVITY]

    def draw (self, screen):
        screen.fill((0, 0, 0))
        screen.fill((255, 255, 255), self.rect)
        for r in self.rects:
            screen.fill((0, 0, 0), self.to_screen(r))
        for o in self.objs:
            screen.fill((0, 255, 0), self.to_screen(o))
        screen.fill((255, 0, 0), self.to_screen(self.player))
        return True