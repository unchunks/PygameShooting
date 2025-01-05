import pygame
from character import Character
import values

# プレイヤークラス
class Player(Character):
    def __init__(self, win_width, win_height):
        super().__init__(
            values.PLAYER_SIZE, 
            win_width // 2, 
            win_height - 2 * values.PLAYER_SIZE, 
            values.PLAYER_SPEED, 
            values.PLAYER_LIVES, 
            values.PLAYER_COLOR,
            values.PLAYER_BULLET_SIZE,
            values.PLAYER_BULLET_SPEED,
            values.PLAYER_BULLET_COLOR,
            "images/player.png"
        )
        # 弾のレベル
        self.bullet_level: int = 1

        # 弾強化の時間制限用
        self.timestamp: int = 0

        image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(image, (self.size, self.size))  # リサイズ

    def fire(self) -> list:
        bullets = []
        if pygame.time.get_ticks() - self.timestamp > 5000:
            self.bullet_level = 1
        if self.bullet_level == 1:
            # 上
            bullets.append(self.shoot(values.UP))
        elif self.bullet_level > 1:
            # 上
            bullets.append(self.shoot(values.UP))
            # 右上
            bullets.append(self.shoot(values.RIGHT_UP))
            # 左上
            bullets.append(self.shoot(values.LEFT_UP))
        return bullets
