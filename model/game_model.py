from constants import GameState, GRID_ROWS, GRID_COLS, PALETTE_COLS, PALETTE_ROWS, TILE_SIZE
from model.car import Car
from model.circuit import Circuit, CIRCUIT1, create_tile, TILE_MAPPING
from model.tile import Tile
import colorsys

class GameModel:

    def __init__(self):
        self.state: str = GameState.MENU
        self.circuit: Circuit | None = None
        self.cars:list[Car] = []
        self.selected_colors:list[tuple[int,int,int]] = [(255,0,0),(0,0,255)]
        self.index_selection_courant:int = 0
        self.palette = self._generate_palette(PALETTE_COLS,PALETTE_ROWS)
        
    def load_circuit(self) -> None:
        self.circuit = Circuit(grid=[])

        grid = []
        for row_index,row_data in enumerate(CIRCUIT1):
            row_tiles = []
            for col_index, char in enumerate(row_data):
                tile = create_tile(char,col=col_index,row=row_index)
                row_tiles.append(tile)
            grid.append(row_tiles)
        self.circuit = Circuit(grid=grid)


        self.spawn_car(7,1,self.selected_colors[0])
        self.spawn_car(8,1,self.selected_colors[1])

    def spawn_car(self,x:float,y:float,color:tuple[int,int,int]) -> None:
        self.cars.append(Car(x, y, color))

    def update(self) -> None:
        if self.state != GameState.RACING or self.circuit is None:
            return

        spawn_pos = [(7*TILE_SIZE + TILE_SIZE //2,1*TILE_SIZE+TILE_SIZE//2),
                     (8*TILE_SIZE + TILE_SIZE //2,1*TILE_SIZE+TILE_SIZE//2)
        ]
        for i,c in enumerate(self.cars):
            
            tile = self.circuit.get_tile_at_pixel(c.x,c.y)
            if tile is None or isinstance(tile,TILE_MAPPING.get("V")):
                spawn_x,spawn_y = spawn_pos[i]
                c.respawn(spawn_x,spawn_y,angle=90.0)
                continue
            self.check_collisions(c)
            friction = tile.friction_factor
            c.update_position(tile_friction=friction)
            
        # for c in self.cars:
        #     tile = self.circuit.get_tile_at_pixel(c.x,c.y)
        #     if tile:
        #         friction = tile.friction_factor
        #     else:
        #         friction = 0.90
            
        #     c.update_position(tile_friction=friction)

    def _generate_palette(self,cols,rows):
        palette = []
        for r in range(rows):
            row_color = []
            val = 0.1 + 0.9 * (1.0 - (r / (rows - 1)))
            for c in range(cols):
                if c == cols - 1:
                    gray = int(val*255)
                    color = (gray,gray,gray)
                else:
                    teinte = c / (cols -1)
                    red,green,blue = colorsys.hsv_to_rgb(teinte,0.85,val)
                    color = (int(red*255),int(green*255),int(blue*255))
                row_color.append(color)
            palette.append(row_color)
        return palette

    def select_color_at_pixel(self,mouse_x:int,mouse_y:int,grid_x:int,grid_y:int,tile_size:int) -> bool:
        if(grid_x <= mouse_x < grid_x + PALETTE_COLS * tile_size and grid_y <= mouse_y < grid_y + PALETTE_ROWS * tile_size):
            col = (mouse_x - grid_x) // tile_size
            row = (mouse_y - grid_y) // tile_size
            color = self.palette[row][col]

            self.selected_colors[self.index_selection_courant] = color
            self.index_selection_courant = (self.index_selection_courant+1)%2
            return True
        return False

    def check_collisions(self,car : Car) -> None:
        if self.circuit is None:
            return False
        
        map_width, map_height = self.circuit.pixel_width(),self.circuit.pixel_height()
        hitbox = car.get_hitbox()

        out_x, out_y = 0.0, 0.0


        for car_x, car_y in hitbox:
            if car_x < 0:
                out_x = max(out_x,-car_x)
            elif car_x >= map_width:
                out_x = min(out_x,map_width-1-car_x)
            
            if car_y < 0:
                out_y = max(out_y,-car_y)
            elif car_y >= map_height:
                out_y = min(out_y,map_height-1-car_y)
        if out_x != 0 or out_y != 0:
            car.x += out_x
            car.y += out_y

            if out_x != 0:
                car.vx = -car.vx *0.3
                car.vy *= 0.85
            if out_y != 0:
                car.vy = -car.vy *0.3
                car.vx *= 0.85
            return