import pygame
from states.base_state import GameState
from transitions.fade_transition import FadeTransition
from renderers.text_renderer import TextRenderer

class GameOverState(GameState):
    def __init__(self, game, winner):
        super().__init__(game)

        self.winner = winner
        self.font = pygame.font.SysFont('Arial', 40)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                from states.play_state import PlayState
                self.next_state = FadeTransition(self.game, self, PlayState(self.game), 1)    

    def update(self, dt):
        pass  # No updates needed for a static menu

    def render(self):
        self.screen.fill('black')
        text = f'GAME OVER\n{self.winner} Wins\nPress SPACE for new game'
        TextRenderer.draw_multiline_text_centered(self.screen, text, self.font, 'white', (self.screen.get_width() // 2, self.screen.get_height() // 2))
        pygame.display.flip()
