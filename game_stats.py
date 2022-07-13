class GameStats:
    def __init__(self, ai_game) -> None:
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0
    
    def reset_stats(self) -> None:
        self.ships_left = self.settings.ship_limit
        self.games_active = False
        self.score = 0