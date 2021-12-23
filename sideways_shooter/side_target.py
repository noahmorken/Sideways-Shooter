import pygame
from pygame.sprite import Sprite

class Target(Sprite):
    """A class to manage the target."""

    def __init__(self, tp_game):
        """Create a target object at the right of the screen."""
        super().__init__()
        self.screen = tp_game.screen
        self.settings = tp_game.settings
        self.color = self.settings.target_color

        # Start the target near the top right of the screen.
        self.rect = pygame.Rect(0, 0, self.settings.target_width,
            self.settings.target_height)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the target's exact vertical position.
        self.y = float(self.rect.y)

    def check_edges(self):
        """Return True if target is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
            return True

    def update(self):
        """Move the target up or down."""
        self.y += self.settings.target_speed * self.settings.target_direction
        self.rect.y = self.y

    def draw_target(self):
        """Draw the target to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)