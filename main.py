import pygame
import math
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

score = 0 
FPS = 60
TANK_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 3

# Posities
tank_x = SCREEN_WIDTH / 2 
tank_y = 650
bullets = [] 
enemy_x = 0
enemy_y = 20
ball_speed_x = ENEMY_SPEED

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


# defenities van zooi






fps_clock = pygame.time.Clock()

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    
    
    # Event verwerking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Schieten met spatiebalk
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
            bullets.remove(bullet)  # Kogel verwijderen als deze uit beeld gaat
    
    # Vijand updaten
    enemy_x += ball_speed_x
    if enemy_x < 0 or enemy_x + ENEMY_WIDTH > SCREEN_WIDTH:
        ball_speed_x *= -1
    
    # Tekenen
    screen.blit(tank_img, (tank_x, tank_y))
    screen.blit(enemy_img, (enemy_x, enemy_y))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet.x, bullet.y))

 




    
    pygame.display.flip()
    fps_clock.tick(FPS)

pygame.quit()
