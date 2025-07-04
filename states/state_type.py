from enum import Enum

class StateType(Enum):
    MENU = 'menu'
    GAME = 'game'
    PAUSE = 'pause'
    GAME_OVER = 'game_over'
    SETTINGS = 'settings'
