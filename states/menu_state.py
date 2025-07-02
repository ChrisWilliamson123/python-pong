import pygame
from states.state import State
from states.state_type import StateType

class MenuState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = pygame.font.SysFont('Arial', 40)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game_manager.change_state(StateType.GAME)
            # self.next_state = FadeTransition(self.game, self, PlayState(self.game), 1)

    def update(self, dt):
        pass  # No updates needed for a static menu

    def render(self):
        self.screen.fill('black')
        text = self.font.render("Press SPACE to Play", True, (255, 255, 255))
        rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, rect)
        pygame.display.flip()
