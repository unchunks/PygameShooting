import time
import random
from bullet import *

# プレイヤークラス
class Player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = 40
        self.height = 40
        self.x = values.WIDTH / 2
        self.y = values.HEIGHT - 50
        self.speed = 10
        self.lives = 3
        self.invincible = False
        self.invincible_time = 0
        self.player_shape = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height, fill="blue"
        )

    def move(self, direction):
        if direction == "up" and self.y > 1:
            self.y -= self.speed
        elif direction == "down" and self.y + self.height < values.HEIGHT - 1:
            self.y += self.speed
        elif direction == "left" and self.x > 1:
            self.x -= self.speed
        elif direction == "right" and self.x + self.width < values.WIDTH - 1:
            self.x += self.speed

        self.canvas.coords(self.player_shape, self.x, self.y, self.x + self.width, self.y + self.height)

    def fire(self, bullets):
        bullets.append(Bullet(self.canvas, self.x + self.width / 2, self.y))

# 敵クラス
class Enemy:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = 40
        self.height = 40
        self.x = random.randint(0, values.WIDTH - self.width)
        self.y = 0
        self.speed = random.randint(1, 3)
        self.enemy_shape = self.canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill="red")
        self.last_shot_time = time.time()

    def move(self):
        self.y += self.speed
        self.canvas.coords(self.enemy_shape, self.x, self.y, self.x + self.width, self.y + self.height)
        if self.y > values.HEIGHT:
            self.canvas.delete(self.enemy_shape)
            return False
        return True

    def fire(self, enemy_bullets):
        if time.time() - self.last_shot_time > 1:
            enemy_bullets.append(EnemyBullet(self.canvas, self.x + self.width / 2, self.y + self.height))
            self.last_shot_time = time.time()