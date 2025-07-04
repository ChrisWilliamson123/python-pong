import pygame

from menu_provider.menu_provider import MenuEntry, MenuEntryAction, MenuProvider, Menu

from states.state import State
from states.state_type import StateType

class MainMenuState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.text_opacity = 20
        self.opacity_direction = 1

        menu_entries = [
            MenuEntry(lambda: 'Play', [MenuEntryAction(pygame.K_RETURN, lambda: self.game_manager.change_state(StateType.GAME))]),
            MenuEntry(lambda: 'Settings', [MenuEntryAction(pygame.K_RETURN, lambda: self.game_manager.change_state(StateType.SETTINGS))]),
        ]
        menu = Menu('PONG', menu_entries)
        menu_provider = MenuProvider(menu, self.font_title, self.font_body, should_flash_selected=False)
        self.add_component(menu_provider)

    def render(self):
        self.screen.fill('black')

        super().render()
