import pygame
import colors

from collections import OrderedDict

class CutScenes:
    def __init__(self, game):
        self.game = game
        self.current = None
        self.dialogue_fail = False
        self.create_scenes()

    def create_scenes(self):
        self.scenes = OrderedDict()
        self.scenes['scene_1'] = OrderedDict()
        self.scenes['scene_2'] = OrderedDict()
        self.scenes['scene_3'] = OrderedDict()

        scene_1 = self.scenes['scene_1']
        scene_1["There was a land where 3 kinds of species lived"] = "narrator"
        scene_1["They lived with dragons in harmony"] = "narrator"
        scene_1["They consisted of mages, knights and beings"] = "narrator"
        scene_1["Some were in clans but they lived in the village"] = "narrator"
        scene_1["There was a being named Niel."] = "narrator"
        scene_1["Most of his clan died out."] = "narrator"
        scene_1["he was looked down by everyone"] = "narrator"
        scene_1["He didn't get to play with the village kids"] = "narrator"
        scene_1["Then one day..."] = "narrator"
        scene_1["A Wild dragon killed his family!"] = "narrator"
        scene_1["From then on, he swore to eradicate all dragons"] = "narrator"
        scene_1["First he made a poison to turn all dragons wild"] = "narrator"
        scene_1["Then he kidnapped the villages main dragons"] = "narrator"
        scene_1["He demanded one child from each species,"] = "narrator"
        scene_1["To fight him for the dragons"] = "narrator"
        scene_1["Crsytal the Mage.."] = "narrator"
        scene_1["Jack the Warrior.."] = "narrator"
        scene_1["and Nathan the Being.."] = "narrator"
        scene_1["You three have been chosen to defeat Niel"] = "narrator"
        scene_1["You must stop Niel! Your journey begins..."] = "narrator"

        scene_2 = self.scenes['scene_2']
        scene_2["Are you guys ready?"] = "crystal"
        scene_2["Yea but we should visit the shop first"] = "jack"
        scene_2["Good Idea!"] = "nathan"

        no_void = self.scenes['scene_3']
        no_void["Darn! We need all 3 Boss Scales ..."] = "crystal"
        no_void["to go to the void"] = "crystal"

        # none = nothing
        # overlay = overlap existing entities + stop movement
        self.draw_scenes = {
            "scene_1":{
                "happy":[1],
                "playing":[7],
                "none":[x for x in range(20) if x not in [1,7]]
            },
            "scene_2":{"overlay":range(10)},
            "scene_3":{"overlay":range(10)},
        }

        self.scene_music = {
            "scene_1":"keep",
            "scene_2":"keep",
            "scene_3":"keep"
        }

        self.game.rsc.set_dialog(self.scenes)

    def reset_scenes(self):
        no_void = self.scenes['scene_3']
        no_void["Darn! We need all 3 Boss Scales ..."] = self.game.name
        no_void["to go to the void"] = self.game.name

    def load_scene(self, scene_number):
        try:
            scene_name = "scene_"+str(scene_number)
            self.game.debug("loading " + scene_name)
            scene = self.scenes[scene_name]
            count = 0

            # load scene music
            scene_music = self.scene_music[scene_name]
            if scene_music == "keep":
                pass
            else:
                try: self.game.music.stop()
                except: pass

                if scene_music != "none":
                    self.game.music = self.game.rsc.music[scene_music]
                    self.game.music.set_volume(self.game.bg_vol)
                    self.game.music.play(-1)

            for text in scene:
                # get scene meta info
                _text = text
                _char = scene[text]

                # get text to render
                render_text = self.game.rsc.dialog[_text]
                name_text = self.game.rsc.names[_char.title()]
                image       = self.game.rsc.faces[_char]

                # render text in count-slides
                if not self.dialogue_fail:
                    self.draw_dialog(render_text, name_text, image, [scene_name, count])
                    count += 1
                else:
                    self.dialogue_fail = False
                    break

        except Exception as e:
            self.game.debug("Failed to load scene: " + str(e))

    def draw_dialog(self, _text, _name, _image, info):
        # one-time calculations to save CPU cycles
        _dbox = self.game.rsc.dbox
        is_done = False
        h_num = 5
        x_box = self.game.WIDTH / 10 * 2
        y_box = self.game.HEIGHT / h_num * (h_num - 1)
        dbox_size = _dbox.get_rect()
        text_height = y_box + dbox_size.height/2
        s_size  = self.game.rsc.scene_size
        s_avg   = (10 - s_size)/2
        sc_size = (self.game.WIDTH/10*s_avg, self.game.HEIGHT/10*s_avg)

        # draw_loop
        while not is_done:
            try:
                # Get scene picture if any
                has_scene = False
                to_draw   = True
                scene_img = None
                for x in self.draw_scenes[info[0]]:
                    x_info = self.draw_scenes[info[0]][x]
                    if int(info[1]) in x_info:
                        if x == "overlay":
                            pass
                        elif x == "none":
                            to_draw = False
                        else:
                            has_scene = True
                            scene_img = self.game.rsc.scene_img[x]

                # grab events and wait for space
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game.running = False
                        self.game.exit()
                        is_done = True
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            is_done = True

                ### Draw the basic things
                #self.game.screen.fill(colors.BLACK)
                self.game.screen.blit(self.game.rsc.scene_bg,(0,0))
                self.game.clock.tick(self.game.FPS/2)

                # draw
                if not has_scene:
                    if to_draw:
                        self.game.draw_sprites(isScene=True)
                else:
                    if to_draw:
                        self.game.screen.blit(scene_img, sc_size)


                ### Draw the dialog
                self.game.screen.blit(_image, (0, self.game.HEIGHT/h_num*(h_num-1)))
                self.game.screen.blit(_dbox, (x_box, y_box))
                self.game.screen.blit(_text, (x_box+30, text_height-20))
                self.game.screen.blit(_name, (x_box+30, self.game.HEIGHT-25))

                ### Update the screen
                pygame.display.flip()

            except Exception as e:
                self.game.debug("Dialog Fail: " + str(e))
                self.dialogue_fail = True
