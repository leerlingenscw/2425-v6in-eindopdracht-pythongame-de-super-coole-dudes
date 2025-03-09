import pygame
import random
import time


pygame.init()



SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TANK_WIDTH = 100
TANK_HEIGHT = 80
tank_x = SCREEN_WIDTH / 2
tank_y = 650
BULLET_WIDTH = 10
BULLET_HEIGHT = 20
ENEMY_WIDTH = 100
ENEMY_HEIGHT = 80
BOMB_WIDTH = 15
BOMB_HEIGHT = 25
EXPLOSION_TIJD = 0.25
MAX_KOGELS = 4
FPS = 60
TANK_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 3
BOMB_SPEED = 5
GAME_DURATION = 600
score = 0
remaining_levens = 3
max_kogels_timer = 0  
originele_max_kogels = MAX_KOGELS  

bullets = []
explosions = []
enemies = []
enemy_speeds = []
bombs = []
powerups = []

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
background = pygame.image.load('background.png').convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
tank_img = pygame.image.load('tank.png').convert_alpha()
tank_img = pygame.transform.scale(tank_img, (TANK_WIDTH, TANK_HEIGHT))
enemy_img = pygame.image.load('enemy.png').convert_alpha()
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
bullet_img = pygame.image.load('bullet.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))
bomb_img = pygame.image.load('bomb.png').convert_alpha()
bomb_img = pygame.transform.scale(bomb_img, (BOMB_WIDTH, BOMB_HEIGHT))
explosion_frames = [pygame.image.load(f'explosion{i}.png') for i in range(1, 6)]
game_over_img = pygame.image.load('game_over.png').convert_alpha()  # Game Over image
game_over_img = pygame.transform.scale(game_over_img, (SCREEN_WIDTH, SCREEN_HEIGHT)) 

# Power-up afbeeldingen en schaling naar 50x50
powerup_images = {
    "speed": pygame.transform.scale(pygame.image.load('faster_bullets.png').convert_alpha(), (50, 50)),
    "invincible": pygame.transform.scale(pygame.image.load('invincible.png').convert_alpha(), (50, 50)),
    "more_bullets": pygame.transform.scale(pygame.image.load('extra_bullet.png').convert_alpha(), (50, 50)),
    "extra_life": pygame.transform.scale(pygame.image.load('plus_one_life.png').convert_alpha(), (50, 50))
}

font = pygame.font.Font(None, 36)

fps_clock = pygame.time.Clock()
start_time = time.time()

def add_enemy():
    enemies.append(pygame.Rect(random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH), 20, ENEMY_WIDTH, ENEMY_HEIGHT))
    enemy_speeds.append(random.choice([-ENEMY_SPEED, ENEMY_SPEED]))

def drop_bombs():
    for enemy in enemies:
        if random.random() < 0.6:  
            bombs.append(pygame.Rect(enemy.x + ENEMY_WIDTH // 2 - BOMB_WIDTH // 2, enemy.y + ENEMY_HEIGHT, BOMB_WIDTH, BOMB_HEIGHT))

def create_powerup(x, y):
    powerup_type = random.choice(["speed", "invincible", "more_bullets", "extra_life"])
    powerups.append({"type": powerup_type, "rect": pygame.Rect(x, y, 50, 50), "image": powerup_images[powerup_type]})

def handle_powerups():
    global BULLET_SPEED, TANK_SPEED, MAX_KOGELS, remaining_levens
    for powerup in powerups[:]:
        if powerup["rect"].colliderect(pygame.Rect(tank_x, tank_y, TANK_WIDTH, TANK_HEIGHT)):
            if powerup["type"] == "speed":
                BULLET_SPEED += 2
            elif powerup["type"] == "invincible":
                global invincible_timer
                invincible_timer = time.time() + 10  
            elif powerup["type"] == "more_bullets":
                MAX_KOGELS += 2 
                max_kogels_timer = time.time() + 10  
            elif powerup["type"] == "extra_life":
                remaining_levens += 1
            powerups.remove(powerup)

def check_for_powerups():
    if random.random() < 0.1:  
        create_powerup(random.randint(0, SCREEN_WIDTH - 50), 0) 

def show_death_screen():
    
    screen.fill((0, 0, 0))  
    screen.blit(game_over_img, (0, 0))  
    pygame.display.flip()

add_enemy()

drop_bomb_time = time.time()
invincible_timer = 0  

running = True
while running:
    elapsed_time = time.time() - start_time
    remaining_time = max(0, GAME_DURATION - int(elapsed_time))

    if remaining_time == 0 or remaining_levens <= 0:
        if remaining_levens <= 0:
            waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_restart = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  
                       
                        tank_x = SCREEN_WIDTH / 2
                        tank_y = 650
                        bullets.clear()
                        bombs.clear()
                        explosions.clear()
                        enemies.clear()
                        enemy_speeds.clear()
                        powerups.clear()
                        MAX_KOGELS = originele_max_kogels
                        remaining_levens = 3
                        score = 0
                        start_time = time.time()
                        waiting_for_restart = False
        continue

    expected_enemies = (600 - remaining_time) // 45 + 1
    while len(enemies) < expected_enemies:
        add_enemy()
    
    if time.time() - drop_bomb_time > 2:
        drop_bombs()
        drop_bomb_time = time.time()
    
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
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

    if max_kogels_timer > 0 and time.time() > max_kogels_timer:
        MAX_KOGELS = originele_max_kogels  
        max_kogels_timer = 0  

    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)
        else:
            for i, enemy in enumerate(enemies[:] ):
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    explosions.append([enemy.x, enemy.y, time.time(), 0])
                    del enemies[i]
                    del enemy_speeds[i]
                    score += 1  
                    check_for_powerups()  
                    
                    break
    
    for i, enemy in enumerate(enemies[:] ):
        enemy.x += enemy_speeds[i]
        if enemy.x < 0 or enemy.x + ENEMY_WIDTH > SCREEN_WIDTH:
            enemy_speeds[i] *= -1
    
    for bomb in bombs[:]:
        bomb.y += BOMB_SPEED
        if bomb.y > SCREEN_HEIGHT:
            bombs.remove(bomb)
        elif bomb.colliderect(pygame.Rect(tank_x, tank_y, TANK_WIDTH, TANK_HEIGHT)):
            explosions.append([tank_x, tank_y, time.time(), 0])
            bombs.remove(bomb)
            remaining_levens -= 1
    
    for explosion in explosions[:]:
        if time.time() - explosion[2] > EXPLOSION_TIJD:
            explosions.remove(explosion)
        else:
            explosion[3] = min(4, int((time.time() - explosion[2]) * 5))
    
  
    for powerup in powerups[:]:
        powerup["rect"].y += 3  
        if powerup["rect"].y > SCREEN_HEIGHT:
            powerups.remove(powerup) 
        else:
            screen.blit(powerup["image"], (powerup["rect"].x, powerup["rect"].y))

    handle_powerups()  

    screen.blit(tank_img, (tank_x, tank_y))
    for enemy in enemies:
        screen.blit(enemy_img, (enemy.x, enemy.y))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x, bullet.y))
    for bomb in bombs:
        screen.blit(bomb_img, (bomb.x, bomb.y))
    for explosion in explosions:
        screen.blit(explosion_frames[explosion[3]], (explosion[0], explosion[1]))
    
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    time_text = font.render(f"Tijd: {remaining_time}s", True, (255, 255, 255))
    levens_text = font.render(f"Levens: {remaining_levens}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (10, 50))
    screen.blit(levens_text, (10, 90))
    
    pygame.display.flip()
    fps_clock.tick(FPS)

pygame.quit()
