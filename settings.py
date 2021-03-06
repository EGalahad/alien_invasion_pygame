class Settings:
    """class to store and manipulate settings of the game"""

    def __init__(self) -> None:
        """initialise the setting for the game"""
        # screen and appearance
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_max = 3

        # bomb settings
        self.bomb_limit = 5

        # alien settings
        self.alien_drop_speed = 10

        self.speedup_scale = 1.1

        self.init_dynamic_settings()
    
    def init_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.bomb_speed = 1.0
        self.alien_speed = 0.4

        self.fleet_direction = 1

        self.alien_points = 50
    
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.bomb_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.speedup_scale)