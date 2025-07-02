import pygame
from entities.paddle import Paddle
from entities.ball import Ball
from dataclasses import dataclass

from states.state import State
# from states.game_over_state import GameOverState

@dataclass
class Score:
    player_one: int = 0
    player_two: int = 0
    max: int = 2

class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        # self.round_started = False
        self.scores = Score()

        # Game dimensions
        self.screen_size = self.screen.get_size()

        # Entities
        self.reset_paddles()
        self.reset_ball()

        # Font
        self.font = pygame.font.SysFont('Arial', 30)

    def reset_paddles(self):
        self.paddle_one = Paddle(10, 250, 10, 100, 400)
        self.paddle_two = Paddle(self.screen_size[0] - 20, 250, 10, 100, 400)

    def reset_ball(self):
        self.ball = Ball(self.screen_size[0] / 2, self.screen_size[1] / 2, 10, self.settings)

    def handle_event(self, event):
        pass
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     self.round_started = not self.round_started

    def update(self, dt):
        # Handling continuous input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddle_one.move(-1, dt, self.screen_size[1])
        if keys[pygame.K_s]:
            self.paddle_one.move(1, dt, self.screen_size[1])
        if keys[pygame.K_UP]:
            self.paddle_two.move(-1, dt, self.screen_size[1])
        if keys[pygame.K_DOWN]:
            self.paddle_two.move(1, dt, self.screen_size[1])

        # Handling non input-dependent logic
        self.ball.move(dt, self.screen_size)

        if self.paddle_one.rect.colliderect(self.ball.rect):
            self.ball.mirror_x()
        elif self.paddle_two.rect.colliderect(self.ball.rect):
            self.ball.mirror_x()

        if self.ball.is_over_x(self.screen_size[0]):
            self.scores.player_one += 1
            self.reset_round()
        elif self.ball.is_under_x():
            self.scores.player_two += 1
            self.reset_round()

        # if winner := self.get_winner():
        #     self.next_state = GameOverState(self.game, winner)

    def get_winner(self):
        if self.scores.player_one == self.scores.max:
            return 'Player 1'
        if self.scores.player_two == self.scores.max:
            return 'Player 2'

    def reset_round(self):
        self.round_started = False
        self.reset_ball()
        self.reset_paddles()

    def render(self):
        self.screen.fill("black")
        self.paddle_one.draw(self.screen)
        self.paddle_two.draw(self.screen)
        self.ball.draw(self.screen)

        score_text = self.font.render(f'{self.scores.player_one} - {self.scores.player_two}', True, (255, 255, 255))
        self.screen.blit(score_text, (self.screen_size[0] // 2 - score_text.get_width() // 2, 20))
