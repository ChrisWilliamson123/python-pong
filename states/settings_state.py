import pygame

from menu_provider.menu_provider import MenuEntry, MenuEntryAction, MenuProvider, Menu

from states.state import State
from states.state_type import StateType

class SettingsState(State):
    def __init__(self, game_manager):
        super().__init__(game_manager)

        menu_entries = [
            MenuEntry(lambda: f'AI: {'ON' if self.settings.is_computer_enabled else 'OFF'}', [MenuEntryAction(pygame.K_RETURN, self.settings.toggle_computer_enabled)]),
            MenuEntry(lambda: f'Ball Speed: {self.settings.ball_speed_level}', [MenuEntryAction(pygame.K_LEFT, self.settings.decrement_ball_speed_level), MenuEntryAction(pygame.K_RIGHT, self.settings.increment_ball_speed_level)]),
            MenuEntry(lambda: f'Paddle Speed: {self.settings.paddle_speed_level}', [MenuEntryAction(pygame.K_LEFT, self.settings.decrement_paddle_speed_level), MenuEntryAction(pygame.K_RIGHT, self.settings.increment_paddle_speed_level)]),
        ]
        menu = Menu('SETTINGS', menu_entries)
        menu_provider = MenuProvider(menu, self.font_title, self.font_body)
        self.add_component(menu_provider)

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_manager.change_to_previous_state()

    def render(self):
        self.screen.fill("black")

        super().render()

    def resume(self):
        self.game_manager.change_state(StateType.GAME)

    def navigate_to_main_menu(self):
        self.game_manager.change_state(StateType.MENU)
