import os
import pygame
import colors

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

        self.load_music()
        self.load_backgrounds()
        self.load_sprite_images()
        self.load_other()


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

                img = self.load_image(p, size, colors.WHITE)
                normal.append(img)

            flipped = [pygame.transform.flip(x, True, False) for x in normal]
            self.sps[f] = [normal, flipped]

    def load_music(self):
        self.game.debug("Loading music...")
        self.music = {}
        songs = [f for f in os.listdir(snd) if os.path.isfile(os.path.join(snd, f))]
        for s in songs:
            s_path = os.path.join(snd, s)
            sound = pygame.mixer.Sound(s_path)

            s = self.game.manager.get_level_name(s)
            self.music[s] = sound

    def load_other(self):
        self.black = pygame.Surface((64, 64))
        self.black.fill(colors.BLACK)

        bg_path = os.path.join(img, "bg.jpg")
        self.scene_bg = self.load_image(bg_path, (self.game.SIZE))

        bar_path = os.path.join(img, "health_bar.png")
        self.bar = self.load_image(bar_path)

        self.load_names()
        self.load_scenes()
        self.load_dialogue()

    def load_dialogue(self):
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