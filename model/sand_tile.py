from model.tile import Tile

class SandTile(Tile):

    def __init__(self, col: int, row: int):
        super().__init__(col,row,friction_factor = 0.015,color = (255, 229, 204))
