import pygame
from block import *

""" Entity/Organism (mob,npc, or player)"""
class Sprite(Block):
    DIR = DirectionEnum()
    direction = DIR.RIGHT

    last_x = 0
    last_y = 0
    vspeed = 0
    hspeed = 0
    speed  = 5
    accel  = .5

    def __init__(self, game):
        self.create_basics()
        super(Sprite, self).__init__()
        self.game = game
        self.image = hitbox_img

        self.bar_width  = self.WIDTH*1.5
        self.hp_evel    = 20

    def create_basics(self):
        self.MAX_HP = 100
        self.MAX_AP = 100
        self.HP = self.MAX_HP
        self.AP = self.MAX_AP
        self.attack = 15

        # Regeneration
        self.HP_REGEN = 1
        self.HP_DELAY = 10
        self.HP_COUNT = 0

        self.AP_REGEN = 3
        self.AP_DELAY = 10
        self.AP_COUNT = 0

        self.ani_frame = 0
        self.ani_count = 0
        self.ani_delay = 5
        self.can_ani = True
        self.has_idle = True
        self.idle = True
        self.idle_frames = {
            str(self.DIR.LEFT): [],
            str(self.DIR.RIGHT): []
        }
        self.frames = {
            str(self.DIR.LEFT): [],
            str(self.DIR.RIGHT): []
        }

    def change_direction(self, direction):
        self.direction = direction

    def movement(self):
        self.idle = True

        self.last_x = self.rect.x
        self.last_y = self.rect.y

        self.rect.x += self.hspeed
        self.rect.y += self.vspeed

        if self.hspeed == 0 and self.vspeed == 0:
            self.idle = False

    def move_back(self):
        self.rect.x = self.last_x
        self.rect.y = self.last_y

    def use_frames(self, frames):
        if frames != []:
            if self.ani_frame < len(frames) - 1:
                self.ani_frame += 1
            else:
                self.ani_frame = 0
            self.image = frames[self.ani_frame]

    def animate(self):
        if self.can_ani:
            frames   = self.frames[str(self.direction)]
            i_frames = self.idle_frames[str(self.direction)]

            if self.ani_count <= self.ani_delay:
                self.ani_count += 1
            else:
                self.ani_count = 0

                if self.idle:
                    self.use_frames(frames)
                else:
                    if self.has_idle:
                        self.use_frames(i_frames)
                    else:
                        self.use_frames(frames)

    def regen(self):
        self.HP_COUNT += 1
        self.AP_COUNT += 1

        if self.HP_COUNT > self.HP_DELAY:
            self.HP_COUNT = 0
            if self.HP < self.MAX_HP:
                self.HP += self.HP_REGEN
        if self.AP_COUNT > self.AP_DELAY:
            self.AP_COUNT = 0
            if self.AP < self.MAX_AP:
                self.AP += self.AP_REGEN

        if self.HP > self.MAX_HP: self.HP = self.MAX_HP
        if self.AP > self.MAX_AP: self.AP = self.MAX_AP

    def set_hitbox_size(self, size):
        self.rect = pygame.Rect((self.rect.x, self.rect.y), size)
        self.SIZE = self.WIDTH, self.HEIGHT = size
        self.bar_width = self.WIDTH