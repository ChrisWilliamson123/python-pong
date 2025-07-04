from dataclasses import dataclass
from typing import Callable, List
import pygame

from constants import SCREEN_WIDTH

from states.state import State
from states.state_type import StateType

class PauseState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        menu_entries = [
            MenuEntry('RESUME', [MenuEntryAction(pygame.K_RETURN, self.resume)]),
            # ('RESUME', self.resume),
            MenuEntry('MAIN MENU', [MenuEntryAction(pygame.K_RETURN, self.navigate_to_main_menu)])
            # ('MAIN MENU', self.navigate_to_main_menu)
        ]
        self.menu_provider = MenuProvider(menu_entries)

    def handle_event(self, event):
        self.menu_provider.handle_event(event)

    def update(self, dt):
        pass  # No updates needed for a static menu

    def render(self):
        self.screen.fill("black")

        # Title
        title_text = self.font_title.render("PAUSED", True, 'white')
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_text, title_rect)

        # Menu options
        for i, entry in enumerate(self.menu_provider.menu_entries):
            color = 'white' if i == self.menu_provider.selection_index else 'gray'
            text = self.font_body.render(entry.text, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + (i * 60)))
            self.screen.blit(text, text_rect)

    def resume(self):
        self.game_manager.change_state(StateType.GAME)

    def navigate_to_main_menu(self):
        self.game_manager.change_state(StateType.MENU)

@dataclass
class MenuEntryAction():
    key: int # pygame.k_* are ints
    func: Callable

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.key:
            self.func()

@dataclass
class MenuEntry():
    text: str
    actions: List[MenuEntryAction]


class MenuProvider():
    def __init__(self, menu_entries):
        self.menu_entries = menu_entries
        self.selection_index = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.selection_index = (self.selection_index + 1) % len(self.menu_entries)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.selection_index = (self.selection_index - 1) % len(self.menu_entries)

        selected_entry = self.menu_entries[self.selection_index]
        for action in selected_entry.actions:
            action.handle_event(event)