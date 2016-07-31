import json
import os
import random

import pygame
from pytmx.util_pygame import load_pygame

from sprites import Block

class LevelManager:
    lvl_path = os.path.join("levels")

    def __init__(self, game):
        self.game = game

    def load_all_levels(self):
        self.levels     = {} # name : json_content
        self.tmx_levels = {} # name : tmx_data
        self.collisions = {} # name : [array of Rects]

        self.level  = "village"
        self.last_save_loc = None

        lvl_files = [f for f in os.listdir(self.lvl_path)]
        for l in lvl_files:

            # Determine file type
            if l.endswith(".json"): ftype = 'json'
            elif l.endswith(".tmx"): ftype  = 'tmx'
            else: ftype = None

            # get dict name
            level_name = self.get_level_name(l)
            l = os.path.join(self.lvl_path, l)

            # set json data
            if ftype == 'json':
                with open(l,'r') as f:
                    self.levels[level_name] = json.loads(f.read())

            # set tmx data
            elif ftype == 'tmx':
                tmx_data = load_pygame(l)
                self.tmx_levels[level_name] = tmx_data
            else:
                pass

    def load_level(self, name):
        level_info = self.levels[name]
        self.level = name

        # update game music
        try: self.game.music.stop()
        except: pass
        self.game.music            = self.game.rsc.music[name]
        self.game.music.set_volume(self.game.bg_vol)
        self.game.music.play(-1)

        self.game.MAP_WIDTH, self.game.MAP_HEIGHT = level_info["size"]
        self.game.MAP_SIZE = (self.game.MAP_WIDTH, self.game.MAP_HEIGHT)

        self.game.background.image = self.game.rsc.bgs[name]
        self.game.camera.update_camera(self.game.SIZE, self.game.MAP_SIZE)

        # kill all the sprites
        for e in self.game.entities.sprites():
            if e.block_id not in ["player", "bot", "bg"]:
                e.kill()
        spawn = level_info["spawn"]

        # reset positions
        self.game.player.set_pos(spawn[0], spawn[1])
        for bot in self.game.bots:
            player_rect = self.game.player.rect
            x, y = player_rect.x, player_rect.y
            rand_x = random.choice( range(x-64, x+64) )
            rand_y = random.choice( range(y-64, y+64) )
            bot.set_pos(rand_x, rand_y)

        # calculate map size and object ratio for collidable objects
        tile_map = self.tmx_levels[name]
        tw, th = tile_map.width, tile_map.height
        tpw, tph = tile_map.tilewidth, tile_map.tileheight
        w, h = (tw * tpw), (th * tph)
        lvl_size = level_info["size"]
        ratio_w, ratio_h = lvl_size[0]/(w*1.0), lvl_size[1]/(h*1.0)

        # create invisible collidable objects
        walls = list()
        for obj in tile_map.objects:
            x, y = obj.x, obj.y
            w, h = obj.width, obj.height
            x, y = x * ratio_w, y * ratio_h
            w, h = w * ratio_w, h * ratio_h

            rect = pygame.Rect(x, y, w, h)
            walls.append(rect)

        # set collidable objects
        self.collisions[name] = walls
        self.game.collisions = self.collisions[name]


    def get_level_name(self, l):
        level_name = l.split('.')
        level_name.pop(-1)
        level_name = '.'.join(level_name)
        return level_name