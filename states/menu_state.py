# states/menu_state.py

import pygame
from states.play_state import PlayState
from states.base_state import GameState
from transitions.fade_transition import FadeTransition

class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont('Arial', 40)

    def handle_events(self, events):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            # self.next_state = PlayState(self.game)
            self.next_state = FadeTransition(self.game, self, PlayState(self.game), 1)

    def update(self, dt):
        pass  # No updates needed for a static menu

    def render(self):
        self.screen.fill("darkblue")
        text = self.font.render("Press SPACE to Play", True, (255, 255, 255))
        rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, rect)
        pygame.display.flip()
