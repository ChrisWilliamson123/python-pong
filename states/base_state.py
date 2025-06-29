# states/base_state.py

from abc import ABC, abstractmethod

class GameState(ABC):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock
        self.running = True
        self.next_state = None

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self):
        pass
