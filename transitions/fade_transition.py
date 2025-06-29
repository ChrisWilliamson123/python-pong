# transitions/fade_transition.py

import pygame
from states.base_state import GameState

class FadeTransition(GameState):
    def __init__(self, game, from_state, to_state, duration=1.0):
        super().__init__(game)
        self.from_state = from_state
        self.to_state = to_state
        self.duration = duration
        self.elapsed = 0.0
        self.overlay = pygame.Surface(game.screen.get_size()).convert()
        self.overlay.fill((0, 0, 0))

    def handle_events(self, events):
        pass  # Block input during transition

    def update(self, dt):
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.next_state = self.to_state
        else:
            alpha = int(255 * (self.elapsed / self.duration))
            self.overlay.set_alpha(alpha)

    def render(self):
        # Render the outgoing screen
        self.from_state.render()
        self.screen.blit(self.overlay, (0, 0))
        pygame.display.flip()
