import sys
import pygame
from  time import sleep
from game_stats import GameStats
from settings import Settings
from ship import Ship
from bullet import Bullet
from bomb import Bomb
from alien import Alien



class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.game_active = True

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_bombs()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(120)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_t:
            self._fire_bomb()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _fire_bomb(self):
        if len(self.bombs) < self.settings.bomb_allowed:
            new_bomb = Bomb(self)
            self.bombs.add(new_bomb)
            new_bomb.rect.x = self.ship.rect.centerx
            new_bomb.rect.y = self.ship.rect.top
            new_bomb.speed_y = -self.settings.bomb_speed
        # 可以在这里立即开始爆炸计时，但通常在碰撞或其他事件时触发
        # new_bomb.explode_bomb()  # 如果要立即爆炸，可以取消注释这行
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _update_bombs(self):
        self.bombs.update()
        for bomb in self.bombs.copy():
            if bomb.rect.bottom <= 0:
                self.bombs.remove(bomb)
            elif pygame.sprite.spritecollide(bomb, self.aliens, False):
                bomb.explode_bomb()
        self._check_bomb_alien_collisions()

    def _check_bomb_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bombs, self.aliens, False, True)
        if not self.aliens:
            self.bombs.empty()
            self._create_fleet()
    def _create_fleet(self):
        alien = Alien(self)
        new_alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        current_x,current_y = alien_width,alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height
    def _create_alien(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bomb in self.bombs.sprites():
            if not bomb.explode:
                bomb.draw_bomb()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()
    def _ship_hit(self):
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False



    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break




if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
