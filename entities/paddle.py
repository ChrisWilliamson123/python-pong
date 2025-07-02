import pygame

class Paddle:
    def __init__(self, x, y, width, height, settings):
        self.pos = pygame.Vector2(x, y)  # precise position
        self.width = width
        self.height = height
        self.settings = settings
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, direction, dt, screen_height):
        # direction: -1 (up), 1 (down), 0 (no movement)
        speed = self.settings.paddle_speed * 100
        self.pos.y += speed * direction * dt

        # Clamp to screen bounds
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y + self.height > screen_height:
            self.pos.y = screen_height - self.height

        # Sync rect to updated float position
        self.rect.y = round(self.pos.y)

    def draw(self, surface, color="white"):
        pygame.draw.rect(surface, color, self.rect)