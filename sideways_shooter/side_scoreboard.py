import pygame.font
from pygame.sprite import Group

from side_ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.highest_score = ai_game.highest_score

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_all_time_high()
        self.prep_level()
        self.prep_ships()

        # Loads the all time high score.
        self.stats.score = self.highest_score.load_score()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)

        # Display the score at the bottom right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.bottom = self.screen_rect.bottom - self.score_rect.height

    def show_score(self):
        """Draw scores, levels, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.record_image, self.record_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)

        # Center the high score at the middle right of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.score_rect.right
        self.high_score_rect.centery = self.screen_rect.centery - 20

    def prep_all_time_high(self):
        """Turn the record into a rendered image."""
        record = round(self.highest_score.load_score(), -1)
        record_str = "{:,}".format(record)
        self.record_image = self.font.render(record_str, True,
                self.text_color, self.settings.bg_color)
        
        # Position the highest score below the high score.
        self.record_rect = self.record_image.get_rect()
        self.record_rect.right = self.score_rect.right
        self.record_rect.centery = self.screen_rect.centery + 20

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def check_final_high_score(self):
        """Saves a new highest score if achieved."""
        if self.stats.score > self.stats.high_score:
            self.all_time_high.save_score(self.stats.score)
            self.prep_all_time_high()

    def check_all_time_high_score(self):
        """Saves a new all time highest score if achieved."""
        record = self.highest_score.load_score()
        if self.stats.high_score > record:
            self.highest_score.save_score(self.stats.high_score)
            self.prep_all_time_high()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = self.screen_rect.right - ship.rect.width
            ship.rect.y = 10 + ship_number * ship.rect.width
            self.ships.add(ship)