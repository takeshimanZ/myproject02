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
pygame.display.set_caption("Wolf vs Sheep")

# 色の設定
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (169,169,169)

# 画像の読み込み
img_folder = "img/"
title_image = pygame.image.load(img_folder + "title.png")
title_image = pygame.transform.scale(title_image, (screen_width, screen_height))
title_background_image = pygame.image.load(img_folder + "title_background.jpg")
title_background_image = pygame.transform.scale(title_background_image, (screen_width, screen_height))
background_image = pygame.image.load(img_folder +"background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))


wolf_image = pygame.image.load(img_folder + "wolf.png")
sheep_image = pygame.image.load(img_folder + "sheep.png")

# BGMの設定 
bgm_folder ="bgm/"
pygame.mixer.music.load(bgm_folder + "title_bgm.mp3")
pygame.mixer.music.play(-1)

# 効果音の読み込み
wolf_sound = pygame.mixer.Sound(bgm_folder +"wolf_bite.mp3")
rifle_sound = pygame.mixer.Sound(bgm_folder + "rifle_shot.mp3")
sheep_sounds = [pygame.mixer.Sound(bgm_folder + "sheep1.mp3"), pygame.mixer.Sound(bgm_folder + "sheep2.mp3"), pygame.mixer.Sound(bgm_folder + "sheep3.mp3"), pygame.mixer.Sound(bgm_folder + "sheep4.mp3")]

# タイトル画面の設定
title_font = pygame.font.SysFont(None, 100)
start_font = pygame.font.SysFont(None, 60)
title_text = title_font.render("Wolf vs Sheep", True, gray)
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
wolf_image = pygame.transform.scale(wolf_image, (wolf_width, wolf_height))
wolf_x = screen_width // 6 - wolf_width // 6
wolf_y = screen_height - wolf_height - 8
wolf_speed = 8

# 羊の設定
sheep_width = 70
sheep_height = 70
sheep_image = pygame.transform.scale(sheep_image, (sheep_width, sheep_height))
sheep_speed = 7
sheep_frequency = 25
sheep_list = []

# スコアの初期化
score = 0

# タイマーの設定
game_start_time = pygame.time.get_ticks()
game_duration = 30000

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

title_screen = True
game_over = False
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if title_screen or game_over:
                title_screen = False
                game_over = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load(bgm_folder + "ingame_bgm.mp3")
                pygame.mixer.music.play(-1)
                game_start_time = pygame.time.get_ticks()
                sheep_list = []
                score = 0
                wolf_x = screen_width // 2 - wolf_width // 2
                wolf_y = screen_height - wolf_height - 10

    keys = pygame.key.get_pressed()
    if not title_screen and not game_over:
        if keys[pygame.K_LEFT] and wolf_x > 0:
            wolf_x -= wolf_speed
        if keys[pygame.K_RIGHT] and wolf_x < screen_width - wolf_width:
            wolf_x += wolf_speed

        elapsed_time = pygame.time.get_ticks() - game_start_time
        remaining_time = max(0, game_duration - elapsed_time)

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
            random.choice(sheep_sounds).play()

        for sheep in sheep_list:
            sheep[0] += random.choice([-5, 5])
            sheep[1] += sheep_speed

        sheep_list = [sheep for sheep in sheep_list if sheep[1] < screen_height]

        if remaining_time <= 0:
            game_over = True

    screen.blit(background_image, (0, 0))  # 背景画像を表示

    if title_screen:
        # title_imagesサイズ
        scaled_title_image = pygame.transform.scale(title_image, (400, 300))
        title_rect = scaled_title_image.get_rect(center=(screen_width // 2, screen_height // 4))

        screen.blit(title_background_image, (0, 0))
        screen.blit(scaled_title_image, title_rect)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 1.8))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 1.5))
    elif game_over:
        screen.blit(game_over_text, game_over_rect)
        screen.blit(retry_text, retry_rect)
        screen.blit(end_text, end_rect)
    else:
        screen.blit(wolf_image, (wolf_x, wolf_y))

        for sheep in sheep_list:
            screen.blit(sheep_image, (sheep[0], sheep[1]))

        draw_text("Time: " + str(remaining_time // 1000), pygame.font.SysFont(None, 30), black, 10, 10)
        draw_text("Score: " + str(score), pygame.font.SysFont(None, 30), black, 10, 50)

    pygame.display.update()
    clock.tick(30)