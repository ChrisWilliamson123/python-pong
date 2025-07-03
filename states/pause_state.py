import pygame

from constants import SCREEN_WIDTH

from states.state import State
from states.state_type import StateType

class PauseState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.menu_entries = [ # TODO: Change to dicts?
            ('RESUME', self.resume),
            ('MAIN MENU', self.navigate_to_main_menu)
        ]
        self.menu_selection = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.menu_selection = (self.menu_selection + 1) % len(self.menu_entries)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.menu_selection = (self.menu_selection - 1) % len(self.menu_entries)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.menu_entries[self.menu_selection][1]()

    def update(self, dt):
        pass  # No updates needed for a static menu

    def render(self):
        self.screen.fill("black")

        # Title
        title_text = self.font_title.render("PAUSED", True, 'white')
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_text, title_rect)

        # Menu options
        for i, entry in enumerate(self.menu_entries):
            color = 'white' if i == self.menu_selection else 'gray'
            text = self.font_body.render(entry[0], True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + (i * 60)))
            self.screen.blit(text, text_rect)

    def resume(self):
        self.game_manager.change_state(StateType.GAME)

    def navigate_to_main_menu(self):
        self.game_manager.change_state(StateType.MENU)