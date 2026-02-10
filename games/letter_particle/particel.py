import random
import sys

import math
import pygame
from pygame.locals import *

# 初始化pygame
pygame.init()
pygame.mixer.init()
# 加载音效
SOUND_A = pygame.mixer.Sound("sounds/A.MP3")

# 设置屏幕大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("键盘字母游戏")

# 定义颜色
BACKGROUND_COLOR = (10, 10, 30)
STAR_COLORS = [
    (255, 255, 255),
    (200, 200, 255),
    (150, 200, 255),
]
LETTER_COLORS = [
    (255, 105, 97),  # 红色
    (76, 209, 137),  # 绿色
    (64, 156, 255),  # 蓝色
    (178, 102, 255),  # 紫色
    (255, 221, 89),  # 黄色
    (255, 149, 81),  # 橙色
]
TEXT_COLOR = (255, 255, 255)
UI_BG_COLOR = (30, 30, 50, 200)
UI_BORDER_COLOR = (100, 200, 255)
HIGHLIGHT_COLOR = (255, 255, 255, 100)

# 游戏参数
FALL_SPEED = 1
LETTER_SIZE = 40
SPAWN_RATE = 30  # 每多少帧生成一个新字母
MAX_LETTERS = 10  # 屏幕上最大字母数


class Particle:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.uniform(0.5, 2)
        self.speed = random.uniform(0.1, 0.5)
        self.color = random.choice(STAR_COLORS)
        self.alpha = random.randint(100, 255)

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)

    def draw(self, surface):
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, self.alpha), (self.size, self.size), self.size)
        surface.blit(s, (self.x, self.y))


class FallingLetter:
    def __init__(self):
        self.letter = chr(random.randint(65, 68))  # A-Z
        # self.letter = chr(random.randint(65, 90))  # A-Z
        self.x = random.randint(LETTER_SIZE, SCREEN_WIDTH - LETTER_SIZE)
        self.y = -LETTER_SIZE
        self.speed = random.uniform(FALL_SPEED, FALL_SPEED + 0.1)
        self.color = random.choice(LETTER_COLORS)
        self.size = LETTER_SIZE
        self.active = True
        self.rotation = 0
        self.glow_radius = 0
        self.glow_direction = 1
        # 播放音效
        SOUND_A.play()

    def update(self):
        if self.active:
            self.y += self.speed
            self.rotation = (self.rotation + 1) % 360
            # 更新发光效果
            self.glow_radius += 0.3 * self.glow_direction
            if self.glow_radius > 5:
                self.glow_direction = -1
            elif self.glow_radius < 0:
                self.glow_direction = 1

    def draw(self, surface):
        if self.active:
            # 绘制发光效果
            glow_surf = pygame.Surface((self.size + 20, self.size + 20), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (*self.color, 50),
                               (self.size // 2 + 10, self.size // 2 + 10),
                               self.size // 2 + 10 + int(self.glow_radius))
            surface.blit(glow_surf, (int(self.x - self.size // 2 - 10), int(self.y - self.size // 2 - 10)))

            # 绘制字母背景圆角矩形
            rect_size = self.size + 10
            rect = pygame.Rect(int(self.x - rect_size // 2), int(self.y - rect_size // 2), rect_size, rect_size)
            pygame.draw.rect(surface, self.color, rect, border_radius=10)
            pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=10)

            # 创建字体对象
            font = pygame.font.SysFont('Arial', self.size - 10, bold=True)
            text_surface = font.render(self.letter, True, TEXT_COLOR)
            text_rect = text_surface.get_rect(center=(self.x, self.y))
            surface.blit(text_surface, text_rect)

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.size


class Game:
    def __init__(self):
        self.falling_letters = []
        self.score = 0
        self.lives = 3
        self.max_lives = 3
        self.spawn_counter = 0
        self.game_over = False
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 24)
        self.particles = [Particle() for _ in range(50)]
        self.background_stars = [(random.randint(0, SCREEN_WIDTH),
                                  random.randint(0, SCREEN_HEIGHT),
                                  random.uniform(0.5, 2)) for _ in range(100)]

    def spawn_letter(self):
        if len(self.falling_letters) < MAX_LETTERS and self.spawn_counter >= SPAWN_RATE:
            self.falling_letters.append(FallingLetter())
            self.spawn_counter = 0
        else:
            self.spawn_counter += 1

    def handle_input(self, key):
        if self.game_over:
            return

        # 将按键转换为大写字母
        letter = key.upper()

        # 查找匹配的字母并移除
        for falling_letter in self.falling_letters:
            if falling_letter.letter == letter and falling_letter.active:
                falling_letter.active = False
                self.score += 10
                return

        # 如果没有匹配，扣生命值
        if not any(f.lower() == letter.lower() for f in [l.letter for l in self.falling_letters if l.active]):
            # 检查是否有其他未被击中的字母到达底部
            for falling_letter in self.falling_letters:
                if falling_letter.active and falling_letter.y > SCREEN_HEIGHT - 50:
                    self.lives -= 1
                    falling_letter.active = False
                    if self.lives <= 0:
                        self.game_over = True
                    break

    def update(self):
        if self.game_over:
            return

        # 更新粒子效果
        for particle in self.particles:
            particle.update()

        # 更新所有掉落字母
        for falling_letter in self.falling_letters[:]:
            falling_letter.update()

            # 检查是否到达底部
            if falling_letter.y > SCREEN_HEIGHT and falling_letter.active:
                self.lives -= 1
                self.falling_letters.remove(falling_letter)
                if self.lives <= 0:
                    self.game_over = True

        # 移除不活跃的字母
        self.falling_letters = [f for f in self.falling_letters if f.active or not f.is_off_screen()]

        # 生成新字母
        self.spawn_letter()

    def draw(self, surface):
        # 绘制星空背景
        surface.fill(BACKGROUND_COLOR)

        # 绘制闪烁星星
        for x, y, size in self.background_stars:
            brightness = (math.sin(pygame.time.get_ticks() / 1000 + x) + 1) / 2
            color_val = int(200 * brightness)
            pygame.draw.circle(surface, (color_val, color_val, color_val), (x, y), size)

        # 绘制粒子效果
        for particle in self.particles:
            particle.draw(surface)

        # 绘制所有掉落字母
        for falling_letter in self.falling_letters:
            falling_letter.draw(surface)

        # 绘制UI面板
        self.draw_ui(surface)

        # 游戏结束画面
        if self.game_over:
            self.draw_game_over(surface)

    def draw_ui(self, surface):
        # 绘制半透明圆角UI面板
        ui_surface = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
        pygame.draw.rect(ui_surface, UI_BG_COLOR, ui_surface.get_rect(), border_radius=15)
        surface.blit(ui_surface, (10, 10))

        # 绘制分数
        score_text = self.font.render(f"score: {self.score}", True, (255, 255, 255))
        surface.blit(score_text, (30, 20))

        # 绘制生命值条
        bar_x, bar_y = SCREEN_WIDTH - 180, 25
        bar_width, bar_height = 140, 20
        pygame.draw.rect(surface, (60, 60, 80), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        life_width = max(0, int(bar_width * self.lives / self.max_lives))
        pygame.draw.rect(surface, (76, 209, 137), (bar_x, bar_y, life_width, bar_height), border_radius=10)
        pygame.draw.rect(surface, (100, 200, 255), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=10)

        # 生命值数字
        lives_text = self.small_font.render(f"{self.lives}/{self.max_lives}", True, (255, 255, 255))
        surface.blit(lives_text, (bar_x + bar_width // 2 - lives_text.get_width() // 2,
                                  bar_y + bar_height // 2 - lives_text.get_height() // 2))

        # 绘制说明文字
        instruction = self.small_font.render("Type letters on the keyboard to eliminate falling letters", True,
                                             (200, 220, 255))
        surface.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT - 40))

    def draw_game_over(self, surface):
        # 半透明覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))

        # 游戏结束文本
        game_over_font = pygame.font.SysFont('Arial', 72, bold=True)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 100, 100))
        surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 80))

        # 最终得分
        final_score = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        surface.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2,
                                   SCREEN_HEIGHT // 2 + 20))

        # 重新开始提示
        restart_text = self.small_font.render("Press R to restart", True, (200, 220, 255))
        surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                    SCREEN_HEIGHT // 2 + 80))


def main():
    clock = pygame.time.Clock()
    game = Game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if game.game_over and event.key == K_r:
                    # 重新开始游戏
                    game = Game()
                elif not game.game_over:
                    try:
                        game.handle_input(event.unicode)
                    except AttributeError:
                        # 处理特殊按键
                        pass

        game.update()
        game.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
