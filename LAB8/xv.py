import pygame
import random
import time

pygame.init()

screen = pygame.display.set_mode((1280,620))
pygame.display.set_caption("Horse Racer!")
font1 = pygame.font.SysFont("Arial",115,bold=True)
font2 = pygame.font.SysFont("Arial",40,bold=True)
title = pygame.font.SysFont("Arial",120,bold=True)
text = pygame.font.SysFont("Arial",50,bold=True)
instruction = pygame.font.SysFont("Arial", 30, bold=True)
clock = pygame.time.Clock()

bg = pygame.image.load('png copy.png')
bg = pygame.transform.smoothscale(bg,(1280,620))
bgstart = pygame.image.load('bg.jpg')
bgstart = pygame.transform.smoothscale(bgstart,(1280,620))
car = pygame.image.load('car.png')
car = pygame.transform.smoothscale(car,(350,200))
rumimg = pygame.image.load('rum.png')
rumimg = pygame.transform.smoothscale(rumimg,(40,50))
barrel = pygame.image.load('tnt.png')
barrel = pygame.transform.smoothscale(barrel,(120,100))


bgsound = pygame.mixer.Sound('bgsound.mp3')
bgsound.set_volume(0.3)
bgsound.play(-1)
bgpov = pygame.mixer.Sound('pov.mp3')
bgpov.set_volume(0.4)
horse = pygame.mixer.Sound('horse.wav')
horse.set_volume(0.5)
st = pygame.mixer.Sound('start.mp3')
st.set_volume(1)
boom = pygame.mixer.Sound('crush.wav')
boom.set_volume(1)
move = pygame.mixer.Sound('move.mp3')
move.set_volume(0.1)
collect = pygame.mixer.Sound('collect.wav')
collect.set_volume(0.2)
lose = pygame.mixer.Sound('lose.wav')
lose.set_volume(1)

def crush(car):
    car = pygame.image.load('crush.png')
    car = pygame.transform.smoothscale(car,(300,200))
    boom.play()
    screen.blit(car,(900,y))
    txt1 = font1.render("GAME OVER!", True, (255,0,0))
    txt2 = text.render(f"Score: {score}", True, (0,0,0))
    txt3 = text.render(f"Level: {level}", True,(0,0,0))
    screen.blit(txt1,(280,230))
    screen.blit(txt2,(530,370))
    screen.blit(txt3,(540,420))
    overlay = pygame.Surface((1280, 620))  
    overlay.set_alpha(80)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    bgpov.stop()
    horse.stop()
    bgsound.stop()
    pygame.display.update()
    time.sleep(0.6)
    lose.play()
    time.sleep(3)
    exit()
    
def start():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    st.play()
                    return  
    
        screen.blit(bgstart, (0, 0))
        overlay = pygame.Surface((1280, 620))  
        overlay.set_alpha(35)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        titl = title.render("Horse Racer!", True, (0,0,0))
        press = text.render("Press SPACE to Start", True, (255, 255, 255))
        inst1 = instruction.render("←  Ускорение", True, (255, 165, 0))
        inst2 = instruction.render("→  Замедление", True, (255, 165, 0))
        inst3 = instruction.render("↑  Вверх   |   ↓  Вниз", True, (255, 165, 0))
        
        screen.blit(titl, titl.get_rect(center=(650, 140)))
        screen.blit(inst1, inst1.get_rect(center=(640, 280)))
        screen.blit(inst2, inst2.get_rect(center=(640, 320)))
        screen.blit(inst3, inst3.get_rect(center=(640, 360)))
        screen.blit(press, press.get_rect(center=(640, 550)))
        pygame.display.update()
        clock.tick(60)

y = 300
bg1 = 0
bg2 = -1280
score = 0

carspeed = 9
bgspeed = 8
maxspeed = 20
minspeed = 8

level = 1
maxlevel = 3
minlevel = 1

rums = []
for rum in range(2):
    rums.append([random.randint(-800,-100),random.randint(160,500)])
    
barrels = []
for barr in range(3):
    barrels.append([random.randint(-800,-100),random.randint(170,500)])


start()
bgpov.play(-1)
horse.play(-1)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
        elif e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_UP,pygame.K_DOWN):
                move.play()
            elif e.key == pygame.K_LEFT:
                bgspeed = min(maxspeed, bgspeed + 5)
                level = min(maxlevel, level + 1)
            elif e.key == pygame.K_RIGHT:
                bgspeed = max(minspeed, bgspeed - 5)
                level = max(minlevel, level - 1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        y -= carspeed
    if keys[pygame.K_DOWN]:
        y += carspeed

    if y <= 80:
        y = 80
        crush(car)
    if y >= 470:
        y = 470
        crush(car)
        
    bg1 += bgspeed
    bg2 += bgspeed
    if bg1 >= 1280:
        bg1 = -1280
    if bg2 >= 1280:
        bg2 = -1280
    
    for rum in rums:
        rum[0] += bgspeed
        if rum[0] > 1280:
            rum[0] = random.randint(-800,-100)
            rum[1] = random.randint(160,500)
    carRect = pygame.Rect(850,y,180,120)
    
    for barr in barrels:
        barr[0] += bgspeed
        if barr[0] > 1400:
            barr[0] = random.randint(-800,-100)
            barr[1] = random.randint(170,500)
            
    for rum in rums:
        rumRect = pygame.Rect(rum[0],rum[1],25,30)
        if carRect.colliderect(rumRect):
            collect.play()
            score += 1
            rum[0] = random.randint(-800,-100)
            rum[1] = random.randint(160,500)
    for barr in barrels:
        barrelRect = pygame.Rect(barr[0],barr[1],20,30)
        if carRect.colliderect(barrelRect):
            crush(car)
            
    screen.blit(bg,(bg1,0))
    screen.blit(bg,(bg2,0))
    for rum in rums:
        screen.blit(rumimg,(rum[0],rum[1]))
    for barr in barrels:
        screen.blit(barrel,(barr[0],barr[1]))
    screen.blit(rumimg,(195,12))
    screen.blit(car,(850,y))
    txt2 = font2.render(f"Score: {score}", True, (0,0,0))
    txt3 = font2.render(f"Level: {level}", True,(0,0,0))
    screen.blit(txt2,(20,20))
    screen.blit(txt3,(280,20))
    pygame.display.update()
    clock.tick(60)
