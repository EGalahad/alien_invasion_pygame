import pygame


class Ship:
    def __init__(self, ai_game) -> None:
        """init position of the ship"""
        self.screen: pygame.Surface = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)

        self.move_right = False
        self.move_left = False

    def center_ship(self) -> None:
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = self.rect.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.move_right and self.rect.right + self.settings.ship_speed < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.move_left and self.rect.left - self.settings.ship_speed > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x
