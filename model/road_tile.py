from model.tile import Tile

class RoadTile(Tile):

    def __init__(self, col: int, row: int):
       super().__init__(col,row,friction_factor = 0.30,color = (80, 80, 90))