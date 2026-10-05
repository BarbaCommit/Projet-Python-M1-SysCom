from model.tile import Tile

class VoidTile(Tile):

    def __init__(self, col: int, row: int):
        super().__init__(col,row,friction_factor=1.0,color=(0,0,0))