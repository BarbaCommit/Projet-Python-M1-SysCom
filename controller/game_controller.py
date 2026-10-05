import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    GameState, PALETTE_TILE_SIZE
)
from model.game_model import GameModel
from view.game_view import GameView
from controller.input_handler import InputHandler


class GameController:

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.model = GameModel()
        self.view = GameView(self.screen)
        self.input_handler = InputHandler()
        self.running = True

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                if self.model.state == GameState.COLOR_SELECTION:
                    ox, oy = self.view.get_palette_origin()
                    mx, my = event.pos
                    self.model.select_color_at_pixel(mx, my, ox, oy,PALETTE_TILE_SIZE)
    def handle_keydown(self, key: int) -> None:
        state = self.model.state

        if state == GameState.MENU:
            self.handle_menu_key(key)
        elif state == GameState.COLOR_SELECTION:
            self.handle_color_selection_key(key)

    def handle_menu_key(self, key: int) -> None:
        if key == pygame.K_RETURN:
            self.model.state = GameState.COLOR_SELECTION
        elif key == pygame.K_ESCAPE:
            self.quit()

    def handle_color_selection_key(self, key: int) -> None:
        if key == pygame.K_RETURN:
            self.model.load_circuit()
            self.model.state = GameState.RACING
        elif key == pygame.K_ESCAPE:
            self.model.state = GameState.MENU


    def update(self) -> None:
        if self.model.state != GameState.RACING:
            return

        p1_input = self.input_handler.get_inputs(self.input_handler.p1_mapping)
        p2_input = self.input_handler.get_inputs(self.input_handler.p2_mapping)

        car1 = self.model.cars[0]
        car2 = self.model.cars[1]

        self.apply_input(car1, p1_input)
        self.apply_input(car2, p2_input)
        self.model.update()

    def apply_input(self, car, player_input) -> None:
        if player_input['accelerate']:
            car.accelerate()
        if player_input['decelerate']:
            car.decelerate()
        if player_input['turn_right']:
            car.turn_right()
        if player_input['turn_left']:
            car.turn_left()

    def render(self) -> None:
        self.view.draw(self.model)

    def quit(self) -> None:
        self.running = False
        pygame.quit()
        sys.exit()
