class Nathan:
    def __init__(self, sprite):
        sprite.frames[str(sprite.DIR.LEFT)] = sprite.game.rsc.sps[sprite.name][1]
        sprite.frames[str(sprite.DIR.RIGHT)] = sprite.game.rsc.sps[sprite.name][0]
        sprite.has_idle = False

class Crystal:
    def __init__(self, sprite):
        sprite.frames[str(sprite.DIR.LEFT)] = sprite.game.rsc.sps[sprite.name][1]
        sprite.frames[str(sprite.DIR.RIGHT)] = sprite.game.rsc.sps[sprite.name][0]

        sprite.idle_frames[str(sprite.DIR.LEFT)] = [sprite.game.rsc.sps[sprite.name][1][0]]
        sprite.idle_frames[str(sprite.DIR.RIGHT)] = [sprite.game.rsc.sps[sprite.name][0][0]]

class Jack:
    def __init__(self, sprite):
        sprite.frames[str(sprite.DIR.LEFT)] = sprite.game.rsc.sps[sprite.name][1]
        sprite.frames[str(sprite.DIR.RIGHT)] = sprite.game.rsc.sps[sprite.name][0]

        sprite.idle_frames[str(sprite.DIR.LEFT)] = [sprite.game.rsc.sps["jack_idle"][1][0]]
        sprite.idle_frames[str(sprite.DIR.RIGHT)] = [sprite.game.rsc.sps["jack_idle"][0][0]]