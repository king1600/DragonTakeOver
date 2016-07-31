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

    MAX_HP   = 100
    MAX_AP   = 100
    HP       = MAX_HP
    AP       = MAX_AP
    attack   = 15
    defense  = 5

    ani_frame = 0
    ani_count = 0
    ani_delay = 5
    can_ani = True
    has_idle = True
    idle = True
    idle_frames = {
        str(DIR.LEFT): [],
        str(DIR.RIGHT): []
    }
    frames = {
        str(DIR.LEFT): [],
        str(DIR.RIGHT): []
    }

    def __init__(self, game):
        super(Sprite, self).__init__()
        self.game = game
        self.image = hitbox_img

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

    def set_hitbox_size(self, size):
        self.rect = pygame.Rect((self.rect.x, self.rect.y), size)