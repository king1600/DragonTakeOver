import os
import pygame
import colors
import threading

rsc  = os.path.join("resources")
img  = os.path.join(rsc, "images")
maps = os.path.join(img, "maps")
spr  = os.path.join(img, "sprites")
snd  = os.path.join(rsc, "sounds")
sfx  = os.path.join(snd, "sfx")


class ResourceManager:
    smooth_transform = True
    sound_cache      = "music.cache"

    def __init__(self, game):
        self.game = game

    def load_song(self, sname):
        songs = [f for f in os.listdir(snd) if os.path.isfile(os.path.join(snd, f))]
        for s in songs:
            if sname in s.lower():
                s_path = os.path.join(snd, s)
                sound = pygame.mixer.Sound(s_path)
                return sound

    def set_dialog(self, scenes):
        # create a list of dialog
        self.dialog = {}
        dialogs = []
        for x in scenes:
            info = scenes[x]
            for y in info:
                dialogs.append(y)
        dialogs = list(set(dialogs)) #filter out extras
        # set values
        for x in dialogs:
            self.dialog[x] = None

    def load_resources(self):
        self.game.debug("Scale algorithm> " + pygame.transform.get_smoothscale_backend())

        loads = [self.load_music, self.load_backgrounds, self.load_sprite_images, self.load_other]
        threads = []
        for l in loads:
            threads.append(self.create_thread(l))
        self.join_and_delete(threads)


    """ Basic Load functions """

    def load_backgrounds(self):
        #self.game.debug("Loading maps...")
        self.bgs = {}
        map_images = [f for f in os.listdir(maps)]

        for m in map_images:
            m_path = os.path.join(maps, m)
            m = self.game.manager.get_level_name(m)

            size = self.game.manager.levels[m]['size']
            surface = self.load_image(m_path, size)
            self.bgs[m] = surface

    def load_sprite_images(self):
        self.game.debug("Loading sprites...")
        self.sps = {}
        folders = [f for f in os.listdir(spr)]

        for f in folders:
            f_path = os.path.join(spr, f)
            pics = [os.path.join(f_path, s) for s in os.listdir(f_path)]

            normal = []
            for p in pics:
                size = (64, 64)

                for y in ['crystal','nathan','jack']:
                    if y in str(f):
                        size = (96, 96)
                for y in ['ice_blob']:
                    if y in str(f):
                        size = (64, 64)

                img = self.load_image(p, size, colors.WHITE)
                normal.append(img)

            flipped = [pygame.transform.flip(x, True, False) for x in normal]
            self.sps[f] = [normal, flipped]

    def load_music(self):
        try:
            self.game.debug("Loading music...")
            self.music = {}
            songs = [f for f in os.listdir(snd) if os.path.isfile(os.path.join(snd, f))]
            threads = []
            for s in songs:
                threads.append(self.create_thread(self.threaded_load_sound, s))
            self.join_and_delete(threads)

        except Exception as e:
            self.game.debug(str(e))

    def threaded_load_sound(self, s):
        s_path = os.path.join(snd, s)
        sound = pygame.mixer.Sound(s_path)

        s = self.game.manager.get_level_name(s)
        self.music[s] = sound

    def load_other(self):
        try:
            self.game.debug("Loading other resources..")
            self.black = pygame.Surface((64, 64))
            self.black.fill(colors.BLACK)

            # scene background
            bg_path = os.path.join(img, "bg.jpg")
            self.scene_bg = self.load_image(bg_path, (self.game.SIZE))

            # big dialogue box
            big_box_path = os.path.join(img, "box.png")
            size = (self.game.WIDTH/10*8, self.game.HEIGHT/10*8 + 16)
            self.big_box  = self.load_image(big_box_path, size)

            # scale image
            scale_path = os.path.join(img, "scale.png")
            self.scale = self.load_image(scale_path, (24, 24), colors.WHITE)

            # boss scale image
            boss_scale_path = os.path.join(img, "boss_scale.png")
            self.boss_scale = self.load_image(boss_scale_path, (24, 24), colors.WHITE)

            # close button
            close_path = os.path.join(img, "close_button.png")
            self.close_btn = self.load_image(close_path, (24, 24), colors.BLACK)

            # buy button
            buy_path = os.path.join(img, "buy.png")
            self.buy_btn = self.load_image(buy_path, (64, 32))

            # cache scale number font renders
            self.scale_nums = {}
            font = pygame.font.Font(None, 32)
            for x in range(self.game.MAX_SCALES + 1):
                text = font.render(str(x), 1, colors.SC_COLOR)
                self.scale_nums[str(x)] = text

            # shop text
            self.shop_text = {}
            for x in self.game.shop.choices:
                self.shop_text[x] = font.render(str(x), 1, (10,10,10))

            self.load_names()
            self.load_scenes()
            self.load_dialogue()

        except Exception as e:
            self.game.debug("RSC.Other Error: " + str(e))

    def load_dialogue(self):
        try:
            self.game.debug("Loading Dialogue & Faces...")

            d_path = os.path.join(img, "dialogue_box.png")
            size = (self.game.WIDTH/10*8, self.game.HEIGHT/5)
            self.dbox = self.load_image(d_path, size, colors.BLACK)

            # load face images
            self.faces = {}
            face_path = os.path.join(img, "faces")
            size = (self.game.WIDTH/10*2, self.game.HEIGHT/5)
            for x in os.listdir(face_path):
                x_name = self.game.manager.get_level_name(x)
                image = self.load_image(os.path.join(face_path, x), size, colors.WHITE)
                self.faces[x_name] = image

            # generate renderd text for dialog
            font = pygame.font.Font(None, 32)
            for x in self.dialog:
                self.dialog[x] = font.render(x, 1, (10,10,10))

        except Exception as e:
            self.game.debug("RSC.Dialogue Error: " + str(e))

    def load_names(self):
        self.names = {
            "Crystal":None,
            "Nathan":None,
            "Jack":None,
            "Narrator":None
        }

        font = pygame.font.Font(None, 24)
        for n in self.names:
            self.names[n] = font.render(n, 1, colors.PURPLE)

    def load_scenes(self):
        s = os.path.join(img, "scenes")
        files = [f for f in os.listdir(s) if os.path.isfile(os.path.join(s, f))]
        self.scene_img = {}
        self.scene_size = 8
        size = (self.game.WIDTH/10*self.scene_size, self.game.HEIGHT/10*self.scene_size)

        for f in files:
            f_path = os.path.join(s, f)
            f_name = self.game.manager.get_level_name(f)
            self.scene_img[f_name] = self.load_image(f_path, size)


    """ Multi-use functions """

    def load_image(self, path, size=None, trans=None):
        img = pygame.image.load(path).convert()

        if trans is not None:
            img.set_colorkey(trans)
            img = img.convert_alpha()

        if size is not None:
            size = (size[0], size[1]) # make sure tuple
            if self.smooth_transform:
                img = pygame.transform.smoothscale(img, size)
            else:
                img = pygame.transform.scale(img, size)
        return img

    def resize_image(self, image, size=None):
        if size is not None:
            if self.smooth_transform:
                img = pygame.transform.smoothscale(image, size)
            else:
                img = pygame.transform.scale(image, size)
            return img

    def make_surface(self, size, color=colors.BLUE):
        surface = pygame.Surface(size)
        surface.fill(color)
        return surface

    def join_and_delete(self, threads):
        for t in threads:
            t.join()
            try: threads.remove(t)
            except: pass
            del t
        del threads

    def create_thread(self, func, *args):
        t = threading.Thread(target=func, args=args)
        t.daemon = True
        t.start()
        return t