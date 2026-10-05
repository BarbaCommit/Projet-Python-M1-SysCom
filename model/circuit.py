from model.tile import Tile
from constants import TILE_SIZE

import model.road_tile
import model.grass_tile
import model.dirt_tile
import model.ice_tile
import model.sand_tile
import model.void_tile

TILE_MAPPING = {classe.__name__[0]: classe for classe in Tile.__subclasses__()}


CIRCUIT1 = [
            ["D","G","R","R","R","R","R","R","R","R","R","R","R","R","G","D"],
            ["G","R","R","R","R","R","R","R","R","R","R","R","R","R","R","G"],
            ["R","R","R","V","V","V","V","V","V","V","V","V","V","R","R","R"],
            ["R","R","V","V","V","V","V","V","V","V","V","V","V","V","R","R"],
            ["R","R","V","V","V","V","V","V","V","V","V","V","V","V","R","R"],
            ["R","R","V","V","V","I","I","S","S","I","I","V","V","V","R","R"],
            ["R","R","V","V","V","I","I","S","S","I","I","V","V","V","R","R"],
            ["R","R","V","V","V","V","V","V","V","V","V","V","V","V","R","R"],
            ["R","R","V","V","V","V","V","V","V","V","V","V","V","V","R","R"],
            ["R","R","R","V","V","V","V","V","V","V","V","V","V","R","R","R"],
            ["D","G","R","R","R","R","R","R","R","R","R","R","R","R","R","G"],
            ["D","G","R","R","R","R","R","R","R","R","R","R","R","R","G","D"],
            ]


def create_tile(char:str,col:int,row:int) -> Tile:
    tile_type = TILE_MAPPING.get(char,TILE_MAPPING.get("V"))
    return tile_type(col,row)


class Circuit:

    def __init__(self,  grid: list[list[Tile]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_tile(self, col: int, row: int) -> Tile | None:
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_tile_at_pixel(self, px: float, py: float) -> Tile | None:
        col = int(px // TILE_SIZE)
        row = int(py // TILE_SIZE)
        return self.get_tile(col, row)

    def pixel_width(self) -> int:
        return self.cols * TILE_SIZE

    def pixel_height(self) -> int:
        return self.rows * TILE_SIZE
