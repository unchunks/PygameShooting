import pygame
from actor import Actor
from bullet import Bullet
import values


# 敵クラス
class Enemy(Actor):
    def __init__(self, x: int, y: int, move_direction: tuple, type: str, cycle: int, amplitude: int):
        super().__init__(
            values.enemy_values['ENEMY_SIZE_' + type], 
            x,
            y, 
            values.enemy_values['ENEMY_SPEED_' + type], 
            values.enemy_values['ENEMY_LIVES_' + type], 
            values.enemy_values['ENEMY_COLOR_' + type],
            values.enemy_values['ENEMY_BULLET_SIZE_' + type],
            values.enemy_values['ENEMY_BULLET_SPEED_' + type],
            values.enemy_values['ENEMY_BULLET_COLOR_' + type],
            self.resource_path("images/enemy.png")
        )

        # 移動方向 [UP, DOWN, LEFT, RIGHT]
        self.move_direction = move_direction

        # 現在の移動タイプ ["STOP", "STRAIGHT", "ZIGZAG", "FAST", "BOSS"]
        self.type = type
        # 元の移動タイプ（BOSS用） ["STOP", "STRAIGHT", "ZIGZAG", "FAST", "BOSS"]
        self.true_type = type

        # 倒した際のスコア
        self.score = values.enemy_values['ENEMY_SCORE_' + type]

        # 基準座標と周期、振幅(ZIGZAG用)
        self.originX = x
        self.originY = y
        self.cycle = cycle
        self.amplitude = amplitude

        if self.move_direction == values.DOWN:
            rotate = 180
        elif self.move_direction == values.RIGHT:
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
            source_x = 64
            source_w = 64
            source_h = 64
            rotate = 180

        image = pygame.image.load(self.image_path)
        clip_rect = pygame.Rect(source_x, source_y, source_w, source_h)
        image = image.subsurface(clip_rect) # クリップ
        image = pygame.transform.scale(image, (self.size, self.size))  # リサイズ
        self.image = pygame.transform.rotate(image, rotate) # 回転

    def move(self):
        super().move(self.move_direction)

    def fire(self) -> list:
        bullets = []
        if self.true_type != "BOSS":
            # 下
            bullets.append(super().shoot(values.DOWN))
        else:
            # 下
            bullets.append(super().shoot(values.DOWN))
            # 上
            bullets.append(super().shoot(values.UP))
            # 右下
            bullets.append(super().shoot(values.RIGHT_DOWN))
            # 左下
            bullets.append(super().shoot(values.LEFT_DOWN))
        return bullets

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
