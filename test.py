import pygame
import random
import sys

# 初期化
pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D弾幕ゲーム")

# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# プレイヤー設定
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10
player_lives = 3

# 敵設定
enemy_size = 50
enemies = []
enemy_speed = 5

# 敵弾設定
enemy_bullet_size = 10
enemy_bullets = []

# プレイヤー弾設定
player_bullet_size = 5
player_bullets = []
player_bullet_speed = 15

# フォント設定
font = pygame.font.SysFont("Arial", 24)

# スコア
score = 0

# クロック
clock = pygame.time.Clock()

# 敵の生成
def spawn_enemy():
    direction = random.choice(["left", "right", "down"])
    if direction == "left":
        enemy_x = WIDTH - enemy_size
        enemy_y = random.randint(0, HEIGHT // 2)
    elif direction == "right":
        enemy_x = 0
        enemy_y = random.randint(0, HEIGHT // 2)
    elif direction == "down":
        enemy_x = random.randint(0, WIDTH - enemy_size)
        enemy_y = 0
    enemies.append([enemy_x, enemy_y, direction])

# ゲームループ
while True:
    screen.fill(WHITE)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キー入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += player_speed
    if keys[pygame.K_SPACE]:
        player_bullets.append([player_pos[0] + player_size // 2, player_pos[1]])

    # 敵の生成
    if random.randint(1, 25) == 1:
        spawn_enemy()

    # 敵の移動
    for enemy in enemies[:]:
        if enemy[2] == "left":
            enemy[0] -= enemy_speed
        elif enemy[2] == "right":
            enemy[0] += enemy_speed
        elif enemy[2] == "down":
            enemy[1] += enemy_speed

        if random.randint(1, 50) == 1:
            enemy_bullets.append([enemy[0] + enemy_size // 2, enemy[1] + enemy_size])
        if enemy[0] < 0 or enemy[0] > WIDTH or enemy[1] > HEIGHT:
            enemies.remove(enemy)

    # 敵弾の移動
    for bullet in enemy_bullets[:]:
        bullet[1] += 7
        if bullet[1] > HEIGHT:
            enemy_bullets.remove(bullet)

    # プレイヤー弾の移動
    for bullet in player_bullets[:]:
        bullet[1] -= player_bullet_speed
        if bullet[1] < 0:
            player_bullets.remove(bullet)

    # 衝突判定 (敵弾とプレイヤー)
    for bullet in enemy_bullets[:]:
        if (player_pos[0] < bullet[0] < player_pos[0] + player_size and
                player_pos[1] < bullet[1] < player_pos[1] + player_size):
            player_lives -= 1
            enemy_bullets.remove(bullet)
            if player_lives == 0:
                print("Game Over!")
                pygame.quit()
                sys.exit()

    # 衝突判定 (プレイヤー弾と敵)
    for bullet in player_bullets[:]:
        for enemy in enemies[:]:
            if (enemy[0] < bullet[0] < enemy[0] + enemy_size and
                    enemy[1] < bullet[1] < enemy[1] + enemy_size):
                if bullet in player_bullets:
                    player_bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                    score += 10
                break

    # プレイヤーの描画
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    # 敵の描画
    for enemy in enemies:
        pygame.draw.rect(screen, BLACK, (enemy[0], enemy[1], enemy_size, enemy_size))

    # 敵弾の描画
    for bullet in enemy_bullets:
        pygame.draw.circle(screen, RED, (bullet[0], bullet[1]), enemy_bullet_size)

    # プレイヤー弾の描画
    for bullet in player_bullets:
        pygame.draw.circle(screen, GREEN, (bullet[0], bullet[1]), player_bullet_size)

    # プレイヤーの残基表示
    lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
    screen.blit(lives_text, (10, 10))

    # スコア表示
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 40))

    # フレームレート表示
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, BLACK)
    screen.blit(fps_text, (WIDTH - 100, 10))

    # 画面更新
    pygame.display.flip()

    # フレームレート
    clock.tick(30)
