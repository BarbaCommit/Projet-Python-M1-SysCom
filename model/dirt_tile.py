from model.tile import Tile

class DirtTile(Tile):

    def __init__(self, col: int, row: int):
        super().__init__(col,row,friction_factor = 0.60, color = (102, 51, 0))
