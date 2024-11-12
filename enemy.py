import pygame
from enum import Enum
from actor import Actor
import values

class Color(Enum):
    PROFILE     = 1 # 縦断
    CROSS       = 2 # 横断
    ZIGZAG      = 3 # ジグザク
    CIRCULAR    = 4 # 円運動
    BOSS        = 5 # ボス

# 敵クラス
class Enemy(Actor):
    def __init__(self, x, y, move_pattern, type, cycle, amplitude):
        super().__init__(
            values.enemy_values['ENEMY_SIZE_' + type], 
            x,
            y, 
            values.enemy_values['ENEMY_SPEED_' + type], 
            values.enemy_values['ENEMY_LIVES_' + type], 
            values.enemy_values['ENEMY_COLOR_' + type]
        )
        self.move_pattern = move_pattern
        self.type = type
        self.true_type = type
        self.score = values.enemy_values['ENEMY_SCORE_' + type]
        self.originX = x
        self.originY = y
        self.cycle = cycle
        self.amplitude = amplitude

        image = pygame.image.load("enemy.png")

        if self.move_pattern == "down":
            rotate = 180
        elif self.move_pattern == "right":
            rotate = 270
        else:
            rotate = 90

        source_x = 0
        source_y = 0
        source_w = 32
        source_h = 32

        if self.type == "STRAIGHT":
            source_x = 32
        if self.type == "ZIGZAG":
            source_y = 32
        if self.type == "STOP":
            rotate = 180
        if self.type == "FAST":
            source_x = 32
            source_y = 32
        if self.type == "BOSS":
            source_w = 64
            source_h = 64
            image = pygame.image.load("boss.png")
            rotate = 180

        clip_rect = pygame.Rect(source_x, source_y, source_w, source_h)
        image = image.subsurface(clip_rect) # クリップ
        image = pygame.transform.scale(image, (self.size, self.size))  # リサイズ
        self.image = pygame.transform.rotate(image, rotate) # 回転

    def move(self):
        pass

    def fire(self, enemy_bullets):
        pass

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
