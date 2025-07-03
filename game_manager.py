import pygame

from constants import *

from states.state_type import StateType
from states.menu_state import MenuState
from states.game_state import GameState
from states.game_over_state import GameOverState
from states.pause_state import PauseState
from states.state_manager import StateManager
import states.state_transition_manager as state_transition_manager

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
        states = {
            StateType.MENU: MenuState(self),
            StateType.GAME: GameState(self),
            StateType.GAME_OVER: GameOverState(self),
            StateType.PAUSE: PauseState(self)
        }

        self.state_manager = StateManager(states, StateType.MENU, state_transition_manager.change_state)

        # Ensure the game is running
        self.running = True

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

    # State helpers
    @property
    def current_state(self):
        return self.state_manager.current_state
    
    def change_state(self, new_state_type):
        self.state_manager.change_state(new_state_type)

    def render_previous_state(self):
        self.state_manager.previous_state.render()