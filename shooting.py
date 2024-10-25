import tkinter as tk
import random
from actor import *
from player import *
from enemy import *
from bullet import *

# ウィンドウの作成
window = tk.Tk()
window.title("2Dシューティングゲーム")
window.resizable(False, False)

# キャンバスを作成
canvas = tk.Canvas(window, width=values.WIDTH, height=values.HEIGHT, bg="black")
canvas.pack()

# ゲームの初期設定
player = Player(canvas)
bullets = []
enemies = []
enemy_bullets = []
keys_pressed = {}
last_update_time_ms = time.time() * 1000
current_fps = 0


def key_press(event):
    keys_pressed[event.keysym] = True

def key_release(event):
    if event.keysym in keys_pressed:
        del keys_pressed[event.keysym]

def setup_events():
    # キーが押されたときと離されたときのイベントバインド
    window.bind("<KeyPress>", key_press)
    window.bind("<KeyRelease>", key_release)

def input():
    # プレイヤーの動きをキーの状態に基づいて更新する
    if keys_pressed.get("w"):
        player.move("up")
    if keys_pressed.get("s"):
        player.move("down")
    if keys_pressed.get("a"):
        player.move("left")
    if keys_pressed.get("d"):
        player.move("right")
    if keys_pressed.get("space"):
        player.fire(bullets)
    if keys_pressed.get("q"):
        window.quit()

# ゲームオーバー画面の処理
def game_over():
    canvas.delete("all")
    game_over_text = canvas.create_text(values.WIDTH / 2, values.HEIGHT / 2, text="GAME OVER", fill="red", font=("Arial", 48))
    restart_button = tk.Button(window, text="Restart", command=start_game)
    canvas.create_window(values.WIDTH / 2, values.HEIGHT / 2 + 50, window=restart_button)

# ゲームを初期化して開始する
def start_game():
    global player, bullets, enemies, enemy_bullets, keys_pressed, lives_text, fps_text, last_update_time
    lives_text = None
    canvas.delete("all")
    player = Player(canvas)
    lives_text = canvas.create_text(10, 10, anchor='nw', text=f"Lives: {player.lives}", fill="white", font=("Arial", 16))
    bullets = []
    enemies = []
    enemy_bullets = []
    keys_pressed = {}
#REVIEW: デバッグ用
    fps_text = canvas.create_text(10, 30, anchor='nw', text=f"FPS: {0}", fill="white", font=("Arial", 16))
    
    # イベントのバインディング
    window.bind("<KeyPress>", key_press)
    window.bind("<KeyRelease>", key_release)
    
    game_loop()
    window.mainloop()

def game_loop():
    if player.lives <= 0:
        game_over()
        return    
    input()

    # プレイヤーの弾の処理
    for bullet in bullets[:]:
        if not bullet.move(-1):
            bullets.remove(bullet)
        for enemy in enemies[:]:
            if bullet.hit_test(enemy):
                enemy.lives -= 1
                if enemy.lives <= 0:
                    canvas.delete(enemy.shape)
                    canvas.delete(bullet.shape)
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    break

    # 敵の生成と移動
    if len(enemies) < values.ENEMY_NUM:  # 敵がランダムに出現
        enemies.append(Enemy(canvas))

    for enemy in enemies[:]:
        if not enemy.move():
            enemies.remove(enemy)
        else:
            enemy.fire(enemy_bullets)  # 敵が弾を発射

    # 敵の弾の処理
    for enemy_bullet in enemy_bullets[:]:
        if not enemy_bullet.move(1):
            enemy_bullets.remove(enemy_bullet)
        elif enemy_bullet.hit_test(player):
            player.lives -= 1
            canvas.itemconfig(lives_text, text=f"Lives: {player.lives}")
            if player.lives <= 0:
                canvas.delete(player.shape)
                game_over()
                return
            canvas.delete(enemy_bullet.shape)
            enemy_bullets.remove(enemy_bullet)
            break

    # FPSの計算
    global last_update_time_ms, current_fps
    current_time_ms = time.time() * 1000
    delta_time_ms = current_time_ms - last_update_time_ms
    last_update_time_ms = current_time_ms
    
    if 5 < delta_time_ms:
        current_fps = 1000 / delta_time_ms
        canvas.itemconfig(fps_text, text=f"FPS: {int(current_fps)}")

    # 次のフレームを待機
    delay = max(0, values.FRAME_TIME - delta_time_ms)
    print(f"FPS: {int(current_fps)},\tdelta time: {delta_time_ms},\tdelay: {delay}")
    if player.lives > 0:
        window.after(int(delay), game_loop)
