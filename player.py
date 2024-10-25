from actor import Actor
import values

# プレイヤークラス
class Player(Actor):
    def __init__(self, canvas):
        super().__init__(
            canvas, 
            values.PLAYER_SIZE, 
            values.WIDTH / 2, 
            values.HEIGHT - 50, 
            values.PLAYER_SPEED, 
            values.PLAYER_LIVES, 
            values.PLAYER_COLOR
        )
        self.invincible = False
        self.invincible_time = 0

    def move(self, direction):
        dx = dy = 0
        if direction == "up" and self.y > self.height/2:
            dy -= self.speed
        elif direction == "down" and self.y + self.height < values.HEIGHT - self.height/2:
            dy += self.speed
        elif direction == "left" and self.x > self.width/2:
            dx -= self.speed
        elif direction == "right" and self.x + self.width < values.WIDTH - self.width/2:
            dx += self.speed

        super().move(dx, dy)

    def fire(self, bullets):
        super().fire(
            bullets,
            values.PLAYER_BULLET_SIZE,
            values.PLAYER_BULLET_SPEED,
            values.PLAYER_BULLET_COLOR
        )
