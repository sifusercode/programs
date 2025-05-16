#20250423-006 Start - Game statistics tracking
class GameStats:
    """Track game statistics."""
    
    def __init__(self,ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialize mutable statistics."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.aliens_destroyed = 0
        self.wave_cleared = True
#20250423-006 End