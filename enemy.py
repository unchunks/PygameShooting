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
    def __init__(self, canvas):
        super().__init__(
            canvas, 
            values.ENEMY_SIZE, 
            random.randint(0, values.WIDTH - values.ENEMY_SIZE),
            0, 
            values.ENEMY_SPEED, 
            values.ENEMY_LIVES, 
            values.ENEMY_COLOR
        )
        self.last_shot_time = time.time()

    def move(self):
        dx = dy = 0
        dy += self.speed
        super().move(dx, dy)
        if self.y > values.HEIGHT:
            self.canvas.delete(self.shape)
            return False
        return True

    def fire(self, enemy_bullets):
        if time.time() - self.last_shot_time > 1:
            super().fire(
                enemy_bullets,
                values.ENEMY_BULLET_SIZE,
                values.ENEMY_BULLET_SPEED,
                values.ENEMY_BULLET_COLOR
            )
            self.last_shot_time = time.time()