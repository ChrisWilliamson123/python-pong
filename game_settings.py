class GameSettings:
    """Shared game settings"""
    def __init__(self):
        self._ball_speed_level = 5
        self._paddle_speed_level = 6

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