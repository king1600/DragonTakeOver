import pygame
import colors

from collections import OrderedDict

class Shop:
    IS_OPEN = False

    PARTY_ATK_5   = 10
    PARTY_ATK_10  = 20
    ATK_5         = 10
    ATK_10        = 25
    HP_15         = 10
    HP_30         = 20
    AP_15         = 10
    AP_30         = 20

    choices = {
        'Party Attack +5':10,
        'Party Attack +10':20,
        'Attack +5':10,
        'Attack +10': 25,
        'Max HP +15':10,
        'Max HP +30': 20,
        'Max AP +15':10,
        'Max AP +30':20
    }

    def __init__(self, game):
        self.game = game
        self.actions = {
            'Party Attack +5': self.party_atk_5,
            'Party Attack +10': self.party_atk_10,
            'Attack +5': self.attack_5,
            'Attack +10': self.attack_10,
            'Max HP +15': self.max_hp_15,
            'Max HP +30': self.max_hp_30,
            'Max AP +15': self.max_ap_15,
            'Max AP +30': self.max_ap_30
        }

    def party_atk_5(self):
        value = self.choices["Party Attack +5"]
        if self.game.player.scales >= value:
            self.game.player.scales -= value
    def party_atk_10(self):
        value = self.choices["Party Attack +10"]
        if self.game.player.scales >= value:
            self.game.player.scales -= value
    def attack_5(self):
        value = self.choices["Attack +5"]
        if self.game.player.scales >= value:
            self.game.player.scales -= value
    def attack_10(self):
        value = self.choices["Attack +5"]
        if self.game.player.scales >= value:
            self.game.player.scales -= value
    def max_hp_15(self):
        value = self.choices["Max HP +15"]
        if self.game.player.scales >= value:
            self.game.player.scales -= value
    def max_hp_30(self):
        value = self.choices["Max HP +30"]
        if self.game.player.scales >= value:
            self.game.player.scales -= value
    def max_ap_15(self):
        value = self.choices["Max AP +15"]
        if self.game.player.scales >= value:
            self.game.player.scales -= value
    def max_ap_30(self):
        value = self.choices["Max AP +30"]
        if self.game.player.scales >= value:
            self.game.player.scales -= value

    def init(self):
        self.box_size = (self.game.WIDTH / 10, self.game.HEIGHT / 10)
        self.box_rect = self.game.rsc.big_box.get_rect()
        self.close_rect = self.game.rsc.close_btn.get_rect()
        self.close_size = [self.box_rect.width + self.box_size[0] - self.close_rect.width - 15]
        self.close_size.append(self.box_size[1] + 15)
        self.close_size = (self.close_size[0], self.close_size[1])  # convert to tuple
        self.close_rect.x, self.close_rect.y = self.close_size  # assign correct coords
        self.scale_size = (self.box_size[0]+10, self.box_size[1]+10)
        self.scale_text_size = (self.box_size[0]+50, self.box_size[1]+10)
        self.scale_pos = (self.box_rect.width + self.box_size[0] - 200, self.box_size[1] + 30)

        self.buy_rects = {}
        buy_rect = self.game.rsc.buy_btn.get_rect()
        buy_rect_size = (buy_rect.width, buy_rect.height)

        # create text and images
        self.shop_info = OrderedDict()
        _x, y = self.box_size[0]+30, self.box_size[1]+40
        count = 0
        for x in self.choices:
            # name = [ text_pos, scale_pos, cost_pos, buy_pos ]
            text_pos = (_x, y + count)
            scale_pos = (self.scale_pos[0], y + count)
            cost_pos  = (scale_pos[0] + 40, y + count)
            buy_pos   = (scale_pos[0] + 80, y + count)
            info = [text_pos, scale_pos, cost_pos, buy_pos]
            self.shop_info[x] = info
            count += 50

            # set buy rects
            buy_rect = pygame.Rect(buy_pos, buy_rect_size)
            self.buy_rects[x] = buy_rect


    def draw_shop(self):
        self.IS_OPEN = True

        while self.IS_OPEN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                    self.game.exit()
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    _x, _y = event.pos
                    if self.close_rect.collidepoint(_x, _y):
                        self.IS_OPEN = False
                        break

                    for x in self.buy_rects:
                        rect = self.buy_rects[x]
                        if rect.collidepoint(_x, _y):
                            function = self.actions[x]
                            function()

            scale_text = self.game.rsc.scale_nums[str(self.game.player.scales)]

            self.game.clock.tick(self.game.FPS/2)
            self.game.screen.fill( colors.BLACK )
            self.game.screen.blit(self.game.rsc.scene_bg, (0, 0))
            self.game.screen.blit(self.game.rsc.big_box, self.box_size)
            self.game.screen.blit(self.game.rsc.close_btn, self.close_size)

            self.game.screen.blit(self.game.rsc.scale, self.scale_size)
            self.game.screen.blit(scale_text, self.scale_text_size)

            for x in self.shop_info:
                info = self.shop_info[x]
                text = self.game.rsc.shop_text[x]
                cost = self.game.rsc.scale_nums[str(self.choices[x])]
                scale = self.game.rsc.scale
                buy = self.game.rsc.buy_btn

                self.game.screen.blit(text, info[0])
                self.game.screen.blit(cost, info[1])
                self.game.screen.blit(scale, info[2])
                self.game.screen.blit(buy, info[3])

            pygame.display.flip()