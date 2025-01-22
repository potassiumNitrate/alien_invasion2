class Settings:
    def __init__(self):
        self.screen_width = 1400
        self.screen_height = 800
        self.bg_color = (255, 192, 203)
        self.ship_speed = 20
        self.ship_limit = 3
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 120
        self.bomb_speed = 3.0
        self.bomb_color = (255,0,0)
        self.bomb_radius = 3
        self.bomb_allowed = 1
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1