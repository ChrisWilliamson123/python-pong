from dataclasses import dataclass

import json
import os

@dataclass
class GameSettings:
    """Shared game settings with JSON persistence"""
    
    SETTINGS_FILE = "settings.json"
    
    def __init__(self):
        self._ball_speed_level = 5
        self._paddle_speed_level = 6
        self._is_computer_enabled = False
        self._load_from_json()
    
    def _load_from_json(self):
        """Load settings from JSON file if it exists"""
        if os.path.exists(self.SETTINGS_FILE):
            try:
                with open(self.SETTINGS_FILE, 'r') as f:
                    data = json.load(f)
                    self._ball_speed_level = data.get('ball_speed_level', 5)
                    self._paddle_speed_level = data.get('paddle_speed_level', 6)
                    self._is_computer_enabled = data.get('is_computer_enabled', False)
            except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
                print(f"Error loading settings: {e}. Using defaults.")
                self._create_default_settings_file()
        else:
            self._create_default_settings_file()
    
    def _save_to_json(self):
        """Save current settings to JSON file"""
        data = {
            'ball_speed_level': self._ball_speed_level,
            'paddle_speed_level': self._paddle_speed_level,
            'is_computer_enabled': self._is_computer_enabled
        }
        try:
            with open(self.SETTINGS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def _create_default_settings_file(self):
        """Create default settings file"""
        self._save_to_json()

    @property
    def ball_speed_level(self):
        return self._ball_speed_level

    @ball_speed_level.setter
    def ball_speed(self, speed):
        self._ball_speed_level = max(1, min(10, speed))  # Clamp between 1-10

    @property
    def ball_speed_pps(self):
        return self._ball_speed_level * 100

    @property
    def paddle_speed_level(self):
        return self._paddle_speed_level

    @paddle_speed_level.setter
    def paddle_speed_level(self, speed):
        self._paddle_speed_level = max(1, min(10, speed))  # Clamp between 1-10

    @property
    def paddle_speed_pps(self):
        return self._paddle_speed_level * 100

    @property
    def is_computer_enabled(self):
        return self._is_computer_enabled

    def toggle_computer_enabled(self):
        self._is_computer_enabled = not self._is_computer_enabled
        self._save_to_json()
