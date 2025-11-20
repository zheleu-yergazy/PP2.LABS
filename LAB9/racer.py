import pygame, sys, random
from pygame.locals import *

def main():
    pygame.init()
    clock = pygame.time.Clock()

    bgsound = pygame.mixer.Sound('bgracer.mp3')
    bgsound.set_volume(0.4)
    bgsound.play(-1)
    trafic = pygame.mixer.Sound('trafic.mp3')
    trafic.set_volume(0.6)
    trafic.play(-1)
    lose = pygame.mixer.Sound('lose.wav')
    accident = pygame.mixer.Sound('crash.wav')
    st = pygame.mixer.Sound('start.mp3')
    collect = pygame.mixer.Sound('collect.wav')
    move = pygame.mixer.Sound('move.mp3')
    move.set_volume(0.2)

    FPS = 60
    RED = (255,0,0)
    YELLOW = (255,165,0)
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    WIDTH = 800
    HEIGHT = 600
    LANES = [230, 347, 473, 600] 
    SPEED = 6
    SCORE = 0

    font = pygame.font.SysFont("Verdana",40,bold = True)
    sfont = pygame.font.SysFont("Verdana",25,bold = True)
    ssfont = pygame.font.SysFont("Verdana",20,bold = True)
    Sssfont = pygame.font.SysFont("Verdana",10,bold = True)
    gmor = font.render("Game  Over", True, RED)

    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    screen.fill(WHITE)
    pygame.display.set_caption("Racer")

    bg = pygame.image.load('road.jpg')
    bg = pygame.transform.smoothscale(bg,(WIDTH,HEIGHT))
    bgstart = pygame.image.load('bgstart.jpg')
    bgstart = pygame.transform.smoothscale(bgstart,(WIDTH,HEIGHT))
    bgend = pygame.image.load('gameover.jpg')
    bgend = pygame.transform.smoothscale(bgend,(WIDTH,HEIGHT))

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('enemy.png')
            self.image = pygame.transform.smoothscale(self.image,(70,100))
            self.rect = self.image.get_rect()
            self.rect.midbottom = (random.choice(LANES),0)
            self.mask = pygame.mask.from_surface(self.image)

        def move(self):
            self.rect.move_ip(0,SPEED+5)
            
            if self.rect.top > 600:
                self.rect.top = 0
                self.rect.midbottom = (random.choice(LANES),0)

            
    class Petrol1(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('petrol.png')
            self.image = pygame.transform.smoothscale(self.image,(60,50))
            self.rect = self.image.get_rect()
            self.rect.midbottom = (random.randint(220,WIDTH -220),-500)
            self.mask = pygame.mask.from_surface(self.image)
            
        def move(self):
            global SCORE
            self.rect.move_ip(0,SPEED)
            if self.rect.top > 600:
                self.rect.top = 0
                self.rect.midbottom = (random.randint(220,WIDTH -220),-500)
                
    class Petrol2(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('petrol2.png')
            self.image = pygame.transform.smoothscale(self.image,(35,39))
            self.rect = self.image.get_rect()
            self.rect.midbottom = (random.randint(220,WIDTH -220),-2500)
            self.mask = pygame.mask.from_surface(self.image)
            
        def move(self):
            global SCORE
            self.rect.move_ip(0,SPEED)
            if self.rect.top > 600:
                self.rect.top = 0
                self.rect.midbottom = (random.randint(220,WIDTH -220),-2500)
                
    class Petrol3(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('petrol3.png')
            self.image = pygame.transform.smoothscale(self.image,(45,45))
            self.rect = self.image.get_rect()
            self.rect.midbottom = (random.randint(220,WIDTH -220),-6000)
            self.mask = pygame.mask.from_surface(self.image)
            
        def move(self):
            global SCORE
            self.rect.move_ip(0,SPEED)
            if self.rect.top > 600:
                self.rect.top = 0
                self.rect.midbottom = (random.randint(220,WIDTH -220),-6000)
            
            
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('player.png')
            self.image = pygame.transform.smoothscale(self.image,(140,120))
            self.rect = self.image.get_rect()
            self.rect.center = (400,530)
            self.mask = pygame.mask.from_surface(self.image)
            
        def move(self):
            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:
                    self.rect.move_ip(-10,0)
            if keys[K_RIGHT]:
                    self.rect.move_ip(10,0)
    
    def start():
        while True:
            screen.blit(bgstart,(0, 0))
            title = sfont.render("Press SPACE to Start", True, YELLOW)
            screen.blit(title, (250, 500))
            title2 = ssfont.render("Exit: ESC", True, BLACK)
            screen.blit(title2, (690, 565))
            title3 = ssfont.render("Use: LEFT | RIGHT", True, WHITE)
            screen.blit(title3, (285, 460))
            pygame.display.update()
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_SPACE:
                            st.play()
                            return  
        
    def gameover():
        bgsound.stop()
        trafic.stop()
        accident.play()
        
        screen.blit(bgend,(0,0))
        
        score = font.render(f"SCORE: {SCORE}",True,YELLOW)
        screen.blit(score,(300,510))
        exit = ssfont.render("Exit: ESC",True,WHITE)
        rest = ssfont.render("Restart: R",True,WHITE)
        screen.blit(exit,(690,565))
        screen.blit(rest,(10,565))
        pygame.display.update()
        
        for entity in all:
            entity.kill() 
        
        pygame.time.delay(1000)
        lose.play()
        
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r: 
                        main()
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    P1 = Player()
    E1 = Enemy()
    PT1 = Petrol1()
    PT2 = Petrol2()
    PT3 = Petrol3()

    enemies = pygame.sprite.Group()
    enemies.add(E1)
    petrol1 = pygame.sprite.Group()
    petrol1.add(PT1)
    petrol2 = pygame.sprite.Group()
    petrol2.add(PT2)
    petrol3 = pygame.sprite.Group()
    petrol3.add(PT3)
    all = pygame.sprite.Group()
    all.add(P1)
    all.add(PT1)
    all.add(PT2)
    all.add(PT3)
    all.add(E1) 
    
    next_up = 5
    bg_y = 0
    start()
        
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key in (K_LEFT,K_RIGHT):
                    move.play()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            
        bg_y += SPEED 
        if bg_y >= HEIGHT:
            bg_y = 0
        screen.blit(bg,(0,bg_y))
        screen.blit(bg,(0,bg_y - HEIGHT))
        
        if SCORE >= next_up:
            SPEED += 1
            next_up += 5

        if P1.rect.left <= 79:
            gameover()
        if P1.rect.right >= 730:
            gameover()
        
        for entity in all:
            screen.blit(entity.image,entity.rect)
            entity.move()
            
        if pygame.sprite.spritecollide(P1, enemies, False, pygame.sprite.collide_mask):
            gameover()
            
        petrol_hit = pygame.sprite.spritecollide(P1, petrol1, False, pygame.sprite.collide_mask)
        if petrol_hit:
            for petrol in petrol_hit:
                SCORE += 1                     
                collect.play()  
                petrol.rect.top = 0      
                petrol.rect.midbottom = (random.randint(220,WIDTH-220), -500)
        
        petrol_hit = pygame.sprite.spritecollide(P1, petrol2, False, pygame.sprite.collide_mask)
        if petrol_hit:
            for petrol in petrol_hit:
                SCORE += 2                     
                collect.play()  
                petrol.rect.top = 0      
                petrol.rect.midbottom = (random.randint(220,WIDTH-220), -2000)
        
        petrol_hit = pygame.sprite.spritecollide(P1, petrol3, False, pygame.sprite.collide_mask)
        if petrol_hit:
            for petrol in petrol_hit:
                SCORE += 3                     
                collect.play()  
                petrol.rect.top = 0      
                petrol.rect.midbottom = (random.randint(220,WIDTH-220), -6000)
            
        score = sfont.render(f"SCORE: {SCORE}",True,YELLOW)
        score_rect = pygame.Rect(610,21,165,30)
        pygame.draw.rect(screen,BLACK,score_rect,border_radius=8)
        screen.blit(score,(620,20))
        pygame.display.update()
        clock.tick(FPS)
       
main()     
            
