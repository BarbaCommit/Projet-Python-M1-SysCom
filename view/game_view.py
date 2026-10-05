import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE,
    COLOR_BG, COLOR_TEXT, COLOR_ACCENT, COLOR_PANEL, COLOR_PANEL_BORDER,
    GameState, PALETTE_COLS, PALETTE_ROWS, PALETTE_TILE_SIZE
)
from model.game_model import GameModel


class GameView:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, model: GameModel) -> None:
        self.screen.fill(COLOR_BG)
        if model.state == GameState.MENU:
            self._draw_menu(model)
        elif model.state == GameState.RACING:
            self._draw_racing(model)
        elif model.state == GameState.COLOR_SELECTION:
            self._draw_color_selection_screen(model)
        pygame.display.flip()

    def _draw_menu(self, model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2

        title_surf = self.font.render(
            "Jeu de course 2D", True, COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 160)))

        options = [("JOUER (Enter)", GameState.RACING),
                   ("QUITTER (Escape)", None)]
        for i, (label, _) in enumerate(options):
            y = 320 + i * 80
            rect = pygame.Rect(cx - 140, y - 25, 280, 50)
            pygame.draw.rect(self.screen, COLOR_PANEL, rect, border_radius=8)
            pygame.draw.rect(self.screen, COLOR_PANEL_BORDER,
                             rect, 2, border_radius=8)
            text_surf = self.font.render(
                label, True, COLOR_ACCENT if i == 0 else COLOR_TEXT)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_racing(self, model: GameModel) -> bool:

        for row_idx, row in enumerate(model.circuit.grid):
            for col_idx, tile in enumerate(row):
                sprite = tile.get_sprite(TILE_SIZE)
                self.screen.blit(
                    sprite, (col_idx * TILE_SIZE, row_idx * TILE_SIZE))

        if model.circuit is None:
            return

        for car in model.cars:
            surf, rect = car.get_rotated_sprite()
            self.screen.blit(surf, rect)

    def _draw_color_selection_screen(self,model: GameModel) -> None:
        cx = WINDOW_WIDTH // 2 
        title_surf = self.font.render("Choix des couleurs",True,COLOR_ACCENT)
        self.screen.blit(title_surf, title_surf.get_rect(center=(cx, 80)))
        self._draw_color_picker(model)
        info_surf = self.font.render("Appuyez sur ENTRÉE pour lancer la course", True, COLOR_TEXT)
        self.screen.blit(info_surf, info_surf.get_rect(center=(cx, WINDOW_HEIGHT - 80)))


    def get_palette_origin(self) -> tuple[int,int]:
        x = (WINDOW_WIDTH - (PALETTE_COLS * PALETTE_TILE_SIZE)) // 2
        y = (WINDOW_HEIGHT - (PALETTE_ROWS * PALETTE_TILE_SIZE)) // 2
        return x, y

    def _draw_color_picker(self,model:GameModel) -> None:
        x, y = self.get_palette_origin()

        for r in range(PALETTE_ROWS):
            for c in range(PALETTE_COLS):
                rect = pygame.Rect(
                    x + c * PALETTE_TILE_SIZE,
                    y + r * PALETTE_TILE_SIZE,
                    PALETTE_TILE_SIZE,
                    PALETTE_TILE_SIZE
                )
                pygame.draw.rect(self.screen,model.palette[r][c],rect)
                pygame.draw.rect(self.screen,(0,0,0),rect,1)

        labels = ["Joueur 1" , "Joueur 2"]
        base_y = y + (PALETTE_ROWS * PALETTE_TILE_SIZE) + 20

        for i in range(2):
            x = (WINDOW_WIDTH // 2) - 100 + (i * 110)
            rect = pygame.Rect(x, base_y, 90, 40)

            pygame.draw.rect(self.screen, model.selected_colors[i], rect)

            is_active = model.index_selection_courant == i
            border_color = (255, 215, 0) if is_active else (200, 200, 200)
            border_width = 4 if is_active else 2
            pygame.draw.rect(
                self.screen, border_color, rect, border_width, border_radius=4
            )

            lbl_surf = self.font.render(labels[i], True, COLOR_TEXT)
            self.screen.blit(
                lbl_surf, lbl_surf.get_rect(center=(rect.centerx, rect.centery - 35))
            )