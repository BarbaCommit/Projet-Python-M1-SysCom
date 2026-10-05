import pygame


P1_MAPPING = {
    pygame.K_UP:        "accelerate",
    pygame.K_DOWN:      "decelerate",
    pygame.K_LEFT:      "turn_left",
    pygame.K_RIGHT:     "turn_right",
    pygame.K_KP_ENTER : "use"
}

P2_MAPPING = {
    pygame.K_z:         "accelerate",
    pygame.K_s:         "decelerate",
    pygame.K_q:         "turn_left",
    pygame.K_d:         "turn_right",
    pygame.K_SPACE :    "use"
}

class InputHandler:

    def __init__(self):
        self.p1_mapping = P1_MAPPING
        self.p2_mapping = P2_MAPPING

    def get_inputs(self,mapping : dict) -> dict:
        keys = pygame.key.get_pressed()

        p = {action: False for action in mapping.values()}

        for key, action in mapping.items():
            if keys[key]:
                p[action] = True

        return p
