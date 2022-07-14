from random import randint
import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from bomb import Bomb
from alien import Alien
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """class to manage game resource and behaviour"""

    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()

        full_screen = False
        if full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        # self._create_fleet()

        self.play_button = Button(self, "Play")

    def _create_fleet(self) -> None:
        """populate the self.aliens group"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        num_aliens_x = available_space_x // (2 * alien_width)

        available_space_y = self.settings.screen_height - \
            (3 * alien_height) - self.ship.rect.height
        number_rows = available_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(num_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, col, row) -> None:
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width * (1 + 2 * col)
        alien.rect.x = alien.x
        alien.rect.y = alien_height * (1 + 2 * row)
        self.aliens.add(alien)

    def run_game(self) -> None:
        while True:
            self._check_events()

            if self.stats.games_active:
                self.ship.update()
                self._update_bullets()
                self._update_bombs()
                self._update_aliens()

                if self.stats.update_high_score():
                    self.sb.prep_high_score()

            self._update_screen()

    def _check_events(self) -> None:
        # monitor mouse and keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_play_button(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                self._check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up_events(event)

    def _check_play_button(self, mouse_pos):
        playbutoon_rect: pygame.Surface = self.play_button.rect
        button_clicked = playbutoon_rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.games_active:
            self._start_game()

    def _start_game(self):
        pygame.mouse.set_visible(False)

        self.settings.init_dynamic_settings()

        self.stats.reset_stats()
        self.stats.games_active = True
        self.sb.prep_score()

        self.aliens.empty()
        self.bullets.empty()
        self.bombs.empty()

        self._create_fleet()
        self.ship.center_ship()

    def _end_game(self):
        with open("high_score.txt", "w") as f:
            f.write(str(self.stats.high_score))
        pygame.mouse.set_visible(True)
        sys.exit()

    def _check_key_down_events(self, event) -> None:
        if event.key == pygame.K_LEFT:
            self.ship.move_left = True
        elif event.key == pygame.K_RIGHT:
            self.ship.move_right = True
        elif event.key == pygame.K_p:
            self._start_game()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            self._end_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_UP:
            self._fire_bomb()

    def _check_key_up_events(self, event) -> None:
        if event.key == pygame.K_LEFT:
            self.ship.move_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.move_right = False

    def _update_bullets(self) -> None:
        self.bullets.update()
        # remove bullets that are out of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()

    def _check_bullet_alien_collision(self) -> None:
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            self.stats.score += self.settings.alien_points * len(collisions)
            self.sb.prep_score()
            if not self.aliens:
                self.bullets.empty()
                self.bombs.empty()
                self._create_fleet()
                self.settings.increase_speed()

    def _update_bombs(self) -> None:
        self.bombs.update()
        # remove bullets that are out of the screen
        for bomb in self.bombs.copy():
            if bomb.rect.bottom <= 0:
                self.bombs.remove(bomb)

        self._check_bomb_alien_collision()

    def _check_bomb_alien_collision(self) -> None:
        collisions = pygame.sprite.groupcollide(
            self.bombs, self.aliens, True, False
        )
        bomb: Bomb = None
        for each_bomb in collisions:
            if collisions[each_bomb] is not None:
                bomb = each_bomb
                break
        if bomb is not None:
            x, y = bomb.rect.center

            pygame.draw.circle(self.screen, (255, 0, 0),
                               (x, y), bomb.harm_radius)
            pygame.display.flip()
            sleep(0.5)

            for alien in self.aliens.copy():
                dist = (alien.rect.x - x) ** 2 + (alien.rect.y - y) ** 2
                if dist < (bomb.harm_radius ** 2):
                    self.stats.score += self.settings.alien_points
                    self.aliens.remove(alien)
            self.sb.prep_score()

            if not self.aliens:
                self.bullets.empty()
                self.bombs.empty()
                self._create_fleet()
                self.settings.increase_speed()

    def _update_aliens(self) -> None:
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_alien_bottom()

    def _check_fleet_edges(self) -> None:
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self) -> None:
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed + randint(-5, 5)
        self.settings.fleet_direction *= -1

    def _check_alien_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self) -> None:
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_left_ships()

            self.aliens.empty()
            self.bullets.empty()
            self.bombs.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.games_active = False
            pygame.mouse.set_visible(True)

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_max:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _fire_bomb(self):
        if self.stats.bombs_left > 0:
            new_bomb = Bomb(self)
            self.bombs.add(new_bomb)
            self.stats.bombs_left -= 1
            self.sb.prep_left_bombs()

    def _update_screen(self) -> None:
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for bomb in self.bombs.sprites():
            bomb.draw_bomb()

        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.games_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
