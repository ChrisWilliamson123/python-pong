from dataclasses import dataclass

@dataclass
class Score:
    player_one: int = 0
    player_two: int = 0
    max: int = 10

    @property
    def winner(self):
        if self.player_one == self.max:
            return "Player One"
        if self.player_two == self.max:
            return "Player Two"
