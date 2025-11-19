
# (^_-)db(-_^)

import pygame, sys, random, time
from pygame.math import Vector2

pygame.init()

cell_n = 15
cell_s = 32
offset_x = 34
offset_y = 96

screen = pygame.display.set_mode((546, 607))
pygame.display.set_caption('Snake🐍')
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
SCREEN_UPDATE2 = pygame.USEREVENT
SCREEN_UPDATE3 = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 200)
pygame.time.set_timer(SCREEN_UPDATE2, 150)
pygame.time.set_timer(SCREEN_UPDATE3, 100)


class SNAKE1:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = offset_x + int(block.x * cell_s)
            y_pos = offset_y + int(block.y * cell_s)
            block_rect = pygame.Rect(x_pos, y_pos, cell_s, cell_s)
            pygame.draw.rect(screen, (60, 100, 140), block_rect)

    def add_block(self):
        self.new_block = True
    
    def move_snake(self):
        body_copy = self.body[:]
        if not self.new_block:
            body_copy = body_copy[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy
        self.new_block = False

class FRUIT1:
    def __init__(self, snake_body):
        self.randomize(snake_body)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(offset_x + int(self.pos.x * cell_s),offset_y + int(self.pos.y * cell_s),cell_s,cell_s)
        apple = pygame.image.load('apple.png')
        wtm = pygame.image.load('wtrmel.png')  
        apple = pygame.transform.smoothscale(apple, (30, 30))
        wtm = pygame.transform.smoothscale(wtm, (38, 38))
        screen.blit(apple, fruit_rect)
        screen.blit(wtm, (120,19))

    def randomize(self, snake_body):
        while True:
            self.x = random.randint(0, cell_n - 1)
            self.y = random.randint(0, cell_n - 1)
            self.pos = Vector2(self.x, self.y)
            if self.pos not in snake_body:
                break

class TEMP_FRUIT1:
    def __init__(self, snake_body):
        self.exists = False
        self.spawn_time = 0
        self.pos = None
        self.image = pygame.image.load('wtrmel.png')  
        self.image = pygame.transform.smoothscale(self.image, (34, 34))
        self.randomize(snake_body)
        
    def randomize(self, snake_body):
        if random.randint(1, 80) == 1 and not self.exists:
            while True:
                x = random.randint(0, cell_n - 1)
                y = random.randint(0, cell_n - 1)
                pos = Vector2(x, y)
                if pos not in snake_body:
                    self.pos = pos
                    self.exists = True
                    self.spawn_time = time.time()
                    break

    def draw_fruit(self):
        if self.exists:
            fruit_rect = pygame.Rect(offset_x + int(self.pos.x * cell_s), offset_y + int(self.pos.y * cell_s), cell_s, cell_s)
            screen.blit(self.image, fruit_rect)

    def check_timeout(self):
        if self.exists and time.time() - self.spawn_time > 3: 
            self.exists = False

class MAIN1:
    def __init__(self):
        self.snake = SNAKE1()
        self.fruit = FRUIT1(self.snake.body)
        self.temp_fruit = TEMP_FRUIT1(self.snake.body)

        self.score = 0
        self.score2 = 0

    def draw_grass(self):
        bg = pygame.image.load('bgsnake777.png')
        bg = pygame.transform.smoothscale(bg, (546, 606))
        screen.blit(bg, (0, 0))

    def draw_score_level(self):
        font = pygame.font.SysFont("VERDANA", 28, bold=True)
        font2 = pygame.font.SysFont("VERDANA", 20, bold=True)
        score1 = font.render(f"{self.score}", True, (0, 0, 0))
        score2 = font.render(f"{self.score2}", True, (0, 0, 0))
        level = font2.render("Level: 1", True, (0, 0, 0))
        screen.blit(score1, (62, 22))
        screen.blit(level, (435, 22))
        screen.blit(score2, (166, 22))

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.temp_fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score_level()

    def sounds(self):
        self.left = pygame.mixer.Sound('snkmove.mp3')
        self.down = pygame.mixer.Sound('snkmove2.mp3')
        self.right = pygame.mixer.Sound('snkmove3.mp3')
        self.up = pygame.mixer.Sound('snkmove4.mp3')
        self.eat = pygame.mixer.Sound('snkeat.mp3')
        self.gmovr = pygame.mixer.Sound('snkgm.mp3')
        
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize(self.snake.body)
            self.snake.add_block()
            self.score += 1
            self.eat.play()
            
        if self.temp_fruit.exists and self.temp_fruit.pos == self.snake.body[0]:
            self.temp_fruit.exists = False
            self.snake.add_block()
            self.snake.add_block()  
            self.score2 += 3
            self.eat.play()

    def check_fail(self):
        head_x = self.snake.body[0].x
        head_y = self.snake.body[0].y

        if head_x < 0:
            self.snake.body[0].x = cell_n - 1
        elif head_x >= cell_n:
            self.snake.body[0].x = 0

        if head_y < 0:
            self.snake.body[0].y = cell_n - 1
        elif head_y >= cell_n:
            self.snake.body[0].y = 0

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gmovr.play()
                return self.game_over()

    def game_over(self):
        bg = pygame.image.load('snkend.png')
        bg = pygame.transform.smoothscale(bg, (250, 250))
        overlay = pygame.Surface((1280, 620))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(bg, (150, 210))

        font1 = pygame.font.SysFont("VERDANA", 30, bold=True)
        font2 = pygame.font.SysFont("VERDANA", 20)
        text1 = font1.render("GAME OVER", True, (255, 255, 255))
        text2 = font2.render(f"Score: {self.score+self.score2}", True, (255, 255, 255))
        screen.blit(text1, (175, 240))
        screen.blit(text2, (227, 280))
        pygame.display.update()

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        return "restart"
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def update(self):
        self.draw_grass()
        self.draw_elements()
        self.snake.move_snake()
        self.check_collision()
        self.temp_fruit.check_timeout()
        self.temp_fruit.randomize(self.snake.body)
        result = self.check_fail()
        return result



class SNAKE2:
    def __init__(self):
        self.body = [Vector2(3, 10), Vector2(2, 10), Vector2(1, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = offset_x + int(block.x * cell_s)
            y_pos = offset_y + int(block.y * cell_s)
            block_rect = pygame.Rect(x_pos, y_pos, cell_s, cell_s)
            pygame.draw.rect(screen, (139, 69, 19), block_rect)

    def move_snake(self):
        body_copy = self.body[:]
        if not self.new_block:
            body_copy = body_copy[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy
        self.new_block = False

    def add_block(self):
        self.new_block = True

class FRUIT2:
    def __init__(self, snake_body):
        self.randomize(snake_body)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(offset_x + int(self.pos.x * cell_s),offset_y + int(self.pos.y * cell_s),cell_s,cell_s)
        pear = pygame.image.load('pear.png')
        tykva = pygame.image.load('tykva.png')  
        pear1 = pygame.transform.smoothscale(pear, (25, 33))
        pear2 = pygame.transform.smoothscale(pear, (28, 42))
        tykva = pygame.transform.smoothscale(tykva, (41, 41))
        screen.blit(pear1, fruit_rect)
        screen.blit(pear2, (28, 14))
        screen.blit(tykva, (120,18))

    def randomize(self, snake_body):
        while True:
            self.x = random.randint(0, cell_n - 2)
            self.y = random.randint(0, cell_n - 2)
            self.pos = Vector2(self.x, self.y)
            if self.pos not in snake_body:
                break

class TEMP_FRUIT2:
    def __init__(self, snake_body):
        self.exists = False
        self.spawn_time = 0
        self.pos = None
        self.image = pygame.image.load('tykva.png')  
        self.image = pygame.transform.smoothscale(self.image, (38, 38))
        self.randomize(snake_body)

    def randomize(self, snake_body):
        if random.randint(1, 80) == 1 and not self.exists:
            while True:
                x = random.randint(0, cell_n - 1)
                y = random.randint(0, cell_n - 1)
                pos = Vector2(x, y)
                if pos not in snake_body:
                    self.pos = pos
                    self.exists = True
                    self.spawn_time = time.time()
                    break

    def draw_fruit(self):
        if self.exists:
            fruit_rect = pygame.Rect(offset_x + int(self.pos.x * cell_s), offset_y + int(self.pos.y * cell_s), cell_s, cell_s)
            screen.blit(self.image, fruit_rect)

    def check_timeout(self):
        if self.exists and time.time() - self.spawn_time > 4:  
            self.exists = False

class MAIN2:
    def __init__(self):
        self.snake = SNAKE2()
        self.fruit = FRUIT2(self.snake.body)
        self.temp_fruit = TEMP_FRUIT2(self.snake.body)
        self.score = 0
        self.score2 = 0

    def draw_grass(self):
        bg = pygame.image.load('bgsnake888.png')
        bg = pygame.transform.smoothscale(bg, (546, 606))
        screen.blit(bg, (0, 0))

    def draw_score_level(self):
        font = pygame.font.SysFont("VERDANA", 28, bold=True)
        font2 = pygame.font.SysFont("VERDANA", 20, bold=True)
        score1 = font.render(f"{self.score}", True, (0, 0, 0))
        score2 = font.render(f"{self.score2}", True, (0, 0, 0))
        level = font2.render("Level: 2", True, (0, 0, 0))
        screen.blit(score1, (62, 22))
        screen.blit(score2, (166, 22))
        screen.blit(level, (435, 22))

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.temp_fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score_level()

    def sounds(self):
        self.left = pygame.mixer.Sound('snkmove.mp3')
        self.down = pygame.mixer.Sound('snkmove2.mp3')
        self.right = pygame.mixer.Sound('snkmove3.mp3')
        self.up = pygame.mixer.Sound('snkmove4.mp3')
        self.eat = pygame.mixer.Sound('snkeat.mp3')
        self.gmovr = pygame.mixer.Sound('snkgm.mp3')

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize(self.snake.body)
            self.snake.add_block()
            self.score += 1
            self.eat.play()
            
        if self.temp_fruit.exists and self.temp_fruit.pos == self.snake.body[0]:
            self.temp_fruit.exists = False
            self.snake.add_block()
            self.snake.add_block()  
            self.score2 += 3
            self.eat.play()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_n or not 0 <= self.snake.body[0].y < cell_n:
            self.gmovr.play()
            return self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gmovr.play()
                return self.game_over()

    def game_over(self):
        bg = pygame.image.load('snkend2.png')
        bg = pygame.transform.smoothscale(bg, (250, 250))
        overlay = pygame.Surface((1280, 620))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(bg, (150, 210))

        font1 = pygame.font.SysFont("VERDANA", 30, bold=True)
        font2 = pygame.font.SysFont("VERDANA", 20)
        text1 = font1.render("GAME OVER", True, (255, 255, 255))
        text2 = font2.render(f"Score: {self.score + self.score2}", True, (255, 255, 255))
        screen.blit(text1, (175, 240))
        screen.blit(text2, (227, 280))
        pygame.display.update()

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        return "restart"
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def update(self):
        self.draw_grass()
        self.draw_elements()
        self.snake.move_snake()
        self.check_collision()
        self.temp_fruit.check_timeout()  
        self.temp_fruit.randomize(self.snake.body)
        result = self.check_fail()
        return result



class SNAKE3:
    def __init__(self):
        self.body = [Vector2(3, 10), Vector2(2, 10), Vector2(1, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = offset_x + int(block.x * cell_s)
            y_pos = offset_y + int(block.y * cell_s)
            block_rect = pygame.Rect(x_pos, y_pos, cell_s, cell_s)
            pygame.draw.rect(screen, (20, 40, 80), block_rect)

    def move_snake(self):
        body_copy = self.body[:]
        if not self.new_block:
            body_copy = body_copy[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy
        self.new_block = False

    def add_block(self):
        self.new_block = True

class FRUIT3:
    def __init__(self, snake_body):
        self.randomize(snake_body)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(offset_x + int(self.pos.x * cell_s),offset_y + int(self.pos.y * cell_s),cell_s,cell_s)
        blue = pygame.image.load('blue.png')
        ice = pygame.image.load('mand.png')  
        blue1 = pygame.transform.smoothscale(blue, (33, 33))
        blue2 = pygame.transform.smoothscale(blue, (44, 44))
        ice = pygame.transform.smoothscale(ice, (38, 38))
        screen.blit(blue1, fruit_rect)
        screen.blit(blue2, (20, 17))
        screen.blit(ice, (120,18))

    def randomize(self, snake_body):
        while True:
            self.x = random.randint(0, cell_n - 2)
            self.y = random.randint(0, cell_n - 2)
            self.pos = Vector2(self.x, self.y)
            if self.pos not in snake_body:
                break

class TEMP_FRUIT3:
    def __init__(self, snake_body):
        self.exists = False
        self.spawn_time = 0
        self.pos = None
        self.image = ice = pygame.image.load('mand.png')  
        self.image = pygame.transform.smoothscale(ice, (30, 30))
        self.randomize(snake_body)

    def randomize(self, snake_body):
        if random.randint(1, 80) == 1 and not self.exists:
            while True:
                x = random.randint(0, cell_n - 1)
                y = random.randint(0, cell_n - 1)
                pos = Vector2(x, y)
                if pos not in snake_body:
                    self.pos = pos
                    self.exists = True
                    self.spawn_time = time.time()
                    break

    def draw_fruit(self):
        if self.exists:
            fruit_rect = pygame.Rect(offset_x + int(self.pos.x * cell_s), offset_y + int(self.pos.y * cell_s), cell_s, cell_s)
            screen.blit(self.image, fruit_rect)

    def check_timeout(self):
        if self.exists and time.time() - self.spawn_time > 3:  
            self.exists = False

class BORDER:
    def __init__(self, snake_body, fruit_pos):
        self.blocks = []
        self.randomize(snake_body, fruit_pos)

    def randomize(self, snake_body, fruit_pos):
        self.blocks = []
        num_blocks = random.randint(3, 5) 

        for _ in range(num_blocks):
            while True:
                x = random.randint(0, cell_n - 1)
                y = random.randint(0, cell_n - 1)
                pos = Vector2(x, y)
                if pos not in snake_body and pos != fruit_pos:
                    self.blocks.append(pos)
                    break

    def draw_border(self):
        for block in self.blocks:
            x_pos = offset_x + int(block.x * cell_s)
            y_pos = offset_y + int(block.y * cell_s)
            block_rect = pygame.Rect(x_pos, y_pos, cell_s, cell_s)

            
            pygame.draw.rect(screen, (180, 230, 255), block_rect)  
            pygame.draw.rect(screen, (100, 160, 220), block_rect, 2)  

class MAIN3:
    def __init__(self):
        self.snake = SNAKE3()
        self.fruit = FRUIT3(self.snake.body)
        self.temp_fruit = TEMP_FRUIT3(self.snake.body)
        self.border = BORDER(self.snake.body, self.fruit.pos)
        self.score = 0
        self.score2 = 0

    def draw_grass(self):
        bg = pygame.image.load('bgsnake999.png')
        bg = pygame.transform.smoothscale(bg, (546, 606))
        screen.blit(bg, (0, 0))

    def draw_score_level(self):
        font = pygame.font.SysFont("VERDANA", 28, bold=True)
        font2 = pygame.font.SysFont("VERDANA", 20, bold=True)
        score1 = font.render(f"{self.score}", True, (0, 0, 0))
        score2 = font.render(f"{self.score2}", True, (0, 0, 0))
        level = font2.render("Level: 3", True, (0, 0, 0))
        screen.blit(score1, (62, 22))
        screen.blit(score2, (162, 22))
        screen.blit(level, (435, 22))

    def draw_elements(self):
        self.border.draw_border()
        self.fruit.draw_fruit()
        self.temp_fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score_level()

    def sounds(self):
        self.left = pygame.mixer.Sound('snkmove.mp3')
        self.down = pygame.mixer.Sound('snkmove2.mp3')
        self.right = pygame.mixer.Sound('snkmove3.mp3')
        self.up = pygame.mixer.Sound('snkmove4.mp3')
        self.eat = pygame.mixer.Sound('snkeat.mp3')
        self.gmovr = pygame.mixer.Sound('snkgm.mp3')

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize(self.snake.body)
            self.border.randomize(self.snake.body, self.fruit.pos)
            self.snake.add_block()
            self.score += 1
            self.eat.play()
            
        if self.temp_fruit.exists and self.temp_fruit.pos == self.snake.body[0]:
            self.temp_fruit.exists = False
            self.snake.add_block()
            self.snake.add_block()  
            self.score2 += 3
            self.eat.play()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_n or not 0 <= self.snake.body[0].y < cell_n:
            self.gmovr.play()
            return self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gmovr.play()
                return self.game_over()
        for wall in self.border.blocks:
            if wall == self.snake.body[0]:
                self.gmovr.play()
                return self.game_over()

    def game_over(self):
        bg = pygame.image.load('snkend3.png')
        bg = pygame.transform.smoothscale(bg, (250, 250))
        overlay = pygame.Surface((1280, 620))
        overlay.set_alpha(100)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        screen.blit(bg, (150, 210))

        font1 = pygame.font.SysFont("VERDANA", 30, bold=True)
        font2 = pygame.font.SysFont("VERDANA", 20)
        text1 = font1.render("GAME OVER", True, (255, 255, 255))
        text2 = font2.render(f"Score: {self.score+self.score2}", True, (255, 255, 255))
        screen.blit(text1, (175, 240))
        screen.blit(text2, (227, 280))
        pygame.display.update()

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        return "restart"
                    if e.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def update(self):
        self.draw_grass()
        self.draw_elements()
        self.snake.move_snake()
        self.check_collision()
        self.temp_fruit.check_timeout()  
        self.temp_fruit.randomize(self.snake.body)
        result = self.check_fail()
        return result


def scane1():
    main_game = MAIN1()
    main_game.sounds()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == SCREEN_UPDATE:
                result = main_game.update()
                if result == "restart":
                    return "scene1"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                        main_game.up.play()
                if e.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                        main_game.down.play()
                if e.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                        main_game.left.play()
                if e.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                        main_game.right.play()
                if e.key == pygame.K_q:
                    st = pygame.mixer.Sound('start.mp3')
                    st.play()
                    return "scene2"
        pygame.display.update()
        clock.tick(60)

def scane2():
    main_game = MAIN2()
    main_game.sounds()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == SCREEN_UPDATE2:
                result = main_game.update()
                if result == "restart":
                    return "scene2"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                        main_game.up.play()
                if e.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                        main_game.down.play()
                if e.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                        main_game.left.play()
                if e.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                        main_game.right.play()
                if e.key == pygame.K_q:
                    st = pygame.mixer.Sound('start.mp3')
                    st.play()
                    return "scene3"
        pygame.display.update()
        clock.tick(60)
        
def scane3():
    main_game = MAIN3()
    main_game.sounds()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == SCREEN_UPDATE3:
                result = main_game.update()
                if result == "restart":
                    return "scene3"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                        main_game.up.play()
                if e.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                        main_game.down.play()
                if e.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                        main_game.left.play()
                if e.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                        main_game.right.play()
                if e.key == pygame.K_q:
                    st = pygame.mixer.Sound('start.mp3')
                    st.play()
                    return "scene1"
        pygame.display.update()
        clock.tick(60)


def start():
    bg = pygame.image.load('bgsnake777.png')
    bg = pygame.transform.smoothscale(bg, (546, 606))
    bgstart = pygame.image.load('fist.png')
    bgstart = pygame.transform.smoothscale(bgstart, (160, 160))
    st = pygame.mixer.Sound('start.mp3')
    font = pygame.font.SysFont("VERDANA", 25)
    text1 = font.render("Press [SPACE] to Start", True, (0, 0, 0))
    text2 = font.render("[Q] next level", True, (0, 0, 0))
    text3 = font.render("[R] restart", True, (0, 0, 0))
    screen.blit(bg, (0, 0))
    screen.blit(bgstart, (198, 212))
    screen.blit(text1, (130, 400))
    screen.blit(text2, (186, 440))
    screen.blit(text3, (205, 480))
    pygame.display.update()
    clock.tick(20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    st.play()
                    pygame.time.delay(500)
                    return "scene1"

def run_game():
    start()
    current_scene = "scene1"
    while True:
        if current_scene == "scene1":
            current_scene = scane1()
        elif current_scene == "scene2":
            current_scene = scane2()
        elif current_scene == "scene3":
            current_scene = scane3()

run_game()
