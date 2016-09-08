import pygame
import random

from child import Child

class Mob(Child):
    def __init__(self, game, name):
        Child.__init__(self, game, name)
        self.game = game
        self.name = name
        self.player = self.game.player

        self.keys = {
            self.UP: False, self.DOWN: False,
            self.LEFT: False, self.RIGHT: False
        }

        self.follow = True
        self.aggro_dist = 30

    def update(self):
        Child.update(self)

        if self.follow:
            # if player in aggro_dist, move to player
            rand_aggro = self.aggro_dist#random.randint(5, self.aggro_dist)

            try:
                p_x, p_y = self.player.rect.x, self.player.rect.y
                rect_x, rect_y = self.rect.x, self.rect.y
                rad_x = range(rect_x - rand_aggro, rect_x + rand_aggro)
                rad_y = range(rect_y - rand_aggro, rect_y + rand_aggro)

                if p_x in rad_x:
                    if rect_x < p_x: self.move_dir(self.RIGHT)
                    if rect_x > p_x: self.move_dir(self.LEFT)
                    self.h_decel = False
                    self.update_movement(self.keys)
                else:
                    self.h_decl = True

                if p_y in rad_y:
                    if rect_y < p_y: self.move_dir(self.DOWN)
                    if rect_y > p_y: self.move_dir(self.UP)
                    self.v_decel = False
                    self.update_movement(self.keys)
                else:
                    self.v_decel = True

            except:
                pass

    def move_dir(self, _dir):
        for x in self.keys:
            if x == _dir:
                self.keys[x] = True
            else:
                self.keys[x] = False

    def reset_keys(self):
        for x in self.keys:
            self.keys[x] = False

    def random_chance(self, chance=50):
        nums = range(0, 101)
        random.shuffle(nums)
        choices = []
        random_choice = random.choice(nums)

        for x in range(chance):
            c = nums.pop(nums.index(random.choice(nums)))
            choices.append(c)

        if random_choice in choices:
            return (True, random_choice)  # It succeded being in chance!
        else:
            return (False, random_choice)  # failed