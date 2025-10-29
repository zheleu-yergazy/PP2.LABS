import pygame
import sys
from pygame import mixer

pygame.init()   
mixer.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мы в универе")

speed = 10
x, y = 300, 200
radius = 25
color = (200, 30, 30)
touch = False

clock = pygame.time.Clock()


sound = pygame.mixer.Sound('move.mp3')
sound2 = pygame.mixer.Sound('border.mp3')
sound.set_volume(0.5)   
sound2.set_volume(0.08)  

run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        
        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                sound.play()

    keys = pygame.key.get_pressed()
    touch = False

    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    
    if x - radius <= 0:
        x = radius
        touch = True
    if x + radius >= WIDTH:
        x = WIDTH - radius
        touch = True
    if y - radius <= 0:
        y = radius
        touch = True
    if y + radius >= HEIGHT:
        y = HEIGHT - radius
        touch = True

   
    if touch:
        color = (30, 30, 200)
        sound2.play()
    else:
        color = (200, 30, 30)

    screen.fill((245, 245, 245))
    pygame.draw.circle(screen, color, (x, y), radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()