import pygame
import datetime
import sys

pygame.init()

sound = pygame.mixer.Sound('tictac.mp3')
sound.set_volume(0.5)
sound.play()

screen = pygame.display.set_mode((640, 500))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()


clock_img = pygame.image.load("mickey.png")
clock_img = pygame.transform.scale(clock_img, (650, 500))

min = pygame.image.load("c.png")
min = pygame.transform.scale(min, (40, 110))

sec = pygame.image.load("c1.png")
sec = pygame.transform.scale(sec, (60, 110))

CENTER = (325, 252)
COLOR = (180, 20, 20)

def drawrotated(surf, image, center, pivot, angle):
    rotated = pygame.transform.rotate(image, angle)
    offset = pygame.math.Vector2(image.get_rect().center) - pygame.math.Vector2(pivot)
    offset = offset.rotate(-angle)
    rect = rotated.get_rect(center=pygame.math.Vector2(center) + offset)
    surf.blit(rotated, rect)

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

    drawrotated(screen, min, CENTER, (min.get_width()/2, min.get_height()), -minute * 6)
    drawrotated(screen, sec, CENTER, (sec.get_width()/2, sec.get_height()), -second * 6)

    pygame.draw.circle(screen, COLOR, CENTER, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
