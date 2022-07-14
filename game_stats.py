class GameStats:
    def __init__(self, ai_game) -> None:
        self.settings = ai_game.settings
        self.reset_stats()
        with open('high_score.txt', 'r') as f:
            self.high_score = int(f.read())
    
    def reset_stats(self) -> None:
        self.ships_left = self.settings.ship_limit
        self.bombs_left = self.settings.bomb_limit
        self.games_active = False
        self.score = 0
    
    def update_high_score(self) -> None:
        if self.score > self.high_score:
            self.high_score = self.score
            return True