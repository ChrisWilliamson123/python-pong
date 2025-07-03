import pygame
from entities.paddle import Paddle
from entities.ball import Ball

from states.state import State
from states.state_type import StateType

class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.context = game.context
        self.score = self.context.score

        # Game dimensions
        self.screen_size = self.screen.get_size()

        # Entities
        self.reset_paddles()
        self.reset_ball()

        # Font
        self.font = pygame.font.SysFont('Arial', 30)

    def reset_paddles(self):
        self.paddle_one = Paddle(10, 250, 10, 100, self.settings)
        self.paddle_two = Paddle(self.screen_size[0] - 20, 250, 10, 100, self.settings)

    def reset_ball(self):
        self.ball = Ball(self.screen_size[0] / 2, self.screen_size[1] / 2, 10, self.settings)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game_manager.change_state(StateType.PAUSE)

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
            self.score.player_one += 1
            self.reset_round()
        elif self.ball.is_under_x():
            self.score.player_two += 1
            self.reset_round()

        if self.context.winner:
            self.game_manager.change_state(StateType.GAME_OVER)

    def reset_round(self):
        self.reset_ball()
        self.reset_paddles()

    def reset(self):
        self.context.reset_score()
        self.score = self.context.score
        self.reset_round()

    def render(self):
        self.screen.fill("black")
        self.paddle_one.draw(self.screen)
        self.paddle_two.draw(self.screen)
        self.ball.draw(self.screen)

        score_text = self.font.render(f'{self.score.player_one} - {self.score.player_two}', True, (255, 255, 255))
        self.screen.blit(score_text, (self.screen_size[0] // 2 - score_text.get_width() // 2, 20))
