from child import Child
from block import *

class Player(Child):
    DIR = DirectionEnum()
    direction = DIR.RIGHT
    ani_frame = 0
    ani_count = 0
    ani_delay = 5
    can_ani = True
    has_idle = True
    idle = True
    idle_frames = {
        str(DIR.LEFT): [],
        str(DIR.RIGHT): []
    }
    frames = {
        str(DIR.LEFT): [],
        str(DIR.RIGHT): []
    }

    def __init__(self, game, name):
        super(Player, self).__init__(game, name)
        self.block_id = "player"