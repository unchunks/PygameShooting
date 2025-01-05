import pygame
import random
import sys
import math
import json
from character import *
from player import *
from enemy import *
from item import *
from bullet import *

# 初期化
pygame.init()

# ウィンドウの作成
window = pygame.display.set_mode((values.INIT_WIDTH, values.INIT_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("VIA LACTEA")

# フォント設定
font_big = pygame.font.SysFont("hackgen", 100)
font_middle = pygame.font.SysFont("hackgen", 48)
font_small = pygame.font.SysFont("hackgen", 36)

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
GAME = 0
HOME = 1
CLEAR = 2
OVER = 3

# キャラクターの初期化
player = Player(values.INIT_WIDTH, values.INIT_HEIGHT)
player_bullets = []

enemy_num = values.ENEMY_NUM
enemies = []
enemy_bullets = []

item_num = values.ITEM_NUM
items = []
boss_mode = False

# ゲーム全体のループ
def main_loop():
    # 起動時のハイスコア読み込み
    load_scores()

    resize_font()
    resize_stars()
    resize_max_num()

    # 初期画面
    screen = HOME

    while True:
        input_mouse()
        if   screen == GAME:    screen = game()
        elif screen == HOME:    screen = menu_home()
        elif screen == CLEAR:   screen = menu_clear()
        elif screen == OVER:    screen = menu_over()

        # 画面更新
        pygame.display.flip()

        # フレームレート調整
        clock.tick(30)


# ゲーム画面
def game() -> int:
    input_key_game()

    spawn_enemy()
    spawn_item()

    process_player()
    process_enemies()
    process_items()

    next_screen = check_collision()

    draw_gradient_background(values.BLACK, values.NAVY)
    draw_animate_stars()
    draw_characters()
    draw_game_ui()

    return next_screen

# ホーム画面
def menu_home() -> int:
    next_screen = input_key_menu(HOME)

    draw_gradient_background(values.BLACK, values.NAVY)
    draw_animate_stars()
    draw_message_menu("VIA LACTEA", values.BEIGE)

    return next_screen

# ゲームクリア画面
def menu_clear() -> int:
    next_screen = input_key_menu(CLEAR)

    draw_gradient_background(values.NAVY, values.SKY_BLUE)
    draw_particles()
    draw_message_menu("GAME CLEAR", values.YELLOW)

    return next_screen

# ゲームオーバー画面
def menu_over() -> int:
    next_screen = input_key_menu(OVER)

    draw_gradient_background(values.BLACK, values.NAVY)
    draw_message_menu("GAME OVER", values.GRAY)

    return next_screen


# 整数を画面サイズに合わせる
def resize_int(value: int) -> int:
    global window
    win_width, win_height = window.get_size()
    win_average = win_height
    init_average = values.INIT_HEIGHT
    return int(win_average * value / init_average)

# フォントサイズを画面サイズに合わせる
def resize_font():
    global font_big, font_middle, font_small
    font_big = pygame.font.SysFont("hackgen", resize_int(100))
    font_middle = pygame.font.SysFont("hackgen", resize_int(48))
    font_small = pygame.font.SysFont("hackgen", resize_int(36))

# 背景の星の数を画面サイズに合わせる
def resize_stars():
    global stars
    stars = [[random.randint(0, window.get_width()), random.randint(0, window.get_height())] for _ in range(resize_int(50))]

# 敵とアイテムの最大数を画面サイズに合わせる
def resize_max_num():
    global enemy_num, item_num
    enemy_num = resize_int(values.ENEMY_NUM)
    item_num = resize_int(values.ITEM_NUM)

# ゲーム内で使用する変数の初期化
def init_game():
    global score, last_score, player, player_bullets, enemies, enemy_bullets, items
    # スコア
    score = 0
    last_score = 0

    # キャラクターの初期化
    win_width, win_height = window.get_size()
    player = Player(win_width, win_height)
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
def spawn_enemy(): # ["STOP", "STRAIGHT", "ZIGZAG", "FAST", "BOSS"]
    global boss_mode, enemies, window, enemy_num
    if random.randint(1, 10) == 1 and len(enemies) < enemy_num:
        type = random.choices(values.enemy_types, weights = values.enemy_weights, k = 1)[0]
        if boss_mode:
            type = "BOSS"   
        direction = random.choice([values.LEFT, values.RIGHT, values.DOWN])
        win_width, win_height = window.get_size()
        enemy_x = random.randint(0, win_width - values.enemy_values['ENEMY_SIZE_' + type])
        enemy_y = random.randint(0, win_height // 2)
        amplitude = random.randint(20, 50)
        cycle = random.randint(20, 30)
        if type != "STOP":
            if direction == values.LEFT:
                enemy_x = win_width - values.enemy_values['ENEMY_SIZE_' + type]
            elif direction == values.RIGHT:
                enemy_x = 0
            elif direction == values.DOWN:
                enemy_y = 0
        enemies.append(Enemy(enemy_x, enemy_y, direction, type, amplitude, cycle))

# アイテムの生成
def spawn_item(): # ["HEAL", "SPEED", "BULLET"]
    global items, window, item_num
    if random.randint(1, 500) == 1 and len(items) < item_num:
        type = random.choices(values.item_types, weights = values.item_weights, k = 1)[0]
        win_width, win_height = window.get_size()
        item_x = random.randint(0, win_width)
        items.append(Item(item_x, 0, type))


# マウス入力処理
def input_mouse():
    global window
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ウィンドウサイズ変更イベントの処理
        if event.type == pygame.VIDEORESIZE:
            win_width, win_height = event.w, event.h  # 新しい幅と高さを取得
            window = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)  # 新しいサイズでウィンドウを再設定
            resize_font()
            resize_stars()
            resize_max_num()

            # ウィンドウリサイズでプレイヤーが画面外に出ないように
            if player.x > win_width:
                player.x = win_width - player.size / 2
            if player.y > win_height:
                player.y = win_height - player.size / 2

# ゲーム画面のキー入力処理
def input_key_game():
    global player, player_bullets, window
    win_width, win_height = window.get_size()
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > 0:
        player.move(values.LEFT)
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x < win_width - player.size:
        player.move(values.RIGHT)
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y > resize_int(150):
        player.move(values.UP)
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y < win_height - player.size:
        player.move(values.DOWN)
    if keys[pygame.K_SPACE]:
        player_bullets.extend(player.fire())
    
    # if keys[pygame.K_p]:
    #     player.bullet_level += 1

# メニュー画面のキー入力処理
def input_key_menu(now_screen: int) -> int:
    global boss_mode
    next_screen = now_screen
    # キー入力処理
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        boss_mode = False
        next_screen = GAME
        init_game()
    elif keys[pygame.K_b]:
        boss_mode = True
        next_screen = GAME
        init_game()
    elif keys[pygame.K_h]:
        next_screen = HOME
    return next_screen


# プレイヤーとその弾の処理
def process_player():
    global player_bullets

    # プレイヤー弾の移動
    for bullet in player_bullets[:]:
        bullet.move()
        if bullet.y < 0:
            player_bullets.remove(bullet)
            # del bullet

# 敵とその弾の処理
def process_enemies():
    global enemies, enemy_bullets, window
    win_width, win_height = window.get_size()
    # 敵の移動
    for enemy in enemies[:]:
        fire_rand = random.randint(1, 50)

        enemy.move()
        if enemy.type == "ZIGZAG":
            if enemy.move_direction[0] == 0:
                enemy.x = enemy.originX + enemy.move_direction[1] * math.sin(enemy.y / enemy.cycle) * enemy.amplitude
            if enemy.move_direction[1] == 0:
                enemy.y = enemy.originY + enemy.move_direction[0] * math.sin(enemy.x / enemy.cycle) * enemy.amplitude

        # 画面外の接触処理
        if enemy.true_type == "BOSS" and (random.randint(1, 100) == 1 or enemy.x < 0 or win_width < enemy.x + enemy.size or enemy.y < 0 or win_height * 0.9 < enemy.y + enemy.size):
            # 画面枠に引っかからないように
            # enemy.move(enemy.move_direction, True)
            Character.move(enemy, enemy.move_direction, True)

            # 万が一外に出たときは内部にテレポート
            cushion_padding = 5
            if enemy.x < -cushion_padding or win_width + cushion_padding < enemy.x + enemy.size or enemy.y < -cushion_padding or win_height * 0.9 + cushion_padding < enemy.y + enemy.size:
                enemy.x = random.randint(10, win_width - 10)
                enemy.y = random.randint(10, int(win_height * 0.9 - 10))

            # 今とは別方向に移動
            directions = [values.LEFT, values.RIGHT, values.UP, values.DOWN]
            directions.remove(enemy.move_direction)
            prev_pattern = enemy.move_direction
            enemy.move_direction = random.choice(directions)

            # 他の敵の動きを模倣
            types = values.enemy_types.copy()
            types.remove(enemy.type)
            prev_type = enemy.type
            enemy.type = random.choice(types)
            enemy.originX = enemy.x
            enemy.originY = enemy.y
            # 特定の動きをしたら速度上昇
            if (prev_pattern == values.DOWN and enemy.move_direction == (values.LEFT or values.RIGHT)) \
            or (prev_type != "BOSS" and enemy.type == "BOSS"):
                enemy.speed = min(enemy.speed + 1, values.enemy_values["ENEMY_SPEED_BOSS"] * 3)
            # 弾を発射する確率を3倍に
            fire_rand //= 3
        elif enemy.x + enemy.size < 0 or win_width <  enemy.x or enemy.y + enemy.size < 0 or win_height < enemy.y: 
            enemies.remove(enemy)
            # del enemy

        # 敵の発砲処理
        if fire_rand <= 1:
            enemy_bullets.extend(enemy.fire())

    # 敵弾の移動
    for bullet in enemy_bullets[:]:
        bullet.move()
        if bullet.y > win_height:
            enemy_bullets.remove(bullet)
            # del bullet

# アイテムの処理
def process_items():
    global window
    win_width, win_height = window.get_size()
    # アイテムの移動
    for item in items[:]:
        item.move()
        if item.y > win_height:
            items.remove(item)

# 弾とキャラクターとアイテムの衝突判定・処理
def check_collision() -> int:
    global score, player, player_bullets, enemies, enemy_bullets, boss_mode
    next_screen = GAME
    # 敵弾とプレイヤー
    for bullet in enemy_bullets[:]:
        if (player.x < bullet.x < player.x + player.size and
                player.y < bullet.y < player.y + player.size):
            player.lives -= 1
            enemy_bullets.remove(bullet)
            # del bullet
            if player.lives == 0:
                next_screen = OVER
            
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
                    if enemy.true_type == "BOSS" and boss_mode == False:
                        next_screen = CLEAR
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

    return next_screen


# グラデーション背景
def draw_gradient_background(top_color: tuple[int, int, int], bottom_color: tuple[int, int, int]):
    global window
    win_width, win_height = window.get_size()
    for y in range(win_height):
        # 画面の上から下まで線形補間で色を変化させる
        blend_ratio = y / win_height
        r = int(top_color[0] * (1 - blend_ratio) + bottom_color[0] * blend_ratio)
        g = int(top_color[1] * (1 - blend_ratio) + bottom_color[1] * blend_ratio)
        b = int(top_color[2] * (1 - blend_ratio) + bottom_color[2] * blend_ratio)
        pygame.draw.line(window, (r, g, b), (0, y), (win_width, y))

# パーティクル
def draw_particles(num_particles: int = 30):
    global window
    win_width, win_height = window.get_size()
    for _ in range(num_particles):
        x = random.randint(0, win_width)
        y = random.randint(0, win_height)
        pygame.draw.circle(window, values.WHITE, (x, y), random.randint(1, 3))  # 小さい円で表現

# 流れ星
def draw_animate_stars():
    global window
    for star in stars:
        star[1] += 1  # 星を下に移動
        if star[1] > window.get_height():
            star[1] = 0  # 上に戻る
            star[0] = random.randint(0, window.get_width())
        pygame.draw.circle(window, values.WHITE, star, 2)

# ハイスコアランキングの描画
def draw_high_score():
    global score, high_scores, window
    win_width, win_height = window.get_size()
    if score != 0:
        save_score()
        load_scores()
    base_y = win_height - resize_int(300)

    high_scores_text = font_middle.render("HIGH SCORE", True, values.YELLOW)
    high_scores_rect = high_scores_text.get_rect(center = (win_width // 2, base_y))
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
        score_rect = (high_scores_rect.x + 10, base_y + resize_int(50) + i * resize_int(40))
        window.blit(score_text, score_rect)

# メニュー画面のテキスト表示
def draw_message_menu(text: str, color: tuple):
    global window
    win_width, win_height = window.get_size()
    # メッセージ方法表示
    message_text = font_big.render(text, True, color)
    message_rect = message_text.get_rect(center = (win_width // 2, win_height // 3))
    window.blit(message_text, message_rect)

    # コンティニュー方法表示
    continue_text = font_small.render(f"Press Enter", True, values.WHITE)
    continue_rect = continue_text.get_rect(center = (win_width // 2, win_height // 2))
    window.blit(continue_text, continue_rect)

    # ボスモードの選択方法表示
    continue_text = font_small.render(f"BOSS Mode: Press B", True, values.WHITE)
    continue_rect = continue_text.get_rect(center = (win_width // 2, win_height // 2 + resize_int(50)))
    window.blit(continue_text, continue_rect)

    draw_high_score()

# キャラと弾とアイテムの描画
def draw_characters():
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

# ゲーム中のUI描画
def draw_game_ui():
    # プレイヤーの残基表示
    lives_text = font_small.render(f"Lives: {player.lives}", True, values.LAVENDER)
    window.blit(lives_text, (resize_int(10), resize_int(10)))

    # スコア表示
    score_text = font_small.render(f"Score: {score}", True, values.LAVENDER)
    window.blit(score_text, (resize_int(10), resize_int(40)))

    # フレームレート表示
    # win_width, win_height = window.get_size()
    # fps = int(clock.get_fps())
    # fps_text = font_small.render(f"FPS: {fps}", True, values.WHITE)
    # window.blit(fps_text, (win_width - 100, 10))
