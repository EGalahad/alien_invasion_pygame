import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen:pygame.Surface = ai_game.screen
        self.settings = ai_game.settings
        self.color:tuple[int] = self.settings.bullet_color

        self.rect = pygame.rect.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        self.y = float(self.rect.y)

    def update(self) -> None:
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self) -> None:
        pygame.draw.rect(self.screen, self.color, self.rect)