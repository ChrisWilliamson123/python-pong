import pygame
from states.state import State
from states.state_type import StateType

class PauseState(State):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_manager.change_state(StateType.GAME)

    def update(self, dt):
        pass  # No updates needed for a static menu

    def render(self):
        self.game_manager.render_previous_state() # Render the underlying game state
        text = self.font.render('PAUSED', True, (255, 255, 255))
        rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, rect)
