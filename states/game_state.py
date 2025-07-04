import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH

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
        if keys[pygame.K_UP] and not self.settings.is_computer_enabled:
            self.paddle_two.move(-1, dt, self.screen_size[1])
        if keys[pygame.K_DOWN] and not self.settings.is_computer_enabled:
            self.paddle_two.move(1, dt, self.screen_size[1])

        # Handling non input-dependent logic
        self.ball.move(dt, self.screen_size)

        # Moving player two automatically
        if self.settings.is_computer_enabled:
            ball_y = (self.ball.pos.y + (self.ball.radius // 2))
            paddle_y = (self.paddle_two.pos.y + (self.paddle_two.height // 2))
            if ball_y < paddle_y - 5:
                self.paddle_two.move(-1, dt, self.screen_size[1])
            elif ball_y > paddle_y + 5:
                self.paddle_two.move(1, dt, self.screen_size[1])

        if self.paddle_one.rect.colliderect(self.ball.rect):
            ball_center = (self.ball.pos.y + (self.ball.radius // 2))
            paddle_center = (self.paddle_one.pos.y + (self.paddle_one.height // 2))
            offset = (ball_center - paddle_center) / (self.paddle_one.height / 2)
            max_angle = 60  # degrees
            self.ball.angle = 0 + (offset * max_angle)
        elif self.paddle_two.rect.colliderect(self.ball.rect):
            ball_center = (self.ball.pos.y + (self.ball.radius // 2))
            paddle_center = (self.paddle_two.pos.y + (self.paddle_two.height // 2))
            offset = (ball_center - paddle_center) / (self.paddle_two.height / 2)
            max_angle = 60  # degrees
            self.ball.angle = 180 + (offset * max_angle)

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

        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(self.screen, 'white', (SCREEN_WIDTH // 2 - 2, y, 4, 10))

        self.paddle_one.draw(self.screen)
        self.paddle_two.draw(self.screen)
        self.ball.draw(self.screen)

        score_text = self.font_title.render(f'{self.score.player_one}   {self.score.player_two}', True, 'white')
        self.screen.blit(score_text, (self.screen_size[0] // 2 - score_text.get_width() // 2, 20))
