import values

# 弾クラス
class Bullet:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = 15
        self.bullet_shape = self.canvas.create_rectangle(self.x - 5, self.y - 10, self.x + 5, self.y, fill="white")

    def move(self):
        self.y -= self.speed
        self.canvas.coords(self.bullet_shape, self.x - 5, self.y - 10, self.x + 5, self.y)
        if self.y < 0:
            self.canvas.delete(self.bullet_shape)
            return False
        return True
    
    def hit_test(self, enemy):
        # プレイヤーの弾と敵の衝突判定
        bullet_coords = self.canvas.bbox(self.bullet_shape)
        enemy_coords = self.canvas.bbox(enemy.enemy_shape)
        if bullet_coords and enemy_coords:
            if (bullet_coords[2] > enemy_coords[0] and  # bullet's right edge > enemy's left edge
                bullet_coords[0] < enemy_coords[2] and  # bullet's left edge < enemy's right edge
                bullet_coords[3] > enemy_coords[1] and  # bullet's bottom edge > enemy's top edge
                bullet_coords[1] < enemy_coords[3]):    # bullet's top edge < enemy's bottom edge
                return True
        return False

# 敵の弾クラス
class EnemyBullet:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.speed = 7
        self.bullet_shape = self.canvas.create_rectangle(self.x - 5, self.y, self.x + 5, self.y + 10, fill="yellow")

    def move(self):
        self.y += self.speed
        self.canvas.coords(self.bullet_shape, self.x - 5, self.y, self.x + 5, self.y + 10)
        if self.y > values.HEIGHT:
            self.canvas.delete(self.bullet_shape)
            return False
        return True
    
    def hit_test(self, player):
        # 敵の弾とプレイヤーの衝突判定
        bullet_coords = self.canvas.bbox(self.bullet_shape)
        player_coords = self.canvas.bbox(player.player_shape)
        if bullet_coords and player_coords:
            if (bullet_coords[2] > player_coords[0] and  # bullet's right edge > player's left edge
                bullet_coords[0] < player_coords[2] and  # bullet's left edge < player's right edge
                bullet_coords[3] > player_coords[1] and  # bullet's bottom edge > player's top edge
                bullet_coords[1] < player_coords[3]):    # bullet's top edge < player's bottom edge
                return True
        return False
