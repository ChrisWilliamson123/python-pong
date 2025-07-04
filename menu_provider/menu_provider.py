from dataclasses import dataclass
from typing import Callable, List

import pygame

from constants import SCREEN_WIDTH

from stateful_component.stateful_component import StatefulComponent

@dataclass
class MenuEntryAction():
    key: int # pygame.k_* are ints
    func: Callable

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.key:
            self.func()

@dataclass
class MenuEntry():
    text: Callable[[], str]
    actions: List[MenuEntryAction]

@dataclass
class Menu():
    title: str
    entries: List[MenuEntry]

class MenuProvider(StatefulComponent):
    """Provides the ability to navigate through and perform actions on menu items"""
    def __init__(self, menu, font_title, font_entry, should_flash_selected=False, selected_color='white', deselected_color='gray', spacing=24):
        self.menu = menu
        self.menu_entries = menu.entries
        self.font_title = font_title
        self.font_entry = font_entry
        self.selection_index = 0
        self.should_flash_selected = should_flash_selected
        self.selected_text_opacity = 20 if should_flash_selected else 255
        self.opacity_transition_direction = 1
        self.opacity_change_rate = 382.5 # Full opacity change in 0.66s, because maths
        self.selected_color = selected_color
        self.deselected_color = deselected_color
        self.spacing = spacing

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.selection_index = (self.selection_index + 1) % len(self.menu_entries)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.selection_index = (self.selection_index - 1) % len(self.menu_entries)

        selected_entry = self.menu_entries[self.selection_index]
        for action in selected_entry.actions:
            action.handle_event(event)

    def update(self, dt):
        if self.should_flash_selected:
            self.selected_text_opacity = self.selected_text_opacity + ((382.5 * dt) * self.opacity_transition_direction)
            if self.selected_text_opacity >= 255:
                self.opacity_transition_direction = -1
            if self.selected_text_opacity <= 20:
                self.opacity_transition_direction = 1

    def render(self, screen):
        title_text = self.font_title.render(self.menu.title, True, 'white')
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(title_text, title_rect)

        for i, entry in enumerate(self.menu_entries):
            color = self.selected_color if i == self.selection_index else self.deselected_color
            text = self.font_entry.render(entry.text(), True, color)
            if self.should_flash_selected and i == self.selection_index:
                text.set_alpha(self.selected_text_opacity)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + (i * 60)))
            screen.blit(text, text_rect)
