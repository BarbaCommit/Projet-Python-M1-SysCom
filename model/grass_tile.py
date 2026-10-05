from model.tile import Tile

class GrassTile(Tile):

    def __init__(self, col: int, row: int):
        super().__init__(col,row,friction_factor = 0.85,color = (0, 204, 0))
