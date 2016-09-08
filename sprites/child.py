import pygame
import colors

from sprite import Sprite
from characters import *
from block import *

""" Child Sprite """
class Child(Sprite):
    IS_ALIVE = True


    UP    = pygame.K_w
    DOWN  = pygame.K_s
    LEFT  = pygame.K_a
    RIGHT = pygame.K_d

    v_decel = False
    h_decel = False
    s_limit = 1

    def __init__(self, game, classname):
        Sprite.__init__(self, game)
        self.name = classname

        self.can_ani = True
        self.image = pygame.Surface(self.SIZE)
        self.image.fill(colors.GREEN)
        self.set_hitbox_size((32, 32))

        self.load_frames()

        # set default picture
        if self.can_ani:
            try:
                if self.has_idle:
                    self.image = self.idle_frames[str(self.DIR.RIGHT)][0]
                else:
                    self.image = self.frames[str(self.DIR.RIGHT)][0]
            except:
                pass

    def load_frames(self):
        if self.name.lower() == "nathan":
            Nathan(self)
        elif self.name.lower() == "crystal":
            Crystal(self)
        elif self.name.lower() == "jack":
            Jack(self)
        else:
            pass

    def update(self):
        # move player
        self.movement()

        # limit player to borders
        limit_width, limit_height = self.game.MAP_SIZE
        if self.rect.x < 0: self.rect.x = 0
        if self.rect.x + self.WIDTH > limit_width: self.rect.x = limit_width - self.WIDTH
        if self.rect.y < 0: self.rect.y = 0
        if self.rect.y + self.HEIGHT > limit_height: self.rect.y = limit_height - self.HEIGHT

        # animate player
        self.animate()

        # update player movement
        self.update_deceleration()
        if self.block_id == "player":
            self.update_movement()

    """ Handle sprite acceleration """
    def update_movement(self, _keys=None):
        # update movement by keys
        keys = pygame.key.get_pressed()
        if _keys is not None:
            keys = _keys

        # update direction
        if keys[self.RIGHT]: self.direction = self.DIR.RIGHT
        if keys[self.LEFT]: self.direction = self.DIR.LEFT

        # update deceleration
        if keys[self.UP] or keys[self.DOWN]:
            self.v_decel = False
        if keys[self.LEFT] or keys[self.RIGHT]:
            self.h_decel = False

        # update acceleration
        if keys[self.DOWN]:
            if self.vspeed < self.speed:
                if self.vspeed <= self.speed - self.accel:
                    self.vspeed += self.accel

        if keys[self.UP]:
            if self.vspeed > -self.speed:
                if self.vspeed >= -self.speed + self.accel:
                    self.vspeed -= self.accel

        if keys[self.RIGHT]:
            if self.hspeed < self.speed:
                if self.hspeed <= self.speed - self.accel:
                    self.hspeed += self.accel

        if keys[self.LEFT]:
            if self.hspeed > -self.speed:
                if self.hspeed >= -self.speed + self.accel:
                    self.hspeed -= self.accel

    """ Handle sprite deceleration """
    def update_deceleration(self):
        # Deceleration
        if self.v_decel:
            # Gradual Vertical deceleration
            if self.vspeed > 0 and self.vspeed > self.s_limit:
                self.vspeed -= self.accel * 1.5
            if self.vspeed < 0 and self.vspeed < -self.s_limit:
                self.vspeed += self.accel * 1.5
            if self.vspeed <= self.s_limit or self.vspeed >= self.s_limit:
                self.vspeed = 0

        if self.h_decel:
            # Gradual horizontal deceleration
            if self.hspeed > 0 and self.hspeed > self.s_limit:
                self.hspeed -= self.accel * 1.5
            if self.hspeed < 0 and self.hspeed < -self.s_limit:
                self.hspeed += self.accel * 1.5
            if self.hspeed <= self.s_limit or self.hspeed >= self.s_limit:
                self.hspeed = 0

    """ Decrease Player movement """
    def update_stop(self, event):
        if event is not None and event.type == pygame.KEYUP:
            if event.key in [self.UP, self.DOWN]:
                self.v_decel = True

            if event.key in [self.LEFT, self.RIGHT]:
                self.h_decel = True