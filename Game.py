import pygame
import sys
import os
import logging
import json
import threading

import resources
import colors
import pyscroll

from level_manager import LevelManager
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

    def __init__(self):
        pygame.display.init()
        pygame.mixer.init()
        pygame.font.init()

        self.music  = None
        self.bg_vol = 0.4
        self.name   = None

        self.entities   = None
        self.map_layer  = None
        self.collisions = []

        self.create_logger()
        self.manager = LevelManager(self)
        self.rsc = resources.ResourceManager(self)
        self.scences = CutScenes(self)

    def init(self, classname="Crystal"):
        # Create window
        os.environ['SDL_VIDEO_CENTERED'] = '1' # center screen
        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Dragon TakeOver")

        # Load levels
        self.manager.load_all_levels()

        # Add icon
        ico_path = os.path.join("resources","images","icon.png")
        ico_surf = self.rsc.load_image(ico_path,(32,32),colors.WHITE)
        pygame.display.set_icon(ico_surf)

        # create camera, fps, and game var
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera = Camera(self.SIZE, self.MAP_SIZE)

        # load game
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
        print "waiting for loading thread to stop..."
        load_thread.join()
        print "loading thread killed"

        self.name = str(classname).lower()
        self.create_sprites()
        self.load_save()

    ### Load Game Save file
    def load_save(self):
        if os.path.exists(self.SAVE_FILE):
            self.debug("loading save data")
            with open(self.SAVE_FILE, 'r') as f:
                save_data = json.loads(f.read())

            self.name = save_data['player']
            self.manager.last_save_loc = save_data['last_save']

        self.create_player()

        if os.path.exists(self.SAVE_FILE):
            self.manager.load_level(save_data['level'])
            to_load = [save_data['lvl'],save_data['coords'],save_data['xp_to_next']]
            self.load_player_info(to_load)

    ### Create/Overwrite Game save file
    def write_save(self):
        self.debug("writing save")
        save = {}
        save['level']      = self.manager.level
        save['player']     = self.name
        save['coords']     = [self.player.rect.x, self.player.rect.y]
        save['lvl']        = self.player.level
        save['xp_to_next'] = self.player.xp_to_next
        save['last_save']  = self.manager.last_save_loc

        with open(self.SAVE_FILE, 'w') as f:
            f.write(json.dumps(save, indent=4, sort_keys=True))

    ### Create Debug/Game log
    def create_logger(self):
        # delete existing log file
        if os.path.exists(self.LOG_FILE): os.remove(self.LOG_FILE)

        # create logger
        logging.basicConfig(filename=self.LOG_FILE, level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    ### Create game sprites
    def create_sprites(self):
        self.debug("creating sprites")
        self.background = Block(self.MAP_SIZE)
        self.background.block_id = "bg"

        self.entities = pygame.sprite.Group()
        self.entities.add( self.background )

    def create_player(self):
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

    ### Load player info from save file
    def load_player_info(self,saveinfo):
        self.player.level = saveinfo[0]
        self.player.rect.x, self.player.rect.y = saveinfo[1]
        self.player.xp_to_next = saveinfo[2]

    """ EVENT LOOP FUNCTIONS """

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.player.update_stop(event)

        self.clock.tick(self.FPS)
        self.screen.fill(colors.BLACK)

        self.draw_sprites()
        self.entities.update()
        pygame.display.flip()

    def draw_sprites(self):
        self.camera.update(self.player)
        for e in self.entities.sprites():
            if e.block_id not in ["player","bot"]:
                self.screen.blit(e.image, self.camera.apply(e))

        # prioritize drawing of player and bots
        for bot in self.bots:
            self.screen.blit(bot.image, self.camera.apply(bot))
        self.screen.blit(self.player.image, self.camera.apply(self.player))

        for sprite in self.entities.sprites():
            if sprite.block_id in ["player","bot"]:
                if sprite.rect.collidelist(self.collisions) > -1:
                    sprite.move_back()

    def draw_health_bars(self, sprite):
        _mid = (sprite.MAX_HP*60/100)
        _low = (sprite.MAX_HP*30/100)

        # get bar size
        size = sprite.SIZE
        if sprite.block_id == "player": bar_width = 480
        elif sprite.block_id == "boss": bar_width = self.WIDTH/10*8
        else: bar_width = size[0]

        # get length of health
        percent_left = (self.player.HP * bar_width) / (self.player.MAX_HP * 1.0)
        percent_lost = ((self.player.MAX_HP - self.player.HP) * bar_width) / (self.player.MAX_HP * 1.0)

        # calculate color
        if sprite.HP > _mid:
            color = colors.H_GREEN
        elif sprite.HP > _low:
            color = colors.H_YELLOW
        else:
            color = colors.H_RED

        # draw player health
        if sprite.block_id == "player":
            pass

        # draw boss health
        elif sprite.block_id == "boss":
            pass

        # draw mob health
        else:
            # draw remaining health
            pygame.draw.rect(self.screen, color, (5, 5, percent_left, 20))
            # draw lost health
            pygame.draw.rect(self.screen, colors.BLACK,
                             (5 + percent_left, 5, percent_lost, 20))


    def draw_player_info(self):
        # draw player info here

        for e in self.entities.sprites():
            if e.IS_ALIVE:
                self.draw_health_bars(e)


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

    def debug(self, text, debug=False):
        _log = text
        if not isinstance(text, basestring): _log = repr(text)
        print _log

        if debug: self.logger.debug(_log)