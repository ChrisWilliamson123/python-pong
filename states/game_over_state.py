import pygame

from states.state import State
from states.state_type import StateType
from renderers.text_renderer import TextRenderer

class GameOverState(State):
    def __init__(self, game):
        super().__init__(game)

        self.context = game.context
        self.font = pygame.font.SysFont('Arial', 40)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game_manager.change_state(StateType.GAME)

    def update(self, dt):
        pass  # No updates needed for a static menu

    def render(self):
        self.screen.fill('black')
        text = f'GAME OVER\n{self.context.winner} Wins\nPress SPACE for new game'
        TextRenderer.draw_multiline_text_centered(self.screen, text, self.font, 'white', (self.screen.get_width() // 2, self.screen.get_height() // 2))
