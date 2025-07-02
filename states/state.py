from abc import ABC, abstractmethod

class State(ABC):
    """Abstract base class for all game states"""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.screen = game_manager.screen
        self.settings = game_manager.settings
        
    @abstractmethod
    def handle_event(self, event):
        """Handle events received by Pygame"""
        pass
    
    @abstractmethod
    def update(self, dt):
        """Handle updates that should be performed independent of events"""
        pass
    
    @abstractmethod
    def render(self):
        """Render the state to the display"""
        pass
