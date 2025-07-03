import pygame

from constants import *

from states.state_type import StateType
from states.menu_state import MenuState
from states.game_state import GameState
from states.game_over_state import GameOverState
import states.state_router as state_router

from game_settings import GameSettings
from game_context import GameContext

class GameManager:
    """Manages game states and shared resources"""
    def __init__(self):
        # Pygame initialisation
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.settings = GameSettings()

        # TODO: Winner

        self.context = GameContext()

        # State initialisation
        self.states = {
            StateType.MENU: MenuState(self),
            StateType.GAME: GameState(self),
            StateType.GAME_OVER: GameOverState(self)
        }
        self.current_state_type = StateType.MENU
        self.current_state = self.states[self.current_state_type]
        self.previous_state_type = None

        # Ensure the game is running
        self.running = True

    def change_state(self, new_state_type):
        state_router.change_state(self.current_state_type, new_state_type, self.states)

        self.previous_state_type = self.current_state_type
        self.current_state = self.states[new_state_type]
        self.current_state_type = new_state_type

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