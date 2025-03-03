import pygame
import math
import random
import time

# Initialisatie
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TANK_WIDTH = 100
TANK_HEIGHT = 80
BULLET_WIDTH = 10
BULLET_HEIGHT = 20
ENEMY_WIDTH = 100
ENEMY_HEIGHT = 80
EXPLOSION_HEIGHT = 75
EXPLOSION_WIDTH = 75 
EXPLOSION_TIJD = 0.25
MAX_KOGELS = 4

score = 0 
FPS = 60
TANK_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 3
GAME_DURATION = 600  # 10 minuten in seconden

# Posities
tank_x = SCREEN_WIDTH / 2 
tank_y = 650

# Lijsten
bullets = [] 
explosions = []
enemies = []
enemy_speeds = []

# Afbeeldingen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
background = pygame.image.load('background.png').convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
tank_img = pygame.image.load('tank.png').convert_alpha()
tank_img = pygame.transform.scale(tank_img, (TANK_WIDTH, TANK_HEIGHT))
enemy_img = pygame.image.load('enemy.png').convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
bullet_img = pygame.image.load('bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))
explosion_frames = [pygame.image.load(f'explosion{i}.png') for i in range(1, 6)]

# Font voor score en tijd
font = pygame.font.Font(None, 36)

fps_clock = pygame.time.Clock()
start_time = time.time()

# Vijand toevoegen
def add_enemy():
    enemies.append(pygame.Rect(random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH), 20, ENEMY_WIDTH, ENEMY_HEIGHT))
    enemy_speeds.append(random.choice([-ENEMY_SPEED, ENEMY_SPEED]))

# Eerste vijand toevoegen
add_enemy()

# Game loop
running = True
while running:
    elapsed_time = time.time() - start_time
    remaining_time = max(0, GAME_DURATION - int(elapsed_time))
    if remaining_time == 0:
        running = False
    
    # Bereken het aantal verwachte vijanden
    expected_enemies = (600 - remaining_time) // 30 + 1
    while len(enemies) < expected_enemies:
        add_enemy()
    
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    # Event verwerking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and len(bullets) < MAX_KOGELS:
                bullets.append(pygame.Rect(tank_x + TANK_WIDTH // 2 - BULLET_WIDTH // 2, tank_y, BULLET_WIDTH, BULLET_HEIGHT))
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and tank_x < SCREEN_WIDTH - TANK_WIDTH:
        tank_x += TANK_SPEED
    if keys[pygame.K_LEFT] and tank_x > 0:
        tank_x -= TANK_SPEED
    
    # Kogels updaten
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)  
        else:
            for i, enemy in enumerate(enemies[:]):
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    explosions.append([enemy.x, enemy.y, time.time(), 0])
                    del enemies[i]
                    del enemy_speeds[i]
                    score += 1  # Score verhogen bij explosie
                    break
    
    # Zorg ervoor dat verslagen vijanden terugkeren
    while len(enemies) < expected_enemies:
        add_enemy()
    
    # Vijanden updaten
    for i, enemy in enumerate(enemies):
        enemy.x += enemy_speeds[i]
        if enemy.x < 0 or enemy.x + ENEMY_WIDTH > SCREEN_WIDTH:
            enemy_speeds[i] *= -1
    
    # Explosies
    for explosion in explosions[:]:
        if time.time() - explosion[2] > EXPLOSION_TIJD:
            explosions.remove(explosion)
        else:
            explosion[3] = min(4, int((time.time() - explosion[2]) * 5))
    
    # Tekenen
    screen.blit(tank_img, (tank_x, tank_y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x, enemy.y))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x, bullet.y))  
    for explosion in explosions:
        screen.blit(explosion_frames[explosion[3]], (explosion[0], explosion[1])) 
    
    # Score en tijd weergeven
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    time_text = font.render(f"Tijd: {remaining_time}s", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (10, 50))
    
    pygame.display.flip()
    fps_clock.tick(FPS)
    
pygame.quit()