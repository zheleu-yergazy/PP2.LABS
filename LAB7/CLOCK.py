import pygame
import datetime
import math
import sys

pygame.init()

sound = pygame.mixer.Sound('tictac.mp3')
sound.set_volume(0.5)
sound.play(-1)

screen = pygame.display.set_mode((640, 500))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()


clock_img = pygame.image.load("mickey.png")
clock_img = pygame.transform.scale(clock_img, (650, 500))

min_img = pygame.image.load("c.png")
min_img = pygame.transform.scale(min_img, (40, 110))

sec_img = pygame.image.load("c1.png")
sec_img = pygame.transform.scale(sec_img, (60, 110))

CENTER = (325, 252)
FPS = 1
COLOR = (180, 20, 20)

def drawrotated(surface, image, center, pivot, angle_deg):
    # Поворачиваем изображение
    rotated = pygame.transform.rotate(image, angle_deg)
    rect = rotated.get_rect()

    # исходные размеры и смещение pivot относительно центра изображения
    w, h = image.get_width(), image.get_height()
    cx, cy = w / 2.0, h / 2.0
    dx = pivot[0] - cx
    dy = pivot[1] - cy

    # угол в радианах
    a = math.radians(angle_deg)

    # вычисляем координату верхнего левого угла повёрнутого изображения,
    # чтобы после поворота pivot оказался в позиции center
    # формулы: центр повёрнутого rect будет в (center + rotated_offset)
    # где rotated_offset = rotate(-a) * (center_of_image - pivot)
    rot_cx = rect.width / 2.0
    rot_cy = rect.height / 2.0

    # смещение после поворота (тригонометрия)
    ox = -dx * math.cos(a) + dy * math.sin(a)
    oy = -dx * math.sin(a) - dy * math.cos(a)

    # позиция верхнего левого угла для blit
    draw_x = center[0] - rot_cx + ox
    draw_y = center[1] - rot_cy + oy

    # blit с int-координатами
    surface.blit(rotated, (int(draw_x), int(draw_y)))

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

    drawrotated(screen, min_img, CENTER, (min_img.get_width()/2, min_img.get_height()), -minute * 6)
    drawrotated(screen, sec_img, CENTER, (sec_img.get_width()/2, sec_img.get_height()), -second * 6)

    pygame.draw.circle(screen, COLOR, CENTER, 10)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
