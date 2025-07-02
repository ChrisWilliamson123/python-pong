import pygame

from constants import *

from states.state_type import StateType
from states.menu_state import MenuState
from states.game_state import GameState

from game_settings import GameSettings

class GameManager:
    """Manages game states and shared resources"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.settings = GameSettings()
        # TODO: Winner

        self.states = {
            StateType.MENU: MenuState(self),
            StateType.GAME: GameState(self)
        }

        self.current_state = self.states[StateType.MENU]
        self.running = True

    def change_state(self, new_state_type):
        self.current_state = self.states[new_state_type]

    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(60) / 1000 # TODO: Put framerate in settings

            # Event handling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_state.handle_event(event)

            self.current_state.update(dt)
            self.current_state.render()

            pygame.display.flip()
        
        pygame.quit()