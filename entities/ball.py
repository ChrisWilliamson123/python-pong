import math
import pygame
import random

class Ball:
    @staticmethod
    def takeoff_angle():
        if random.choice([True, False]):
            return random.randint(-45, 45)
        else:
            return random.randint(135, 225)

    def __init__(self, x, y, radius, settings):
        self.pos = pygame.Vector2(x, y)  # precise position
        self.radius = radius
        self.angle = Ball.takeoff_angle()
        self.rect = pygame.Rect(x, y, radius, radius)
        self.settings = settings

    def move(self, dt, screen_size):
        ball_speed = self.settings.ball_speed * 100
        velocity_vector = pygame.Vector2(ball_speed * math.cos(math.radians(self.angle)), ball_speed * math.sin(math.radians(self.angle)))

        self.pos.x += velocity_vector.x * dt
        self.pos.y += velocity_vector.y * dt

        # Mirror the ball's angle on edge hits to screen bounds
        screen_height = screen_size[1]
        if (self.pos.y < 0) or (self.pos.y + self.radius > screen_height):
            self.angle *= -1

        # Sync rect to updated float position
        self.rect.y = round(self.pos.y)
        self.rect.x = round(self.pos.x)

    def is_over_x(self, screen_width):
        return self.pos.x + self.radius > screen_width
    
    def is_under_x(self):
        return self.pos.x < 0

    def mirror_x(self):
        self.angle = 180 - self.angle

    def draw(self, surface, color="white"):
        pygame.draw.circle(surface, color, self.rect.center, self.radius)