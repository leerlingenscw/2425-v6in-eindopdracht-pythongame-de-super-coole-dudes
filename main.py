#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#
x = 640
y = 650
FPS = 60 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TANK_WIDTH = 100
TANK_HEIGHT = 80

ball_x = 0
ball_speed_x = 6
tank_x = SCREEN_WIDTH / 2 
tank_y = SCREEN_HEIGHT = 650

ENEMY_WIDTH = 100
ENEMY_HEIGHT = 80 
enemy_x = 0
enemy_y = SCREEN_HEIGHT = 20 

#
# init game
#

pygame.init()
font = pygame.font.SysFont('default', 64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
fps_clock = pygame.time.Clock()
ball_location =(600, 1)

#
# read images
#

tank_img = pygame.image.load('tank.png').convert_alpha()    
tank_img = pygame.transform.scale(tank_img, (TANK_WIDTH, TANK_HEIGHT))  
enemy_img = pygame.image.load('enemy.png').convert_alpha()    
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))  


#
# game loop
#

print('mygame is running')
running = True
while running:
    
    #
    # read events
    # 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            running = False 
    keys = pygame.key.get_pressed() 
    

    
            
    # 
    # move everything
    #

    # move ball
    if keys[pygame.K_RIGHT] and tank_x<SCREEN_WIDTH - TANK_WIDTH : tank_x += 5 
    if keys[pygame.K_LEFT] and tank_x>0: tank_x -= 5 
   
 
     
    # bounce ball
    if enemy_x < 0 :
       ball_speed_x = abs(ball_speed_x)
    if enemy_x + ENEMY_WIDTH > SCREEN_WIDTH:
      ball_speed_x = abs(ball_speed_x) * -1

    # 
    # handle collisions
    #
    enemy_x = enemy_x + ball_speed_x
    # 
    # draw everything
    #

    # clear screen
    screen.fill('black') 

    # draw ball
    screen.blit(tank_img,(tank_x,tank_y))
    screen.blit(enemy_img,(enemy_x,enemy_y))
    # show screen
    pygame.display.flip() 
    pygame.display.update()  

    
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
