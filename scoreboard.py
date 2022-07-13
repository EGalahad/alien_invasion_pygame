import pygame.font


class Scoreboard:
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_left_lives()
        self.prep_high_score()
        

    def prep_score(self) -> None:
        score_str = "Score: " + str(self.stats.score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    
    def prep_left_lives(self) -> None:
        lives_str = "Left ships: " + str(self.stats.ships_left)
        self.left_lives_image = self.font.render(
            lives_str, True, self.text_color, self.settings.bg_color)
        self.left_lives_rect = self.left_lives_image.get_rect()
        self.left_lives_rect.right = self.screen_rect.right - 20
        self.left_lives_rect.top = self.score_rect.bottom + 20

    def prep_high_score(self):
        high_score_str = "High score: " + str(self.stats.high_score)
        
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
    def show_score(self) -> None:
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.left_lives_image, self.left_lives_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
