from enum import Enum

from data_classes.score import Score

class ContextKey(Enum):
    SCORE = 'score'

class GameContext:
    def __init__(self):
        self._context = {
            ContextKey.SCORE: Score()
        }

    # Getters and setters for underlying context properties
    @property
    def score(self):
        return self._context[ContextKey.SCORE]

    @score.setter
    def score(self, score):
        self._context[ContextKey.SCORE] = score

    def reset_score(self):
        self.score = Score()

    # Computed properties
    @property
    def winner(self):
        return self.score.winner
