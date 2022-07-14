from lib2to3.pygram import python_grammar
import pygame
from pygame.sprite import Sprite

class Bomb(Sprite):
    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen:pygame.Surface = ai_game.screen
        self.settings = ai_game.settings
        self.color = (255, 0, 0)
        
        self.rect = pygame.rect.Rect(
            0, 0, 1, 1)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

        self.radius = 10
        self.harm_radius = 150

        self.speed = self.settings.bomb_speed

    def update(self) -> None:
        self.y -= self.speed
        self.rect.y = self.y
    
    def draw_bomb(self) -> None:
        pygame.draw.circle(self.screen, self.color, (self.rect.x, self.rect.y), self.radius)