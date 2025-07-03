import pygame

from constants import SCREEN_WIDTH

from states.state import State
from states.state_type import StateType

class MenuState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.text_opacity = 20
        self.direction = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.game_manager.change_state(StateType.GAME)
            # self.next_state = FadeTransition(self.game, self, PlayState(self.game), 1)

    def update(self, dt):
        self.text_opacity = self.text_opacity + ((382.5 * dt) * self.direction)
        if self.text_opacity >= 255:
            self.direction = -1
        if self.text_opacity <= 20:
            self.direction = 1
        
    def render(self):
        self.screen.fill('black')
        # Title
        title_text = self.font_title.render("PONG", True, 'white')
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_text, title_rect)

        text = self.font_body.render('Press SPACE to play', True, 'white')
        text.set_alpha(self.text_opacity)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(text, text_rect)
