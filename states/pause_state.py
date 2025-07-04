import pygame

from menu_provider.menu_provider import MenuEntry, MenuEntryAction, MenuProvider, Menu

from states.state import State
from states.state_type import StateType

class PauseState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        menu_entries = [
            MenuEntry('RESUME', [MenuEntryAction(pygame.K_RETURN, self.resume)]),
            MenuEntry('MAIN MENU', [MenuEntryAction(pygame.K_RETURN, self.navigate_to_main_menu)])
        ]
        menu = Menu('PAUSED', menu_entries)
        menu_provider = MenuProvider(menu, self.font_title, self.font_body)
        self.add_component(menu_provider)

    def render(self):
        self.screen.fill("black")

        super().render()

    def resume(self):
        self.game_manager.change_state(StateType.GAME)

    def navigate_to_main_menu(self):
        self.game_manager.change_state(StateType.MENU)
