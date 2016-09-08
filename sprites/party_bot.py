import pygame
import random

from child import Child

class States:
    FOLLOW = 0x0
    ATTACK = 0x1
    DEFEND = 0x2
    COLLECT= 0x3

""" Basic Bot mechanics """

class AI_Bot(Child):
    def __init__(self, game, name):
        Child.__init__(self, game, name)
        self.game = game
        self.name = name

        self.states = States
        self.state = self.states.FOLLOW

        if len(self.game.bots) == 0:
            self.radius_x = 40
            self.radius_y = 40
        else:
            self.radius_x = 80
            self.radius_y = 80

        self.keys = {
            self.UP:False, self.DOWN:False,
            self.LEFT:False, self.RIGHT:False
        }

        self.player = self.game.player
        self.MAX_HP += self.player.party_health
        self.attack += self.player.party_attack

        self.block_id = "bot"
        self.set_hitbox_size((32, 32))

        #self.image = pygame.Surface(self.SIZE)
        #self.image.fill(colors.GREEN)
        #self.can_ani = True

    def update(self):
        Child.update(self)
        self.regen()

        ### Follow Player ###
        if self.state == self.states.FOLLOW:
            # get player location
            p_x, p_y = self.player.rect.centerx, self.player.rect.centery

            # check if bot in range
            rad_x = range(p_x - self.radius_x, p_x + self.radius_x)
            rad_y = range(p_y - self.radius_y, p_y + self.radius_y)
            rect_x, rect_y = self.rect.centerx, self.rect.centery

            # if not next to player, move bot to player
            self.reset_keys()
            if rect_x not in rad_x:
                if rect_x < rad_x[0]: self.move_dir(self.RIGHT)
                if rect_x > rad_x[0]: self.move_dir(self.LEFT)
                self.h_decel = False
                self.update_movement(self.keys)
            else:
                self.h_decel = True
            if rect_y not in rad_y:
                if rect_y < rad_y[0]: self.move_dir(self.DOWN)
                if rect_y > rad_y[0]: self.move_dir(self.UP)
                self.v_decel = False
                self.update_movement(self.keys)
            else:
                self.v_decel = True

        ### Attack Enemies ###
        elif self.state == self.states.ATTACK:
            pass

        ### Defend Player ###
        elif self.state == self.states.DEFEND:
            pass

        ### Collect Scales ###
        elif self.state == self.states.COLLECT:
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

    def spawn_random(self, x=False, y=False):
        if x: rand_x = random.choice(range(0, self.game.MAP_WIDTH))
        else: rand_x = 0

        if y: rand_y = random.choice(range(0, self.game.MAP_HEIGHT))
        else: rand_y = 0

        self.set_pos(rand_x, rand_y)


""" Different types of Bots """

class NathanBot(AI_Bot):
    def __init__(self, game, name):
        AI_Bot.__init__(self, game, name)

class CrystalBot(AI_Bot):
    def __init__(self, game, name):
        AI_Bot.__init__(self, game, name)

class JackBot(AI_Bot):
    def __init__(self, game, name):
        AI_Bot.__init__(self, game, name)