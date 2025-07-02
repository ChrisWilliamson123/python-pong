import pygame
import sys
from abc import ABC, abstractmethod
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_SIZE = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

class StateType(Enum):
    MENU = "menu"
    GAME = "game"
    OPTIONS = "options"
    PAUSE = "pause"

class GameSettings:
    """Shared game settings that persist across states"""
    def __init__(self):
        self.ball_speed = 5
        self.paddle_speed = 6
        self.ai_difficulty = 0.8  # AI paddle speed multiplier
        
    def get_ball_speed(self):
        return self.ball_speed
    
    def set_ball_speed(self, speed):
        self.ball_speed = max(1, min(10, speed))  # Clamp between 1-10

class GameState(ABC):
    """Abstract base class for all game states"""
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.screen = game_manager.screen
        self.settings = game_manager.settings
        
    @abstractmethod
    def handle_event(self, event):
        pass
    
    @abstractmethod
    def update(self, dt):
        pass
    
    @abstractmethod
    def render(self):
        pass

class MenuState(GameState):
    """Main menu state"""
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = pygame.font.Font(None, 74)
        self.menu_font = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ["Start Game", "Settings", "Quit"]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # Start Game
                    self.game_manager.change_state(StateType.GAME)
                elif self.selected_option == 1:  # Settings
                    self.game_manager.change_state(StateType.OPTIONS)
                elif self.selected_option == 2:  # Quit
                    pygame.quit()
                    sys.exit()
    
    def update(self, dt):
        pass
    
    def render(self):
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font.render("PONG", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Menu options
        for i, option in enumerate(self.options):
            color = WHITE if i == self.selected_option else GRAY
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 60))
            self.screen.blit(text, text_rect)
        
        # Instructions
        inst_text = pygame.font.Font(None, 24).render("Use UP/DOWN to navigate, ENTER to select", True, GRAY)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(inst_text, inst_rect)

class OptionsState(GameState):
    """Options/Settings state"""
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = pygame.font.Font(None, 48)
        self.menu_font = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ["Ball Speed", "Back"]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_LEFT and self.selected_option == 0:
                # Decrease ball speed
                self.settings.set_ball_speed(self.settings.ball_speed - 1)
            elif event.key == pygame.K_RIGHT and self.selected_option == 0:
                # Increase ball speed
                self.settings.set_ball_speed(self.settings.ball_speed + 1)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 1:  # Back
                    self.game_manager.change_state(StateType.MENU)
    
    def update(self, dt):
        pass
    
    def render(self):
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font.render("OPTIONS", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        # Ball Speed setting
        speed_color = WHITE if self.selected_option == 0 else GRAY
        speed_text = self.menu_font.render(f"Ball Speed: {self.settings.ball_speed}", True, speed_color)
        speed_rect = speed_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(speed_text, speed_rect)
        
        # Back option
        back_color = WHITE if self.selected_option == 1 else GRAY
        back_text = self.menu_font.render("Back", True, back_color)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, 350))
        self.screen.blit(back_text, back_rect)
        
        # Instructions
        inst_text = pygame.font.Font(None, 24).render("LEFT/RIGHT to adjust, UP/DOWN to navigate, ENTER to select", True, GRAY)
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
        self.screen.blit(inst_text, inst_rect)

class Ball:
    def __init__(self, x, y, settings):
        self.x = x
        self.y = y
        self.settings = settings
        self.reset_velocity()
        
    def reset_velocity(self):
        import random
        self.dx = self.settings.get_ball_speed() * random.choice([-1, 1])
        self.dy = self.settings.get_ball_speed() * random.choice([-1, 1])
    
    def update(self, dt):
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off top and bottom
        if self.y <= 0 or self.y >= SCREEN_HEIGHT - BALL_SIZE:
            self.dy = -self.dy
    
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.reset_velocity()
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, BALL_SIZE, BALL_SIZE)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        
    def update(self, dt, settings):
        self.y += self.speed * settings.paddle_speed
        self.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

class GamePlayState(GameState):
    """Main game playing state"""
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = pygame.font.Font(None, 74)
        self.reset_game()
        
    def reset_game(self):
        self.player1 = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.player2 = Paddle(SCREEN_WIDTH - 70, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.settings)
        self.score1 = 0
        self.score2 = 0
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_manager.change_state(StateType.PAUSE)
    
    def update(self, dt):
        # Handle player input
        keys = pygame.key.get_pressed()
        self.player1.speed = 0
        if keys[pygame.K_w]:
            self.player1.speed = -1
        elif keys[pygame.K_s]:
            self.player1.speed = 1
            
        # Simple AI for player 2
        ball_center = self.ball.y + BALL_SIZE // 2
        paddle_center = self.player2.y + PADDLE_HEIGHT // 2
        
        if ball_center < paddle_center - 10:
            self.player2.speed = -self.settings.ai_difficulty
        elif ball_center > paddle_center + 10:
            self.player2.speed = self.settings.ai_difficulty
        else:
            self.player2.speed = 0
        
        # Update game objects
        self.player1.update(dt, self.settings)
        self.player2.update(dt, self.settings)
        self.ball.update(dt)
        
        # Ball collision with paddles
        if self.ball.get_rect().colliderect(self.player1.get_rect()) or \
           self.ball.get_rect().colliderect(self.player2.get_rect()):
            self.ball.dx = -self.ball.dx
        
        # Scoring
        if self.ball.x < 0:
            self.score2 += 1
            self.ball.reset()
        elif self.ball.x > SCREEN_WIDTH:
            self.score1 += 1
            self.ball.reset()
    
    def render(self):
        self.screen.fill(BLACK)
        
        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(self.screen, WHITE, (SCREEN_WIDTH // 2 - 2, y, 4, 10))
        
        # Draw paddles
        pygame.draw.rect(self.screen, WHITE, self.player1.get_rect())
        pygame.draw.rect(self.screen, WHITE, self.player2.get_rect())
        
        # Draw ball
        pygame.draw.rect(self.screen, WHITE, self.ball.get_rect())
        
        # Draw scores
        score_text = self.font.render(f"{self.score1}  {self.score2}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(score_text, score_rect)
        
        # Draw instructions
        inst_text = pygame.font.Font(None, 24).render("W/S to move, ESC to pause", True, GRAY)
        self.screen.blit(inst_text, (10, SCREEN_HEIGHT - 30))

class PauseState(GameState):
    """Pause state"""
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = pygame.font.Font(None, 74)
        self.menu_font = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ["Resume", "Main Menu"]
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # Resume
                    self.game_manager.change_state(StateType.GAME)
                elif self.selected_option == 1:  # Main Menu
                    self.game_manager.change_state(StateType.MENU)
            elif event.key == pygame.K_ESCAPE:
                self.game_manager.change_state(StateType.GAME)
    
    def update(self, dt):
        pass
    
    def render(self):
        self.screen.fill(BLACK)
        
        # Title
        title_text = self.font.render("PAUSED", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title_text, title_rect)
        
        # Menu options
        for i, option in enumerate(self.options):
            color = WHITE if i == self.selected_option else GRAY
            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 60))
            self.screen.blit(text, text_rect)

class GameManager:
    """Manages game states and shared resources"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong - State Based")
        self.clock = pygame.time.Clock()
        self.settings = GameSettings()
        
        # Initialize states
        self.states = {
            StateType.MENU: MenuState(self),
            StateType.GAME: GamePlayState(self),
            StateType.OPTIONS: OptionsState(self),
            StateType.PAUSE: PauseState(self)
        }
        
        self.current_state = self.states[StateType.MENU]
        self.running = True
    
    def change_state(self, state_type):
        """Change the current game state"""
        if state_type == StateType.GAME and isinstance(self.current_state, (MenuState, PauseState)):
            # Reset game if coming from menu
            if isinstance(self.current_state, MenuState):
                self.states[StateType.GAME].reset_game()
        
        self.current_state = self.states[state_type]
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.current_state.handle_event(event)
            
            # Update current state
            self.current_state.update(dt)
            
            # Render current state
            self.current_state.render()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameManager()
    game.run()