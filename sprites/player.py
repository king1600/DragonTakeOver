from child import Child

class Player(Child):

    def __init__(self, game, name):
        super(Player, self).__init__(game, name)
        self.block_id = "player"

        self.face = self.game.rsc.resize_image(
            self.game.rsc.faces[self.name], (32, 32))

        self.HP          = 25
        self.scales      = self.game.MAX_SCALES
        self.boss_scales = 0
        self.party_attack= 10
        self.party_health= 10

        self.set_hitbox_size((32, 32))
        self.bar_width = self.game.WIDTH / 4 * 1


    def update(self):
        Child.update(self)
        self.regen()