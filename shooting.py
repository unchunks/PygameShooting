import pygame
import random
import sys
import math
import json
from actor import *
from player import *
from enemy import *
from item import *
from bullet import *

# 初期化
pygame.init()

# ウィンドウの作成
window = pygame.display.set_mode((values.WIDTH, values.HEIGHT))
pygame.display.set_caption("2D弾幕ゲーム")

# フォント設定
font_big = pygame.font.SysFont("hackgen", 48)
font_middle = pygame.font.SysFont("hackgen", 36)
font_small = pygame.font.SysFont("hackgen", 24)

# クロック
clock = pygame.time.Clock()

# 流れ星
stars = [[random.randint(0, window.get_width()), random.randint(0, window.get_height())] for _ in range(50)]

# スコア
score = 0
last_score = 0
high_scores = []

# スコアファイルのパス
SCORE_FILE = "high_scores.json"

# 画面
HOME = 0
GAME = 1
CLEAR = 2
OVER = 3

# キャラクターの初期化
player = Player()
player_bullets = []

enemies = []
enemy_bullets = []

items = []

# ゲーム内で使用する変数の初期化
def init_game():
    global score, last_score, player, player_bullets, enemies, enemy_bullets, items
    # スコア
    score = 0
    last_score = 0

    # キャラクターの初期化
    player = Player()
    player_bullets = []

    enemies = []
    enemy_bullets = []

    items = []

# スコアの読み込み
def load_scores():
    global high_scores
    try:
        with open(SCORE_FILE, "r") as file:
            high_scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        high_scores = [5000, 4000, 3000, 2000, 1000]

# スコアの保存
def save_score():
    global score, last_score, high_scores
    high_scores.append(score)
    last_score = score
    score = 0
    high_scores = sorted(high_scores, reverse=True)[:5]  # 上位5つのみ保持
    with open(SCORE_FILE, "w") as file:
        json.dump(high_scores, file)

# 敵の生成
def spawn_enemy(): # ["STRAIGHT", "ZIGZAG", "STOP", "FAST", "BOSS"]
    type = random.choices(values.enemy_types, weights = values.enemy_weights, k = 1)[0]
    # type = "BOSS"   
    direction = random.choice(["left", "right", "down"])
    enemy_x = random.randint(0, values.WIDTH - values.enemy_values['ENEMY_SIZE_' + type])
    enemy_y = random.randint(0, values.HEIGHT // 2)
    amplitude = random.randint(20, 50)
    cycle = random.randint(20, 30)
    if type != "STOP":
        if direction == "left":
            enemy_x = values.WIDTH - values.enemy_values['ENEMY_SIZE_' + type]
        elif direction == "right":
            enemy_x = 0
        elif direction == "down":
            enemy_y = 0
    enemies.append(Enemy(enemy_x, enemy_y, direction, type, amplitude, cycle))

# アイテムの生成
def spawn_item(): # ["HEAL", "SPEED", "BULLET"]
    type = random.choices(values.item_types, weights = values.item_weights, k = 1)[0]
    item_x = random.randint(0, values.WIDTH)
    items.append(Item(item_x, 0, type))

# キー入力処理
def key_input():
    global player, player_bullets
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > 0:
        player.x -= player.speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x < values.WIDTH - player.size:
        player.x += player.speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y > 0:
        player.y -= player.speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y < values.HEIGHT - player.size:
        player.y += player.speed
    if keys[pygame.K_SPACE]:
        player_bullets.extend(player.fire())
    
    if keys[pygame.K_p]:
        player.bullet_level += 1

# プレイヤーとその弾の処理
def player_process():
    global player_bullets
    # プレイヤー弾の移動
    for bullet in player_bullets[:]:
        bullet.move()
        if bullet.y < 0:
            player_bullets.remove(bullet)
            # del bullet

# 敵とその弾の処理
def enemies_process():
    global enemies, enemy_bullets
    # 敵の移動
    for enemy in enemies[:]:
        if enemy.move_pattern == "left":
            enemy.x -= enemy.speed
            if enemy.type == "ZIGZAG":
                enemy.y = enemy.originY + math.sin(enemy.x / enemy.cycle) * enemy.amplitude
        elif enemy.move_pattern == "right":
            enemy.x += enemy.speed
            if enemy.type == "ZIGZAG":
                enemy.y = enemy.originY + math.sin(enemy.x / enemy.cycle) * enemy.amplitude
        elif enemy.move_pattern == "down":
            enemy.y += enemy.speed
            if enemy.type == "ZIGZAG":
                enemy.x = enemy.originX + math.sin(enemy.y / enemy.cycle) * enemy.amplitude
        elif enemy.move_pattern == "up": # ボス用
            enemy.y -= enemy.speed

        # TODO: 敵の発砲処理
        if random.randint(1, 50) == 1:    
            enemy_bullets.append(Bullet(
                values.enemy_values["ENEMY_BULLET_SIZE_" + enemy.true_type], 
                enemy.x + enemy.size // 2, 
                enemy.y + enemy.size, 
                0,
                values.enemy_values["ENEMY_BULLET_SPEED_" + enemy.true_type], 
                values.enemy_values["ENEMY_BULLET_COLOR_" + enemy.true_type],
            ))

        # 画面外の接触処理
        if enemy.true_type == "BOSS" and (random.randint(1, 60) == 1 or enemy.x < 0 or values.WIDTH < enemy.x + enemy.size or enemy.y < 0 or values.HEIGHT < enemy.y + enemy.size):
            if enemy.move_pattern == "left":    enemy.x += enemy.speed
            elif enemy.move_pattern == "right": enemy.x -= enemy.speed
            elif enemy.move_pattern == "down":  enemy.y -= enemy.speed
            elif enemy.move_pattern == "up":    enemy.y += enemy.speed
            directions = ["left", "right", "down", "up"]
            directions.remove(enemy.move_pattern)
            prev_pattern = enemy.move_pattern
            enemy.move_pattern = random.choice(["left", "right", "down", "up"])
            if prev_pattern == "down" and enemy.move_pattern == ("left" or "right"):
                enemy.speed += 1

        elif enemy.x + enemy.size < 0 or values.WIDTH <  enemy.x or enemy.y + enemy.size < 0 or values.HEIGHT < enemy.y: 
            enemies.remove(enemy)
            # del enemy

    # 敵弾の移動
    for bullet in enemy_bullets[:]:
        bullet.move()
        if bullet.y > values.HEIGHT:
            enemy_bullets.remove(bullet)
            # del bullet

# アイテムの処理
def items_process():
    # アイテムの移動
    for item in items[:]:
        item.move()
        if item.y > values.HEIGHT:
            items.remove(item)

# 弾とキャラクターとアイテムの衝突判定・処理
def collision_check():
    global score, player, player_bullets, enemies, enemy_bullets
    screen = GAME
    # 敵弾とプレイヤー
    for bullet in enemy_bullets[:]:
        if (player.x < bullet.x < player.x + player.size and
                player.y < bullet.y < player.y + player.size):
            player.lives -= 1
            enemy_bullets.remove(bullet)
            # del bullet
            if player.lives == 0:
                screen = OVER
            
    # プレイヤー弾と敵
    for bullet in player_bullets[:]:
        for enemy in enemies:
            if (enemy.x < bullet.x < enemy.x + enemy.size and
                    enemy.y < bullet.y < enemy.y + enemy.size):
                if bullet in player_bullets:
                    player_bullets.remove(bullet)
                    # del bullet
                enemy.lives -= 1
                if enemy.lives == 0:
                    if enemy.true_type == "BOSS":
                        screen = CLEAR
                    score += enemy.score
                    enemies.remove(enemy)
                    # del enemy

    # プレイヤーとアイテム
    for item in items[:]:
        if (player.x < item.x < player.x + player.size and
                player.y < item.y < player.y + player.size):
            player = item.enhancement(player)
            items.remove(item)
            # del item

    return screen

# キャラと弾とアイテムの描画
def draw_actors():
    # プレイヤーの描画
    player.draw(window)

    # 敵の描画
    for enemy in enemies:
        enemy.draw(window)

    # 敵弾の描画
    for bullet in enemy_bullets:
        bullet.draw(window)

    # プレイヤー弾の描画
    for bullet in player_bullets:
        bullet.draw(window)
    
    # アイテムの描画
    for item in items:
        item.draw(window)

# UIの描画
def draw_ui():
    # プレイヤーの残基表示
    lives_text = font_small.render(f"Lives: {player.lives}", True, values.WHITE)
    window.blit(lives_text, (10, 10))

    # スコア表示
    score_text = font_small.render(f"Score: {score}", True, values.WHITE)
    window.blit(score_text, (10, 40))

    # フレームレート表示
    fps = int(clock.get_fps())
    fps_text = font_small.render(f"FPS: {fps}", True, values.WHITE)
    window.blit(fps_text, (values.WIDTH - 100, 10))

def score_ui():
    global score, high_scores
    if score != 0:
        save_score()
        load_scores()
    base_y = values.HEIGHT - 220

    high_scores_text = font_middle.render("HIGH SCORE", True, values.YELLOW)
    high_scores_rect = high_scores_text.get_rect(center = (values.WIDTH // 2, base_y))
    window.blit(high_scores_text, high_scores_rect)

    last_score_not_found = True
    for i, point in enumerate(high_scores):
        color = values.WHITE
        message = ""
        if point == last_score and last_score != 0 and last_score_not_found:
            color = values.SALMON
            message = "← last score"
            last_score_not_found = False
        score_text = font_small.render(f"No.{i + 1}: {point} {message}", True, color)
        score_rect = (high_scores_rect.x + 10, base_y + 50 + i * 30)
        window.blit(score_text, score_rect)

# ゲーム全体のループ
def game():
    load_scores()
    screen = HOME
    while True:
        if screen == HOME:      screen = home_loop()
        elif screen == GAME:    screen = play_loop()
        elif screen == CLEAR:   screen = game_clear()
        elif screen == OVER:    screen = game_over()

        # 画面更新
        pygame.display.flip()

        # フレームレート
        clock.tick(30)

# グラデーション背景
def draw_gradient_background(surface, color1, color2):
    width, height = surface.get_size()
    for y in range(height):
        # 画面の上から下まで線形補間で色を変化させる
        blend_ratio = y / height
        r = int(color1[0] * (1 - blend_ratio) + color2[0] * blend_ratio)
        g = int(color1[1] * (1 - blend_ratio) + color2[1] * blend_ratio)
        b = int(color1[2] * (1 - blend_ratio) + color2[2] * blend_ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

# パーティクル
def draw_particles(surface, num_particles=30):
    width, height = surface.get_size()
    for _ in range(num_particles):
        x = random.randint(0, width)
        y = random.randint(0, height)
        pygame.draw.circle(surface, values.WHITE, (x, y), random.randint(1, 3))  # 小さい円で表現

# 画像背景
def image_background(path):
    background_image = pygame.image.load(path)
    window.blit(background_image, (0, 0))

# 流れ星
def animate_stars(surface):
    for star in stars:
        star[1] += 1  # 星を下に移動
        if star[1] > surface.get_height():
            star[1] = 0  # 上に戻る
            star[0] = random.randint(0, surface.get_width())
        pygame.draw.circle(surface, values.WHITE, star, 2)


# ホーム画面
def home_loop():
    global score
    screen = HOME
    draw_gradient_background(window, values.BLACK, values.NAVY)
    animate_stars(window)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キー入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        screen = GAME
        init_game()

    score_ui()

    # メッセージ方法表示
    message_text = font_big.render(f"SHOOTING GAME", True, values.BEIGE)
    message_rect = message_text.get_rect(center = (values.WIDTH // 2, values.HEIGHT // 3))
    window.blit(message_text, message_rect)

    # コンティニュー方法表示
    continue_text = font_small.render(f"Press Enter", True, values.WHITE)
    continue_rect = continue_text.get_rect(center = (values.WIDTH // 2, values.HEIGHT // 2))
    window.blit(continue_text, continue_rect)

    return screen

# ゲーム画面
def play_loop():
    global enemies
    screen = GAME
    draw_gradient_background(window, values.BLACK, values.NAVY)
    animate_stars(window)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    key_input()

    # 敵の生成
    if random.randint(1, 10) == 1 and len(enemies) < values.ENEMY_NUM:
        spawn_enemy()

    # アイテムの生成
    if random.randint(1, 1000) == 1 and len(items) < values.ITEM_NUM:
        spawn_item()

    player_process()
    enemies_process()
    items_process()

    screen = collision_check()

    draw_actors()
    draw_ui()

    return screen

# ゲームクリア画面
def game_clear():
    global score
    screen = CLEAR
    draw_gradient_background(window, values.NAVY, values.SKY_BLUE)
    draw_particles(window)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キー入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        screen = GAME
        init_game()
    elif keys[pygame.K_h]:
        screen = HOME

    score_ui()

    # メッセージ方法表示
    message_text = font_big.render(f"GAME CLEAR", True, values.YELLOW)
    message_rect = message_text.get_rect(center = (values.WIDTH // 2, values.HEIGHT // 3))
    window.blit(message_text, message_rect)

    # コンティニュー方法表示
    continue_text = font_small.render(f"Press Enter", True, values.WHITE)
    continue_rect = continue_text.get_rect(center = (values.WIDTH // 2, values.HEIGHT // 2))
    window.blit(continue_text, continue_rect)

    return screen

# ゲームオーバー画面
def game_over():
    global score, high_scores
    screen = OVER
    draw_gradient_background(window, values.BLACK, values.NAVY)

    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キー入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        screen = GAME
        init_game()
    elif keys[pygame.K_h]:
        screen = HOME

    score_ui()

    # メッセージ方法表示
    message_text = font_big.render(f"GAME OVER", True, values.GRAY)
    message_rect = message_text.get_rect(center = (values.WIDTH // 2, values.HEIGHT // 3))
    window.blit(message_text, message_rect)

    # コンティニュー方法表示
    continue_text = font_small.render(f"Press Enter", True, values.WHITE)
    continue_rect = continue_text.get_rect(center = (values.WIDTH // 2, values.HEIGHT // 2))
    window.blit(continue_text, continue_rect)

    return screen
