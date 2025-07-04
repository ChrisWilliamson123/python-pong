from abc import ABC

import pygame

class State(ABC):
    """Abstract base class for all game states"""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.screen = game_manager.screen
        self.settings = game_manager.settings

        self.font_title = pygame.font.Font(None, 74)
        self.font_body = pygame.font.Font(None, 36)

        self.components = []

    def add_component(self, component):
        self.components.append(component)
 
    def handle_event(self, event):
        """Handle events received by Pygame"""
        for component in self.components:
            component.handle_event(event)

    def update(self, dt):
        """Handle updates that should be performed independent of events"""
        for component in self.components:
            component.update(dt)

    def render(self):
        """Render the state to the display"""
        for component in self.components:
            component.render(self.screen)
