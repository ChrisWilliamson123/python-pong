from abc import ABC, abstractmethod

class StatefulComponent(ABC):
    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def render(self, screen):
        pass
