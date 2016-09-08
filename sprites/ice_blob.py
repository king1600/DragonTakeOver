import pygame
import random

from mob import Mob
from characters import *

class IceBlob(Mob):
    def __init__(self, game):
        self.name = "ice_blob"
        self.block_id = "ice_blob"
        self.has_idle = False
        Mob.__init__(self, game, self.name)

        Ice_Blob(self)
        self.direction = self.DIR.RIGHT
        self.image = self.frames[str(self.DIR.RIGHT)][0]

        self.aggro_dist = 120
        self.speed = 2
        self.accel = .25
