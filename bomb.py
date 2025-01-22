import pygame
from pygame.sprite import Sprite

class Bomb(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/bomb.jpg').convert_alpha()  # 确保使用透明背景的炸弹图片
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.speed_factor = self.settings.bomb_speed
        self.explode = False  # 标记炸弹是否爆炸
        self.explode_time_left = 0
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bomb_color
        self.rect = pygame.Rect(0,0,self.settings.bomb_radius,self.settings.bomb_radius)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.radius =  self.settings.bomb_radius
        self.y = float(self.rect.y)

    def update(self):
        self.calculate_gravity()

        if self.explode:
            self.explode_time_left -= self.ai_game.clock.get_time() / 1000.0  # 以秒为单位减少时间
            if self.explode_time_left <= 0:
                self.kill()  # 爆炸动画结束后删除炸弹
        else:
            self.rect.y += self.speed_y
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def calculate_gravity(self):
        # 此方法通常用于计算炸弹的垂直移动，根据游戏需要调整
        if self.rect.y >= self.ai_game.settings.screen_height:
            self.kill()


    def draw_bomb(self):
        self.image = pygame.image.load('images/1.jpg').convert_alpha()
        if self.explode:
            # 绘制爆炸动画（例如，使用一个更大的爆炸图片或改变颜色）
            # 这里简单处理为不显示炸弹，实际应显示爆炸动画
            pass  # 或者绘制一个爆炸图像
        else:
            self.ai_game.screen.blit(self.image, self.rect)

    def explode_bomb(self):
        self.explode = True
        self.explode_time_left = 0.06  # 60毫秒
        # 可以添加代码来替换或修改self.image为爆炸图像
        # 例如：self.image = pygame.image.load('explosion.png').convert_alpha()


    def draw_bomb(self):
        pygame.draw.circle(self.screen, self.color, self.rect.midtop, self.radius)