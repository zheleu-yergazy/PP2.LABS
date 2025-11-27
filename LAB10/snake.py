# (^_-)db(-_^)

import pygame, sys, random, time
from pygame.math import Vector2
from config import load_config
from connect import connect

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


def get_db_connection():
    try:
        config = load_config()
        connection = connect(config)
        cursor = connection.cursor() 
       
        return connection
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        return None


def init_database():
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
           
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(50) PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_game_state (
                    username VARCHAR(50) PRIMARY KEY REFERENCES users(username),
                    level INTEGER DEFAULT 1,
                    score INTEGER DEFAULT 0,
                    snake_body TEXT,
                    snake_direction_x INTEGER,
                    snake_direction_y INTEGER,
                    fruit_pos_x INTEGER,
                    fruit_pos_y INTEGER,
                    temp_fruit_exists BOOLEAN DEFAULT FALSE,
                    temp_fruit_pos_x INTEGER,
                    temp_fruit_pos_y INTEGER,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            connection.commit()
            print("успешно")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            cursor.close()
            connection.close()


init_database()

def get_or_create_user(username):
    connection = get_db_connection()
    if not connection:
        return 0, 1, None  
    
    try:
        cursor = connection.cursor()
        
       
        cursor.execute("""
            INSERT INTO users (username) 
            VALUES (%s) 
            ON CONFLICT (username) DO NOTHING
        """, (username,))
        
      
        cursor.execute("""
            SELECT level, score, snake_body, snake_direction_x, snake_direction_y,
                   fruit_pos_x, fruit_pos_y, temp_fruit_exists, temp_fruit_pos_x, temp_fruit_pos_y
            FROM user_game_state 
            WHERE username = %s
        """, (username,))
        
        result = cursor.fetchone()
        
        if result:
            level, score, snake_body, dir_x, dir_y, fruit_x, fruit_y, temp_exists, temp_x, temp_y = result
            
        
            saved_state = {
                "level": level,
                "score": score,
                "snake_body": snake_body,
                "snake_direction": Vector2(dir_x, dir_y) if dir_x is not None else Vector2(1, 0),
                "fruit_pos": Vector2(fruit_x, fruit_y) if fruit_x is not None else None,
                "temp_fruit_exists": temp_exists,
                "temp_fruit_pos": Vector2(temp_x, temp_y) if temp_x is not None else None
            }
            print(f"Загружено : уровень {level}, очки {score}")
            return score, level, saved_state
        else:
         
            cursor.execute("""
                INSERT INTO user_game_state (username, level, score) 
                VALUES (%s, 1, 0)
                ON CONFLICT (username) DO NOTHING
            """, (username,))
            connection.commit()
            print("Создан пользователь")
            return 0, 1, None
            
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return 0, 1, None
    finally:
        cursor.close()
        connection.close()

def save_game_state(username, level, score, snake_body=None, snake_direction=None, fruit_pos=None, temp_fruit_exists=False, temp_fruit_pos=None):
    
    connection = get_db_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        
    
        snake_body_str = str([(b.x, b.y) for b in snake_body]) if snake_body else None
        dir_x = snake_direction.x if snake_direction else None
        dir_y = snake_direction.y if snake_direction else None
        fruit_x = fruit_pos.x if fruit_pos else None
        fruit_y = fruit_pos.y if fruit_pos else None
        temp_x = temp_fruit_pos.x if temp_fruit_pos else None
        temp_y = temp_fruit_pos.y if temp_fruit_pos else None
        
        cursor.execute("""
            INSERT INTO user_game_state 
            (username, level, score, snake_body, snake_direction_x, snake_direction_y, 
             fruit_pos_x, fruit_pos_y, temp_fruit_exists, temp_fruit_pos_x, temp_fruit_pos_y)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO UPDATE SET
                level = EXCLUDED.level,
                score = EXCLUDED.score,
                snake_body = EXCLUDED.snake_body,
                snake_direction_x = EXCLUDED.snake_direction_x,
                snake_direction_y = EXCLUDED.snake_direction_y,
                fruit_pos_x = EXCLUDED.fruit_pos_x,
                fruit_pos_y = EXCLUDED.fruit_pos_y,
                temp_fruit_exists = EXCLUDED.temp_fruit_exists,
                temp_fruit_pos_x = EXCLUDED.temp_fruit_pos_x,
                temp_fruit_pos_y = EXCLUDED.temp_fruit_pos_y,
                updated_at = CURRENT_TIMESTAMP
        """, (username, level, score, snake_body_str, dir_x, dir_y, fruit_x, fruit_y, temp_fruit_exists, temp_x, temp_y))
        
        connection.commit()
        print(f"Сохранено: {username}, уровень {level}, очки {score}")
        
    except Exception as e:
        print(f"Ошибка сохранения: {e}")
    finally:
        cursor.close()
        connection.close()

def delete_saved_state(username):

    connection = get_db_connection()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE user_game_state 
            SET score = 0, level = 1, snake_body = NULL, snake_direction_x = NULL,
                snake_direction_y = NULL, fruit_pos_x = NULL, fruit_pos_y = NULL,
                temp_fruit_exists = FALSE, temp_fruit_pos_x = NULL, temp_fruit_pos_y = NULL
            WHERE username = %s
        """, (username,))
        connection.commit()
        print(f"Сброшено: {username}")
    except Exception as e:
        print(f"Ошибка сброса: {e}")
    finally:
        cursor.close()
        connection.close()

def get_username_pygame():
    
    username = ""
    font = pygame.font.Font("font.ttf", 25)
    font2 = pygame.font.Font("font.ttf", 19)
    bg1 = pygame.image.load('snkend7.png')
    bg1 = pygame.transform.smoothscale(bg1,(546, 607))
    clock = pygame.time.Clock()
    while True:
        prompt = font.render("Введите имя игрока:", True, (0, 0, 0))
        user_text = font.render(username, True, (0, 0, 0))
        text1 = font2.render("Press [ENTER] to Start", True, (0, 0, 0))
        text2 = font2.render("[Q] next level", True, (0, 0, 0))
        text3 = font2.render("[R] restart", True, (0, 0, 0))

        screen.blit(bg1, (0,0))
        screen.blit(prompt, (35, 160))
        screen.blit(user_text, (180, 210))
        screen.blit(text1, (65, 480))
        screen.blit(text2, (130, 520))
        screen.blit(text3, (155, 560))
       
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip() != "":
                        return username.strip()
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    if len(username) < 12:  
                        username += event.unicode
        clock.tick(30)

def pause_menu(main_game, username, level):
    overlay = pygame.Surface((546, 607))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    font = pygame.font.SysFont("VERDANA", 40, bold=True)
    text = font.render("PAUSED", True, (255, 255, 255))
    screen.blit(text, (180, 250))
    
    font2 = pygame.font.SysFont("VERDANA", 25)
    resume_text = font2.render("Press [R] to Resume", True, (255, 255, 255))
    screen.blit(resume_text, (140, 300))
    
    pygame.display.update()
    
    if hasattr(main_game, 'save_state'):
        state = main_game.save_state()
        save_game_state(username, level, state["score"],state["snake_body"], state["snake_direction"],
            state["fruit_pos"], state["temp_fruit_exists"], state["temp_fruit_pos"]
        )
    
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False
        clock.tick(30)

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
        apple = pygame.transform.smoothscale(apple, (30, 30))
        screen.blit(apple, fruit_rect)
    

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
    def __init__(self, saved_state=None):
        if saved_state and saved_state.get("snake_body"):
           
            self.snake = SNAKE1()
            self.snake.body = [Vector2(x, y) for x, y in eval(saved_state["snake_body"])]
            self.snake.direction = saved_state["snake_direction"]
            self.fruit = FRUIT1(self.snake.body)
            if saved_state["fruit_pos"]:
                self.fruit.pos = saved_state["fruit_pos"]
            self.temp_fruit = TEMP_FRUIT1(self.snake.body)
            if saved_state["temp_fruit_exists"] and saved_state["temp_fruit_pos"]:
                self.temp_fruit.exists = True
                self.temp_fruit.pos = saved_state["temp_fruit_pos"]
                self.temp_fruit.spawn_time = time.time() - 1
           
            saved_score = saved_state.get("score", 0)
            self.score = saved_score
            print(f"Загружен уревень 1: очки {saved_score}")
        else:
          
            self.snake = SNAKE1()
            self.fruit = FRUIT1(self.snake.body)
            self.temp_fruit = TEMP_FRUIT1(self.snake.body)
            self.score = 0

    def save_state(self):
        state = {
            "snake_body": [Vector2(b.x, b.y) for b in self.snake.body],
            "snake_direction": Vector2(self.snake.direction.x, self.snake.direction.y),
            "score": self.score,
            "fruit_pos": Vector2(self.fruit.pos.x, self.fruit.pos.y),
            "temp_fruit_pos": Vector2(self.temp_fruit.pos.x, self.temp_fruit.pos.y) if self.temp_fruit.exists else None,
            "temp_fruit_exists": self.temp_fruit.exists
        }
        print(f"Сохранен уревень 1: score={self.score}")
        return state

    def draw_grass(self):
        bg = pygame.image.load('bgsnake777.png')
        bg = pygame.transform.smoothscale(bg, (546, 606))
        screen.blit(bg, (0, 0))

    def draw_score_level(self):
        font = pygame.font.SysFont("VERDANA", 28, bold=True)
        font2 = pygame.font.SysFont("VERDANA", 20, bold=True)
        score1 = font.render(f"{self.score}", True, (0, 0, 0))
        level = font2.render("Level: 1", True, (0, 0, 0))
        screen.blit(score1, (62, 22))
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
            self.score += 3 
            self.eat.play()

    def check_fail(self, username):
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
                return self.game_over(username)

    def game_over(self, username):
       
        delete_saved_state(username)
        
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
        text2 = font2.render(f"Score: {self.score}", True, (255, 255, 255))
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

    def update(self, username):
        self.draw_grass()
        self.draw_elements()
        self.snake.move_snake()
        self.check_collision()
        self.temp_fruit.check_timeout()
        self.temp_fruit.randomize(self.snake.body)
        result = self.check_fail(username)
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
        pear1 = pygame.transform.smoothscale(pear, (25, 33))
        pear2 = pygame.transform.smoothscale(pear, (28, 42))
        screen.blit(pear1, fruit_rect)
        screen.blit(pear2, (28, 14))

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
    def __init__(self, saved_state=None):
        if saved_state and saved_state.get("snake_body"):
            self.snake = SNAKE2()
            self.snake.body = [Vector2(x, y) for x, y in eval(saved_state["snake_body"])]
            self.snake.direction = saved_state["snake_direction"]
            self.fruit = FRUIT2(self.snake.body)
            if saved_state["fruit_pos"]:
                self.fruit.pos = saved_state["fruit_pos"]
            self.temp_fruit = TEMP_FRUIT2(self.snake.body)
            if saved_state["temp_fruit_exists"] and saved_state["temp_fruit_pos"]:
                self.temp_fruit.exists = True
                self.temp_fruit.pos = saved_state["temp_fruit_pos"]
                self.temp_fruit.spawn_time = time.time() - 1
         
            saved_score = saved_state.get("score", 0)
            self.score = saved_score
            print(f"Загружен уревень 2: очки {saved_score}")
        else:
            self.snake = SNAKE2()
            self.fruit = FRUIT2(self.snake.body)
            self.temp_fruit = TEMP_FRUIT2(self.snake.body)
            self.score = 0

    def save_state(self):
        state = {
            "snake_body": [Vector2(b.x, b.y) for b in self.snake.body],
            "snake_direction": Vector2(self.snake.direction.x, self.snake.direction.y),
            "score": self.score,
            "fruit_pos": Vector2(self.fruit.pos.x, self.fruit.pos.y),
            "temp_fruit_pos": Vector2(self.temp_fruit.pos.x, self.temp_fruit.pos.y) if self.temp_fruit.exists else None,
            "temp_fruit_exists": self.temp_fruit.exists
        }
        print(f"Сохранен уревень 2: score={self.score}")
        return state

    def draw_grass(self):
        bg = pygame.image.load('bgsnake888.png')
        bg = pygame.transform.smoothscale(bg, (546, 606))
        screen.blit(bg, (0, 0))

    def draw_score_level(self):
        font = pygame.font.SysFont("VERDANA", 28, bold=True)
        font2 = pygame.font.SysFont("VERDANA", 20, bold=True)
        score1 = font.render(f"{self.score}", True, (0, 0, 0))
        level = font2.render("Level: 2", True, (0, 0, 0))
        screen.blit(score1, (62, 22))
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
            self.score += 3 
            self.eat.play()

    def check_fail(self, username):
        if not 0 <= self.snake.body[0].x < cell_n or not 0 <= self.snake.body[0].y < cell_n:
            self.gmovr.play()
            return self.game_over(username)
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gmovr.play()
                return self.game_over(username)

    def game_over(self, username):
      
        delete_saved_state(username)
        
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
        text2 = font2.render(f"Score: {self.score}", True, (255, 255, 255))
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

    def update(self, username):
        self.draw_grass()
        self.draw_elements()
        self.snake.move_snake()
        self.check_collision()
        self.temp_fruit.check_timeout()  
        self.temp_fruit.randomize(self.snake.body)
        result = self.check_fail(username)
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
        blue1 = pygame.transform.smoothscale(blue, (33, 33))
        blue2 = pygame.transform.smoothscale(blue, (44, 44))
        screen.blit(blue1, fruit_rect)
        screen.blit(blue2, (20, 17))

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
        self.image = pygame.image.load('mand.png')  
        self.image = pygame.transform.smoothscale(self.image, (30, 30))
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
    def __init__(self, saved_state=None):
        if saved_state and saved_state.get("snake_body"):
            self.snake = SNAKE3()
            self.snake.body = [Vector2(x, y) for x, y in eval(saved_state["snake_body"])]
            self.snake.direction = saved_state["snake_direction"]
            self.fruit = FRUIT3(self.snake.body)
            if saved_state["fruit_pos"]:
                self.fruit.pos = saved_state["fruit_pos"]
            self.temp_fruit = TEMP_FRUIT3(self.snake.body)
            if saved_state["temp_fruit_exists"] and saved_state["temp_fruit_pos"]:
                self.temp_fruit.exists = True
                self.temp_fruit.pos = saved_state["temp_fruit_pos"]
                self.temp_fruit.spawn_time = time.time() - 1
          
            saved_score = saved_state.get("score", 0)
            self.score = saved_score
            self.border = BORDER(self.snake.body, self.fruit.pos)
            print(f"Загружен уревень 3: очки {saved_score}")
        else:
            self.snake = SNAKE3()
            self.fruit = FRUIT3(self.snake.body)
            self.temp_fruit = TEMP_FRUIT3(self.snake.body)
            self.border = BORDER(self.snake.body, self.fruit.pos)
            self.score = 0

    def save_state(self):
        state = {
            "snake_body": [Vector2(b.x, b.y) for b in self.snake.body],
            "snake_direction": Vector2(self.snake.direction.x, self.snake.direction.y),
            "score": self.score,
            "fruit_pos": Vector2(self.fruit.pos.x, self.fruit.pos.y),
            "temp_fruit_pos": Vector2(self.temp_fruit.pos.x, self.temp_fruit.pos.y) if self.temp_fruit.exists else None,
            "temp_fruit_exists": self.temp_fruit.exists
        }
        print(f"Сохранен уревень 3: score={self.score}")
        return state

    def draw_grass(self):
        bg = pygame.image.load('bgsnake999.png')
        bg = pygame.transform.smoothscale(bg, (546, 606))
        screen.blit(bg, (0, 0))

    def draw_score_level(self):
        font = pygame.font.SysFont("VERDANA", 28, bold=True)
        font2 = pygame.font.SysFont("VERDANA", 20, bold=True)
        score1 = font.render(f"{self.score}", True, (0, 0, 0))
        level = font2.render("Level: 3", True, (0, 0, 0))
        screen.blit(score1, (62, 22))
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
            self.score += 3 
            self.eat.play()

    def check_fail(self, username):
        if not 0 <= self.snake.body[0].x < cell_n or not 0 <= self.snake.body[0].y < cell_n:
            self.gmovr.play()
            return self.game_over(username)
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gmovr.play()
                return self.game_over(username)
        for wall in self.border.blocks:
            if wall == self.snake.body[0]:
                self.gmovr.play()
                return self.game_over(username)

    def game_over(self, username):
        delete_saved_state(username)
        
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
        text2 = font2.render(f"Score: {self.score}", True, (255, 255, 255))
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

    def update(self, username):
        self.draw_grass()
        self.draw_elements()
        self.snake.move_snake()
        self.check_collision()
        self.temp_fruit.check_timeout()  
        self.temp_fruit.randomize(self.snake.body)
        result = self.check_fail(username)
        return result

def scane1(username, saved_state=None):
    main_game = MAIN1(saved_state)
    main_game.sounds()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == SCREEN_UPDATE:
                result = main_game.update(username)
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
                    
                    state = main_game.save_state()
                    save_game_state(username, 2, state["score"],state["snake_body"], state["snake_direction"],
                        state["fruit_pos"], state["temp_fruit_exists"], state["temp_fruit_pos"]
                    )
                    return "scene2"
                if e.key == pygame.K_p:
                    pause_menu(main_game, username, 1)
        pygame.display.update()
        clock.tick(60)

def scane2(username, saved_state=None):
    main_game = MAIN2(saved_state)
    main_game.sounds()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == SCREEN_UPDATE2:
                result = main_game.update(username)
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
                    state = main_game.save_state()
                    save_game_state(username, 3, state["score"],state["snake_body"], state["snake_direction"],
                        state["fruit_pos"], state["temp_fruit_exists"], state["temp_fruit_pos"]
                    )
                    return "scene3"
                if e.key == pygame.K_p:
                    pause_menu(main_game, username, 2)
        pygame.display.update()
        clock.tick(60)
        
def scane3(username, saved_state=None):
    main_game = MAIN3(saved_state)
    main_game.sounds()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == SCREEN_UPDATE3:
                result = main_game.update(username)
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
                    state = main_game.save_state()
                    save_game_state(username, 1, state["score"],state["snake_body"], state["snake_direction"],
                        state["fruit_pos"], state["temp_fruit_exists"], state["temp_fruit_pos"]
                    )
                    return "scene1"
                if e.key == pygame.K_p:
                    pause_menu(main_game, username, 3)
        pygame.display.update()
        clock.tick(60)

def run_game():
    username = get_username_pygame()
    score, level, saved_state = get_or_create_user(username)
    
    print(f"Начало игры: {username}, уровень: {level}, очки: {score}")
    if level == 1:
        current_scene = "scene1"
    elif level == 2:
        current_scene = "scene2" 
    elif level == 3:
        current_scene = "scene3"
    else:
        current_scene = "scene1"
    
    while True:
        if current_scene == "scene1":
            current_scene = scane1(username, saved_state)
            saved_state = None  
        elif current_scene == "scene2":
            current_scene = scane2(username, saved_state)
            saved_state = None
        elif current_scene == "scene3":
            current_scene = scane3(username, saved_state)
            saved_state = None

run_game()