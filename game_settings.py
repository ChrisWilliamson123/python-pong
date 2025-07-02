class GameSettings:
    """Shared game settings"""
    def __init__(self):
        self._ball_speed = 5
        self._paddle_speed = 6

    @property
    def ball_speed(self):
        return self._ball_speed
    
    @ball_speed.setter
    def ball_speed(self, speed):
        self._ball_speed = max(1, min(10, speed))  # Clamp between 1-10

    @property
    def paddle_speed(self):
        return self._paddle_speed
    
    @paddle_speed.setter
    def paddle_speed(self, speed):
        self._paddle_speed = max(1, min(10, speed))  # Clamp between 1-10