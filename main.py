#
# BREAKOUT GAME 
#

import pygame, time

#
# definitions 
#

FPS = 60 # Frames Per Second
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TANK_WIDTH = 300
TANK_HEIGHT = 200

ball_x = 0
ball_speed_x = 6
tank_x = SCREEN_WIDTH / 2 
tank_y = SCREEN_HEIGHT = 215

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
    ball_x = ball_x + ball_speed_x

    # bounce ball
    if ball_x < 0 : 
      ball_speed_x = abs(ball_speed_x) 
    if ball_x + TANK_WIDTH > SCREEN_WIDTH: 
      ball_speed_x = abs(ball_speed_x) * -1 

    # 
    # handle collisions
    #
    
    # 
    # draw everything
    #

    # clear screen
    screen.fill('black') 

    # draw ball
    screen.blit(tank_img, (tank_x,tank_y))
    # show screen
    pygame.display.flip() 

    
    # wait until next frame
    #

    fps_clock.tick(FPS) # Sleep the remaining time of this frame

print('mygame stopt running')
