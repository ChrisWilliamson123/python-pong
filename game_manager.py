import pygame

from constants import *

from states.state_type import StateType
from states.menu_state import MenuState
from states.game_state import GameState
from states.game_over_state import GameOverState
import states.state_transition_logic as state_transition_logic

from game_settings import GameSettings
from game_context import GameContext

class StateManager:
    def __init__(self, states, current_state_type, state_transition_logic_fn):
        self.states = states
        self.current_state_type = current_state_type
        self.current_state = states[self.current_state_type]
        self.previous_state_type = None
        self.state_transition_logic_fn = state_transition_logic_fn # takes in states as param and performs logic based on state transition

    def change_state(self, new_state_type):
        self.state_transition_logic_fn(self.states, self.current_state_type, new_state_type)

        self.previous_state_type = self.current_state_type
        self.current_state = self.states[new_state_type]
        self.current_state_type = new_state_type

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
            StateType.GAME_OVER: GameOverState(self)
        }

        self.state_manager = StateManager(states, StateType.MENU, state_transition_logic.change_state)

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