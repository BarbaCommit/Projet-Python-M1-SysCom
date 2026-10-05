import pygame
from constants import TILE_SIZE


class Tile:

    def __init__(self, col: int, row: int,friction_factor:float = 1.0, color : tuple[int,int,int] = (80,80,90)):
        self.col = col
        self.row = row
        self.sprite: pygame.Surface | None = None
        self.friction_factor:float = friction_factor
        self.color = color

    def get_sprite(self, tile_size: int = TILE_SIZE) -> pygame.Surface:
        if self.sprite and self.sprite.get_width() == tile_size:
            return self.sprite
        surface = pygame.Surface((tile_size, tile_size))
        surface.fill(self.color)
        pygame.draw.rect(surface, (60, 60, 70), surface.get_rect(), 2)

        self.sprite = surface
        return self.sprite
