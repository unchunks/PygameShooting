from actor import Actor
from bullet import *
import values

# プレイヤークラス
class Player(Actor):
    def __init__(self):
        super().__init__(
            values.PLAYER_SIZE, 
            values.WIDTH // 2, 
            values.HEIGHT - 2 * values.PLAYER_SIZE, 
            values.PLAYER_SPEED, 
            values.PLAYER_LIVES, 
            values.PLAYER_COLOR
        )

    def move(self, dir):
        pass

    def fire(self) -> list:
        bullets = []
        if self.bullet_level == 1:
            # 中央
            bullets.append(Bullet(
                values.PLAYER_BULLET_SIZE, 
                self.x + self.size // 2, 
                self.y, 
                0,
                -values.PLAYER_BULLET_SPEED, 
                values.PLAYER_BULLET_COLOR,
            ))
        else:
            # 中央
            bullets.append(Bullet(
                values.PLAYER_BULLET_SIZE, 
                self.x + self.size // 2, 
                self.y, 
                0,
                -values.PLAYER_BULLET_SPEED,
                values.PLAYER_BULLET_COLOR,
            ))
            # 右上
            bullets.append(Bullet(
                values.PLAYER_BULLET_SIZE, 
                self.x + self.size // 2, 
                self.y, 
                values.PLAYER_BULLET_SPEED / 3,
                -values.PLAYER_BULLET_SPEED, 
                values.PLAYER_BULLET_COLOR,
            ))
            # 左上
            bullets.append(Bullet(
                values.PLAYER_BULLET_SIZE, 
                self.x + self.size // 2, 
                self.y, 
                -values.PLAYER_BULLET_SPEED / 3,
                -values.PLAYER_BULLET_SPEED, 
                values.PLAYER_BULLET_COLOR,
            ))
        return bullets
