import time
import random
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
        self.score = values.enemy_values['ENEMY_SCORE_' + type]
        self.originX = x
        self.originY = y
        self.cycle = cycle
        self.amplitude = amplitude

    def move(self):
        pass

    def fire(self, enemy_bullets):
        pass