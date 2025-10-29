import pygame
import datetime
import math
import sys

pygame.init()

# --- звук ---
sound = pygame.mixer.Sound('tictac.mp3')
sound.set_volume(0.5)
sound.play(-1)

# --- окно ---
screen = pygame.display.set_mode((640, 500))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()

# --- изображения ---
clock_img = pygame.image.load("mickey.png")
clock_img = pygame.transform.scale(clock_img, (650, 500))

min_img = pygame.image.load("c.png")
min_img = pygame.transform.scale(min_img, (40, 110))

sec_img = pygame.image.load("c1.png")
sec_img = pygame.transform.scale(sec_img, (60, 110))

# --- центр часов ---
CENTER = (325, 252)
FPS = 1
COLOR = (180, 20, 20)


def drawrotated(surf, image, center, pivot, angle):
    """Поворачивает изображение вокруг pivot, оставляя центр в center"""
    rotated = pygame.transform.rotate(image, angle)
    rect = rotated.get_rect()

    dx = pivot[0] - image.get_width() / 2
    dy = pivot[1] - image.get_height() / 2

    # используем math, а не pygame.math
    angle_rad = math.radians(angle)
    x = center[0] - rect.width / 2 - dx * math.cos(angle_rad) + dy * math.sin(angle_rad)
    y = center[1] - rect.height / 2 - dx * math.sin(angle_rad) - dy * math.cos(angle_rad)

    surf.blit(rotated, (x, y))


# --- основной цикл ---
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    now = datetime.datetime.now()
    minute = now.minute
    second = now.second

    screen.fill((0, 0, 0))
    screen.blit(clock_img, (0, 0))

    # рисуем стрелки
    drawrotated(screen, min_img, CENTER, (min_img.get_width()/2, min_img.get_height()), -minute * 6)
    drawrotated(screen, sec_img, CENTER, (sec_img.get_width()/2, sec_img.get_height()), -second * 6)

    # центр (ось)
    pygame.draw.circle(screen, COLOR, CENTER, 10)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
