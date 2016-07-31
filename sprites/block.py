import pygame
import colors

hitbox_img = pygame.Surface((64, 64))
hitbox_img.fill(colors.BLUE)

""" Direction Facing """
class DirectionEnum:
    LEFT   = 0x00
    RIGHT  = 0x01


""" Basic Sprite Block (interactive object) """
class Block(pygame.sprite.Sprite):
    WIDTH     = 64
    HEIGHT    = 64
    SIZE      = (WIDTH, HEIGHT)

    COORDS = (0, 0)
    COLOR  = colors.BLUE

    block_id  = None
    IS_ALIVE = False

    def __init__(self, size=None, coords=(0,0)):
        super(Block, self).__init__()

        if size is not None:
            self.WIDTH, self.HEIGHT = size
            self.SIZE = (self.WIDTH, self.HEIGHT)
        self.COORDS = coords
        self.image = hitbox_img

        self.rect = pygame.Rect(self.COORDS, self.SIZE)

    def set_pos(self, x, y):
        self.rect.x = x
        self.rect.y = y
