import pygame
import sys
import random
import math

# 初期化
pygame.init()

# 画面の設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("オオカミ vs 羊ゲーム")

# 色の設定
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (169, 169, 169)

# 画像の読み込み
title_image = pygame.image.load("title.png")  # タイトル画像
title_image = pygame.transform.scale(title_image, (screen_width, screen_height))  # 画面サイズに合わせる
background_image = pygame.image.load("background.jpg")  # 背景画像
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # 画面サイズに合わせる
wolf_image = pygame.image.load("wolf.png")  # オオカミの画像
sheep_image = pygame.image.load("sheep.png")  # 羊の画像
farmer_image = pygame.image.load("farmer.png")  # 農夫の画像

# BGMの設定
pygame.mixer.music.load("title_bgm.mp3")  # タイトル画面用のBGMファイル
pygame.mixer.music.play(-1)  # ループ再生

# 効果音の読み込み
wolf_sound = pygame.mixer.Sound("wolf_bite.mp3")  # オオカミの効果音
rifle_sound = pygame.mixer.Sound("rifle_shot.mp3")  # ライフルの効果音

# 農夫の発言効果音
farmer_speak_sounds = [
    pygame.mixer.Sound("farmer_speak1.wav"),
    pygame.mixer.Sound("farmer_speak2.wav"),
    pygame.mixer.Sound("farmer_speak3.wav"),
    pygame.mixer.Sound("farmer_speak4.wav")
]

# タイトル画面の設定
title_font = pygame.font.SysFont(None, 100)
start_font = pygame.font.SysFont(None, 60)
title_text = title_font.render("オオカミ vs 羊", True, black)
title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))
start_text = start_font.render("Press any key to start", True, black)
start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 1.5))

# ゲームオーバー画面の設定
game_over_font = pygame.font.SysFont(None, 100)
retry_font = pygame.font.SysFont(None, 60)
game_over_text = game_over_font.render("Game Over", True, black)
retry_text = retry_font.render("Press 'R' to retry", True, black)
end_text = retry_font.render("Press 'Q' to quit", True, black)
game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 3))
retry_rect = retry_text.get_rect(center=(screen_width // 2, screen_height // 2))
end_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 1.5))

# オオカミの設定
wolf_width = 100
wolf_height = 100
wolf_image = pygame.transform.scale(wolf_image, (wolf_width, wolf_height))  # 画像サイズに合わせる
wolf_x = screen_width // 6 - wolf_width // 6
wolf_y = screen_height - wolf_height - 8
wolf_speed = 8

# 農夫の設定
farmer_width = 90
farmer_height = 90
farmer_image = pygame.transform.scale(farmer_image, (farmer_width, farmer_height))  # 画像サイズに合わせる
farmer_x = (screen_width - farmer_width) // 2  # 画面中央に設定
farmer_y = screen_height - farmer_height
farmer_speed_x = 3
farmer_move_direction = 1
farmer_shoot_frequency = 80
farmer_shoot_timer = 0
farmer_spawn_timer = pygame.time.get_ticks()
farmer_active_time = 10000
farmer_active_timer = 0

print(farmer_x,farmer_y)
# ライフルの設定
rifle_radius = 10  # 弾の大きさ

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10

    def move(self):
        self.y -= self.speed


# 羊の設定
sheep_width = 70
sheep_height = 70
sheep_image = pygame.transform.scale(sheep_image, (sheep_width, sheep_height))  # 画像サイズに合わせる
sheep_speed = 7
sheep_frequency = 25
sheep_list = []
sheep_sounds = [pygame.mixer.Sound("sheep1.mp3"), pygame.mixer.Sound("sheep2.mp3"), pygame.mixer.Sound("sheep3.mp3"), pygame.mixer.Sound("sheep4.mp3")]

# スコアの初期化
score = 0

# タイマーの設定
game_start_time = pygame.time.get_ticks()
game_duration = 60000

# 農夫がしゃべる効果音の設定
farmer_speak_sounds = [
    pygame.mixer.Sound("farmer_speak2.wav"),
    pygame.mixer.Sound("farmer_speak3.wav"),
    pygame.mixer.Sound("farmer_speak3.wav")
]

farmer_speak_sounds2 = [
    pygame.mixer.Sound("farmer_speak1.wav")
]

# 農夫の発射する弾の効果音の設定
rifle_sound = pygame.mixer.Sound("rifle_shot.mp3")

# 関数: テキスト描画
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# 関数: 2点間の距離を計算
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# 関数: 農夫の発言
def farmer_speak():
    sound = random.choice(farmer_speak_sounds)
    sound.play()

# 関数: 農夫が発射する弾
def farmer_shoot():
    rifle_sound.play()
    bullets.append(Bullet(farmer_x + farmer_width // 2, farmer_y + farmer_height))

# ゲームループ
title_screen = True
game_over = False
clock = pygame.time.Clock()
bullets = []
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if title_screen:
                title_screen = False
                game_over = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("ingame_bgm.mp3")
                pygame.mixer.music.play(-1)
                game_start_time = pygame.time.get_ticks()
                sheep_list = []
                score = 0
                wolf_x = screen_width // 2 - wolf_width // 2
                wolf_y = screen_height - wolf_height - 10
                farmer_x = screen_width // 2 - farmer_width // 2  # 画面中央に設定
                farmer_y = screen_height // 2 - farmer_height // 2  # 画面中央に設定
                farmer_spawn_timer = pygame.time.get_ticks()
                farmer_active_timer = 0
                farmer_speed_x = 3
                farmer_move_direction = 1
                farmer_shoot_frequency = 50
                farmer_shoot_timer = 15
            elif game_over:
                if event.key == pygame.K_r:
                    game_over = False
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("title_bgm.mp3")
                    pygame.mixer.music.play(-1)
                    title_screen = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    keys = pygame.key.get_pressed()
    if not title_screen:
        if keys[pygame.K_LEFT] and wolf_x > 0:
            wolf_x -= wolf_speed
        if keys[pygame.K_RIGHT] and wolf_x < screen_width - wolf_width:
            wolf_x += wolf_speed

        elapsed_time = pygame.time.get_ticks() - game_start_time
        remaining_time = max(0, game_duration - elapsed_time)

        # スコアが100を超え、農夫がまだ登場していない場合
        if score > 100 and not farmer_active_timer:
            farmer_active_timer = pygame.time.get_ticks()  # 農夫の活動時間のタイマーを設定
            farmer_x = random.choice([0, screen_width - farmer_width])  # 左右どちらから登場するかランダムに選択
            farmer_speak()  # 農夫の発言
            farmer_speed_x = 3 * random.choice([1, -1])  # 左右どちらに移動するかランダムに選択
            farmer_move_direction = farmer_speed_x / abs(farmer_speed_x)  # 移動方向を設定

        # 農夫の動きと球の発射
        if farmer_active_timer and pygame.time.get_ticks() - farmer_active_timer < farmer_active_time:
            farmer_x += farmer_speed_x * farmer_move_direction

            if farmer_x < 0:
                farmer_x = 0
                farmer_move_direction = 1
            elif farmer_x > screen_width - farmer_width:
                farmer_x = screen_width - farmer_width
                farmer_move_direction = -1

            farmer_shoot_timer += 1
            if farmer_shoot_timer >= farmer_shoot_frequency:
                # 弾を発射
                farmer_shoot()
                if not game_over:
                    # 農夫の発言
                    random.choice(farmer_speak_sounds).play()
                farmer_shoot_timer = 0
        else:
            farmer_active_timer = 0  # 農夫の活動時間が終わったらタイマーをリセット
            farmer_x = random.choice([0, screen_width - farmer_width])
            farmer_y = -farmer_height - 50

        for bullet in bullets:
            # 弾の移動ベクトルを計算し、オオカミの位置に向かって移動
            angle = math.atan2(wolf_y - bullet.y, wolf_x - bullet.x)
            bullet.x += bullet.speed * math.cos(angle)
            bullet.y += bullet.speed * math.sin(angle)

        bullets = [bullet for bullet in bullets if bullet.y > 0]

        for bullet in bullets:
            if (
                wolf_x < bullet.x < wolf_x + wolf_width
                and wolf_y < bullet.y < wolf_y + wolf_height
            ):
                game_over = True

        if remaining_time <= 0:
            game_over = True

        # オオカミが羊を食べる
        for sheep in sheep_list:
            if (
                wolf_x < sheep[0] < wolf_x + wolf_width
                and wolf_y < sheep[1] < wolf_y + wolf_height
            ):
                sheep_list.remove(sheep)
                score += 10
                wolf_sound.play()

        if random.randrange(0, sheep_frequency) == 0:
            sheep_x = random.randrange(0, screen_width - sheep_width)
            sheep_y = -sheep_height
            sheep_list.append([sheep_x, sheep_y])
            random.choice(sheep_sounds).play()  # 羊が登場したときに鳴く

        for sheep in sheep_list:
            # ジグザグな動き
            sheep[0] += random.choice([-5, 5])
            sheep[1] += sheep_speed

        sheep_list = [sheep for sheep in sheep_list if sheep[1] < screen_height]

    screen.blit(background_image, (0, 0))

    if title_screen:
        screen.blit(title_image, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(start_text, start_rect)
    elif game_over:
        screen.blit(game_over_text, game_over_rect)
        screen.blit(retry_text, retry_rect)
        screen.blit(end_text, end_rect)
    else:
        screen.blit(wolf_image, (wolf_x, wolf_y))
        screen.blit(farmer_image, (farmer_x, farmer_y))

        for bullet in bullets:
            pygame.draw.circle(screen, red, (int(bullet.x), int(bullet.y)), rifle_radius)

        for sheep in sheep_list:
            screen.blit(sheep_image, (sheep[0], sheep[1]))

        draw_text("Time: " + str(remaining_time // 1000), pygame.font.SysFont(None, 30), black, 10, 10)
        draw_text("Score: " + str(score), pygame.font.SysFont(None, 30), black, 10, 50)

    pygame.display.update()
    clock.tick(30)