from model.tile import Tile

class IceTile(Tile):

    def __init__(self, col: int, row: int):
        super().__init__(col,row,friction_factor = 0.98,color = (153,255,255))
