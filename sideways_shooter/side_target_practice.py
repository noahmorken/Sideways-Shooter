import sys
from time import sleep

import pygame

from side_settings import Settings
from side_stats import GameStats
from side_button import Button
from side_ship import Ship
from side_bullet import Bullet
from side_target import Target

class TargetPractice:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()

        # These lines are for fullscreen.
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        # These lines are for windowed.
        # self.screen = pygame.display.set_mode(
        #     (self.settings.screen_width, self.settings.screen_height))
        
        pygame.display.set_caption("Target Practice")

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.target = pygame.sprite.Group()

        self._create_target()

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_target()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Responds to keypresses."""
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Responds to key releases."""
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()
            self.settings.initialize_dynamic_settings()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
                self._target_missed()

        self._check_bullet_target_collisions()

    def _check_bullet_target_collisions(self):
        """Respond to bullet-target collisions."""
        # Remove any bullets that have hit the target.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.target, True, False)
        if collisions:
            for bullet in self.bullets.copy():
                self.bullets.remove(bullet)
            self.settings.increase_speed()

    def _create_target(self):
        # Create the target.
        target = Target(self)
        target_width, target_height = target.rect.size
        target.y = self.settings.screen_height // 2 - (target_height // 2)
        target.rect.y = target.y
        target.rect.x = self.settings.screen_width - target.rect.width
        self.target.add(target)

    def _update_target(self):
        """
        Check if the target is at an edge,
          then update the position of the target.
        """
        self._check_target_edges()
        self.target.update()

    def _check_target_edges(self):
        """Respond appropriately if the target has reached an edge."""
        for target in self.target.sprites():
            if target.check_edges():
                self._change_target_direction()

    def _change_target_direction(self):
        """Change the target's direction."""
        self.settings.target_direction *= -1

    def _target_missed(self):
        """Respond to the ship missing the target."""
        if self.stats.ships_left > 0:
            # Decrement ships left.
            self.stats.ships_left -= 1

            # Get rid of the target and bullets.
            self.target.empty()
            self.bullets.empty()
        
            # Create a new target and center the ship.
            self._create_target()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    
    def _start_game(self):
        """Starts a game of Target Practice."""
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of the target and bullets.
        self.target.empty()
        self.bullets.empty()

        # Create a new target and center the ship.
        self._create_target()
        self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for target in self.target.sprites():
            target.draw_target()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    tp = TargetPractice()
    tp.run_game()