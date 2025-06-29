import pygame
from states.menu_state import MenuState

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.state = MenuState(self)

    def handle_quit(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.state.running = False
                break

    def run(self):
        while self.state.running:
            dt = self.clock.tick(60) / 1000
            events = pygame.event.get()

            self.handle_quit(events)
            
            self.state.handle_events(events)
            self.state.update(dt)
            self.state.render()

            # Handle state transition
            if self.state.next_state:
                self.state = self.state.next_state

        pygame.quit()

if __name__ == "__main__":
    Game().run()