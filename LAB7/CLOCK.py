import pygame
import datetime

pygame.init()
sound = pygame.mixer.Sound('tictac.mp3')
sound.set_volume(0.5)
sound.play(-1)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()
clock_img = pygame.image.load("base_micky.jpg")
clock_img = pygame.transform.scale(clock_img, (800, 600))
hour_img = pygame.image.load("c copy.png")
hour_img = pygame.transform.scale(hour_img, (55, 135))
min_img = pygame.image.load("c.png")
min_img = pygame.transform.scale(min_img, (55, 135))
sec_img = pygame.image.load("c1.png")
sec_img = pygame.transform.scale(sec_img, (65, 135))

def drawrot(surf, image, center, pivot, angle):
    rotated = pygame.transform.rotate(image, angle)
    offset = pygame.math.Vector2(image.get_rect().center) - pygame.math.Vector2(pivot)
    offset = offset.rotate(-angle)
    rect = rotated.get_rect(center=pygame.math.Vector2(center) + offset)
    surf.blit(rotated, rect)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    screen.fill((255,255,255))
    screen.blit(clock_img,(0,0))

    drawrot(screen, min_img, (400,300), (min_img.get_width()/2, min_img.get_height()), -minute * 6)
    drawrot(screen, sec_img, (400,300), (sec_img.get_width()/2, sec_img.get_height()), -second * 6)
    drawrot(screen, sec_img, (400,300), (sec_img.get_width()/2, sec_img.get_height()), -hour * 6)

    
    pygame.draw.circle(screen, (180,20,20), (400,300), 13)
    pygame.display.flip()   
    clock.tick(60)




