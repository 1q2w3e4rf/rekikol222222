import pygame
import sys
import random

pygame.init()
WHITE3 , HOHO= 500, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE2 = (255, 255, 255)
RED = (255, 0, 0)

WIDTH, HEIGHT = 800, 400
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Ezik Game')

dino_width, dino_height = 50, 50
dino_x, dino_y = 50, HEIGHT - dino_height
dino_image = pygame.image.load('1.png')
dino_image = pygame.transform.scale(dino_image, (dino_width, dino_height))
dino_image2 = pygame.image.load('2.png')
dino_image2 = pygame.transform.scale(dino_image2, (dino_width, dino_height))
jumping = False
jump_count = 10

min_distance, max_distance = 200, 1000

obstacles = []

clock = pygame.time.Clock()


fon = pygame.image.load('fon.png')
fon = pygame.transform.scale(fon, (WIDTH, HEIGHT))

def create_obstacle():
    global obstacle_image
    obstacle_types = {
        'rock': (50, 50),
        'tree': (55, 70),
        'bush': (70, 40)
    }

    obstacle_type = random.choice(list(obstacle_types.keys()))
    obstacle_width, obstacle_height = obstacle_types[obstacle_type]

    obstacle_x = WIDTH
    obstacle_y = HEIGHT - obstacle_height
    distance = random.randint(min_distance, max_distance)
    
    obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))
    
    if obstacle_type == 'rock':
        obstacle_image = 'br.png'
    elif obstacle_type == 'tree':
        obstacle_image = 'kam.png'
    elif obstacle_type == 'bush':
        obstacle_image = 'kust.png'
    
    obstacle_image = pygame.image.load(obstacle_image)
    obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))
    
    for obstacle in obstacles:
        screen.blit(obstacle_image, (obstacle.x, obstacle.y))
enemies = []

def create_enemy():
    enemy_types = {
        'bird': (50, 50),
    }
    
    enemy_type = random.choice(list(enemy_types.keys()))
    enemy_width, enemy_height = enemy_types[enemy_type]

    enemy_x = WHITE3
    enemy_y = random.randint(0,  - enemy_height)
    enemy_y = random.randint(0, enemy_height)
    distance = random.randint(min_distance, max_distance)

    if enemy_type == 'bird':
        enemy_image = 'br.png'

    enemy = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    enemies.append(enemy)

enemy_spawn_timer = pygame.time.Clock()
enemy_spawn_time = 5000
def handle_enemy_spawning():
    global enemy_spawn_timer, enemy_spawn_time
    enemy_spawn_timer.tick()
    if enemy_spawn_timer.get_time() > enemy_spawn_time:
        create_enemy()
        enemy_spawn_timer.reset()  # Сброс таймера после спавна
def check_collision():
    dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
    for obstacle in obstacles:
        if dino_rect.colliderect(obstacle):
            return True
    return False

current_image = 1
image_timer = 0
speed = 10
speed_timer = 0
speed_increment = 0.1
score = 0
win = 0
image_switch_time = 10

while True:
    screen.blit(fon, (0, 0))

    image_timer += clock.tick(FPS)
    if image_timer >= image_switch_time:
        if current_image == 1:
            screen.blit(dino_image2, (dino_x, dino_y))
            current_image = 2
        else:
            screen.blit(dino_image, (dino_x, dino_y))
            current_image = 1
        image_timer = 0

    speed_timer += clock.tick(FPS)
    if speed_timer >= 1000:
        speed += speed_increment
        if speed > 25:
            speed = 25
        speed_timer = 0

    if speed > 10:
        score += 0.2 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not jumping:
                jumping = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not jumping:
                jumping = True

    keys = pygame.key.get_pressed()
    if not jumping:
        if keys[pygame.K_SPACE]:
            jumping = True
    else:
        if jump_count >= -10:
            dino_y -= (jump_count * abs(jump_count)) * 0.4
            jump_count -= 1
        else:
            jump_count = 10
            jumping = False

    if len(obstacles) == 0 or obstacles[-1].x < WIDTH - max_distance:
        create_obstacle()

    for obstacle in obstacles:
        obstacle.x -= speed * 1.5
        screen.blit(obstacle_image, (obstacle.x, obstacle.y))


    if check_collision():
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, RED)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)   

        speed = 10
        speed_timer = 0
        score = 0
        jumping = False
        jump_count = 10
        obstacles = []
        dino_x, dino_y = 50, HEIGHT - dino_height     
        win = 0
    
        create_obstacle()

    font = pygame.font.Font(None, 36)
    text_score = font.render(f"Score: {int(score)}", True, RED)
    screen.blit(text_score, (10, 30))

    font = pygame.font.Font(None, 36)
    text_score = font.render(f"Win: {int(win)}", True, RED)
    screen.blit(text_score, (10, 10))

    font = pygame.font.Font(None, 36)
    text_score = font.render(f"Speed: {int(speed)}", True, RED)
    screen.blit(text_score, (10, 60))

    if score >= 1000:
        font = pygame.font.Font(None, 36)
        text_speed = font.render("You Win", True, RED)
        text_rect = text_speed.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text_speed, text_rect)
        win += 1
        pygame.display.flip()
        pygame.time.delay(2000)

        speed = 10
        speed_timer = 0
        score = 0
        jumping = False
        jump_count = 10
        obstacles = []
        dino_x, dino_y = 50, HEIGHT - dino_height

        create_obstacle()
    
    
    pygame.display.flip()

