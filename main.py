import pygame
from controller.game_controller import GameController


def main():
    pygame.init()
    pygame.display.set_caption("TracKart League")

    controller = GameController()
    controller.run()

    pygame.quit()


if __name__ == "__main__":
    main()
