import pygame
import sys
import os
import logging
import json
import threading
import multiprocessing

import resources
import colors

from level_manager import LevelManager
from shop import Shop
from cut_scenes import CutScenes
from camera import Camera
from sprites import Player
from sprites import Block
from sprites import NathanBot, JackBot, CrystalBot

class Game:
    WIDTH    = 720
    HEIGHT   = WIDTH/12*9
    SIZE     = (WIDTH, HEIGHT)

    MAP_WIDTH  = 1980
    MAP_HEIGHT = 1080
    MAP_SIZE   = (MAP_WIDTH, MAP_HEIGHT)

    FPS        = 60
    LOG_FILE   = "gamelog.log"
    SAVE_FILE  = "save.json"

    HAS_MAP    = False
    HAS_HEALTH = True

    MAX_SCALES = 100

    def __init__(self):
        self.create_logger()

        try:
            self.debug("Initializing pygame")
            pygame.init()
        except Exception as e:
            self.debug("Init Error: "+str(e))

        self.music  = None
        self.bg_vol = 0.4
        self.name   = None

        self.entities   = None
        self.map_layer  = None
        self.collisions = []
        self.transport_rects = {}

        try:
            self.shop = Shop(self)
            self.manager = LevelManager(self)
            self.rsc     = resources.ResourceManager(self)
            self.scenes = CutScenes(self)
        except Exception as e:
            self.debug("Manager Error: "+str(e))

    def init(self, classname="Crystal"):
        # Create window
        os.environ['SDL_VIDEO_CENTERED'] = '1' # center screen
        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Dragon TakeOver")

        # Load levels
        try:
            self.debug("Loading levels...")
            self.manager.load_all_levels()
        except Exception as e:
            self.debug("Level.All Error: " + str(e))

        # Add icon
        ico_path = os.path.join("resources","images","icon.png")
        ico_surf = self.rsc.load_image(ico_path,(32,32),colors.WHITE)
        pygame.display.set_icon(ico_surf)

        # create camera, fps, and game var
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_dead = False
        self.camera = Camera(self.SIZE, self.MAP_SIZE)


        self.name = str(classname).lower()

        # load game
        try:
            self.debug("loading resources")
            font =  pygame.font.Font(None, 48)
            self.load_text = font.render("Loading...",1,colors.WHITE)
            self.load_rect = self.load_text.get_rect()
            self.load_rect.centerx = self.screen.get_rect().centerx
            self.load_rect.centery = self.screen.get_rect().centery
            self.IS_LOADING = True
            load_thread = self.create_thread(self.loading_screen)

            self.rsc.load_resources()
            self.IS_LOADING = False
            self.debug("waiting for loading thread to stop...")
            load_thread.join()
            self.debug("loading thread killed")

        except Exception as e:
            self.debug("Resource error: " + str(e))

        try:
            self.debug("loading shop resources")
            self.shop.init()
        except Exception as e:
            self.debug("Shop.init Error: " + str(e))

        self.create_sprites()
        self.load_save()

    ### Load Game Save file
    def load_save(self):
        save_data = None

        try:
            self.debug("loading save data")
            if os.path.exists(self.SAVE_FILE):
                with open(self.SAVE_FILE, 'r') as f:
                    save_data = json.loads(f.read())

                self.name = save_data['player']
                self.scenes.reset_scenes()

            self.create_player()

            if os.path.exists(self.SAVE_FILE):
                self.manager.load_level(save_data['level'])
                self.load_player_info(save_data)

        except Exception as e:
            self.debug("Save data Error: " + str(e))

    ### Create/Overwrite Game save file
    def write_save(self):
        self.debug("writing save")
        save = {}
        save['level']      = self.manager.level
        save['player']     = self.name
        save['max_hp']     = self.player.MAX_HP
        save['max_ap']     = self.player.MAX_AP
        save['attack']     = self.player.attack
        save['scales']     = self.player.scales
        save['boss_scales']= self.player.boss_scales
        save['party_hp']   = self.player.party_health
        save['party_atk']  = self.player.party_attack


        with open(self.SAVE_FILE, 'w') as f:
            f.write(json.dumps(save, indent=4, sort_keys=True))

    ### Create Debug/Game log
    def create_logger(self):
        # delete existing log file
        if os.path.exists(self.LOG_FILE):
            os.remove(self.LOG_FILE)

        # create logger
        logging.basicConfig(filename=self.LOG_FILE, level=logging.DEBUG)

    ### Create game sprites
    def create_sprites(self):
        self.debug("creating sprites")
        self.background = Block(self.MAP_SIZE)
        self.background.block_id = "bg"

        self.entities = pygame.sprite.Group()
        self.entities.add( self.background )

    def create_player(self):
        self.tests = []
        try:
            self.debug("Creating party..")

            # spawn player
            self.player = Player(self, self.name)
            self.player.block_id = "player"
            self.entities.add( self.player )

            # choose ally bots
            bot_options = ["crystal","nathan","jack"]
            bot_options.remove(self.name.lower())

            # spawn bots
            self.bots = []
            for bot_name in bot_options:
                self.debug("Creating bot: "+bot_name)

                if bot_name == "crystal": bot = CrystalBot(self, bot_name)
                elif bot_name == "jack": bot = JackBot(self, bot_name)
                else: bot = NathanBot(self, bot_name)

                bot.rect.x = self.player.rect.x + 50
                bot.rect.y = self.player.rect.y - 50

                self.bots.append( bot )
                self.entities.add( bot )

        except Exception as e:
            self.debug("Party Creation Error: " + str(e))

    ### Load player info from save file
    def load_player_info(self, info):
        self.player.MAX_HP = info['max_hp']
        self.player.MAX_AP = info['max_ap']
        self.player.attack = info['attack']
        self.player.scales = info['scales']

        self.player.boss_scales  = info['boss_scales']
        self.player.party_attack = info['party_atk']
        self.player.party_health = info['party_hp']

    """ EVENT LOOP FUNCTIONS """

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player.update_stop(event)

        self.clock.tick(self.FPS)
        self.screen.fill(colors.BLACK)

        self.draw_sprites()
        self.draw_player_info()
        self.entities.update()
        pygame.display.flip()

    def draw_sprites(self, isScene=False):
        self.camera.update(self.player)
        for e in self.entities.sprites():
            if e.block_id not in ["player","bot"]:
                self.screen.blit(e.image, self.camera.apply(e.rect))

        # prioritize drawing of player and bots
        for bot in self.bots:
            self.screen.blit(bot.image, self.camera.apply(bot.rect))
        self.screen.blit(self.player.image, self.camera.apply(self.player.rect))

        # do collision
        for sprite in self.entities.sprites():
            if sprite.block_id in ["player","bot"]:
                if sprite.rect.collidelist(self.collisions) > -1:
                    sprite.move_back()

        # check transport
        if not isScene:
            for name in self.transport_rects:
                rect = self.transport_rects[name]
                if self.player.rect.colliderect(rect):
                    print str(name)
                    if name == "void":
                        if self.player.boss_scales < 3:
                            self.player.rect.y -= 30
                            self.player.h_decel, self.player.v_decel = True, True
                            self.scenes.load_scene(3)
                            spawn = self.manager.levels["village"]["spawn"]
                            self.player.set_pos(spawn[0], spawn[1])
                            break
                    else:
                        self.manager.load_level(name)
                        break
        else:
            pass

        for x in self.tests:
            self.screen.blit(x[1], self.camera.apply(x[0]))

    def draw_bars(self, sprite):
        _mid = (sprite.MAX_HP*60/100)
        _low = (sprite.MAX_HP*30/100)

        bar_width = sprite.bar_width

        # get length of health
        percent_left = (sprite.HP * bar_width) / (sprite.MAX_HP * 1.0)
        percent_lost = ((sprite.MAX_HP - sprite.HP) * bar_width) / (sprite.MAX_HP * 1.0)

        # get length of ap
        ap_left = (sprite.AP * bar_width) / (sprite.MAX_AP * 1.0)
        ap_lost = ((sprite.MAX_AP - sprite.AP) * bar_width) / (sprite.MAX_AP * 1.0)

        # calculate color
        if sprite.HP > _mid:
            color = colors.H_GREEN
        elif sprite.HP > _low:
            color = colors.H_YELLOW
        else:
            color = colors.H_RED

        # draw player health
        if sprite.block_id == "player":
            bar_x, bar_y = 40, 10
            bar_height = 15

            # draw HP
            left = (bar_x+3,bar_y+3, percent_left, bar_height)
            lost = (bar_x+percent_left+3, bar_y+3, percent_lost, bar_height)
            pygame.draw.rect(self.screen, color, left)
            pygame.draw.rect(self.screen, (10, 10, 10), lost)

            # draw ap
            left = (bar_x + 3, bar_y + 30, ap_left, bar_height)
            lost = (bar_x + ap_left+3, bar_y + 30, ap_lost, bar_height)
            pygame.draw.rect(self.screen, colors.AP_COLOR, left)
            pygame.draw.rect(self.screen, (10, 10, 10), lost)

        # draw boss health
        elif sprite.block_id == "boss":
            pass

        # draw mob health
        else:
            hp_rect = self.camera.apply(sprite.rect)
            x, y = hp_rect.x, hp_rect.y
            start_x = x + (sprite.WIDTH/2)
            start_y = y - sprite.hp_evel
            bar_height = 5

            left = (start_x, start_y, percent_left, bar_height)
            lost = (start_x+percent_left, start_y, percent_lost, bar_height)

            pygame.draw.rect(self.screen, color, left)
            pygame.draw.rect(self.screen, (10,10,10), lost)

    def draw_player_info(self):
        # draw face
        face = self.player.face
        self.screen.blit(face, (5,5))

        # draw scales
        scale_text = self.rsc.scale_nums[str(self.player.scales)]
        boss_text  = self.rsc.scale_nums[str(self.player.boss_scales)]
        self.screen.blit(self.rsc.scale, (5, 65))
        self.screen.blit(self.rsc.boss_scale, (105, 65))
        self.screen.blit(scale_text, (35, 65))
        self.screen.blit(boss_text, (135, 65))

        # draw all entity health bars
        for e in self.entities.sprites():
            if e.IS_ALIVE:
                self.draw_bars(e)

    #### Other

    def draw_loading(self):
        self.clock.tick(self.FPS)
        self.screen.fill(colors.BLACK)
        self.screen.blit(self.load_text, self.load_rect)
        pygame.display.flip()

    def run(self):

        while self.running:
            self.draw()

        self.exit()

    def exit(self):
        self.write_save()
        pygame.quit()
        sys.exit()

    def loading_screen(self):
        while self.IS_LOADING:
            self.draw_loading()

    def create_thread(self, func, *args):
        t = threading.Thread(target=func, args=args)
        t.daemon = True
        t.start()
        return t

    def debug(self, text, debug=True):
        _log    = text
        starter = "> "
        if not isinstance(text, basestring): _log = repr(text)

        if debug:
            logging.debug(starter + _log)
        else:
            logging.info(starter + _log)
        print _log