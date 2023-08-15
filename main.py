#importing pygame
import pygame
from sys import exit
from random import randint

def scoreboard():
    score=0
    curr_time=pygame.time.get_ticks()- start_time
    curr_time_secs = int(curr_time/1000)

    print(curr_time_secs)
    surf_score=text_font.render(("score: "+str(curr_time_secs)),False,"black")
    rect_score=surf_score.get_rect(center = (400,25))
    screen.blit(surf_score,rect_score)
#Obstacle movement
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle.x-=5
            if obstacle.bottom == 300: screen.blit(surf_snail,obstacle)
            else: screen.blit(surf_fly,obstacle)

        obstacle_list = [ obstacle for obstacle in obstacle_list if obstacle.x >= -100]
        return obstacle_list
    else:
        return []
def collisions(player, obstacle_list):
    global game_active
    for obstacle in obstacle_list:
        if obstacle.colliderect(player): return False
    return True
def player_movement():
    global player_surf,player_index
    if rect_player.bottom==300:
        player_index=player_index+0.1
        if player_index>=len(player_walk_list):player_index=0
        player_surf=player_walk_list[int(player_index)]


#initialize pygame
pygame.init()
start_time=0
screen = pygame.display.set_mode((800,400))
title= pygame.display.set_caption("ruin run")
clock= pygame.time.Clock()
text_font= pygame.font.Font("font/Pixeltype.ttf",50)

#creatinng_surfaces_and_rectangles
#intro screen
surf_intro=pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
surf_intro=pygame.transform.rotozoom(surf_intro,0,1.5)
rect_intro=surf_intro.get_rect(center=(400,200))
surf_intro_text=text_font.render("Game Over",False,(111,196,169))
surf_intro_text2=text_font.render("Please press a key to continue!",False,(111,196,169))
rect_intro_text=surf_intro_text.get_rect(midbottom=(400,100))
rect_intro_text2=surf_intro_text.get_rect(bottomright=(350,325))
surf_player=pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
#player_rectangle
player_walk1_surf=pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk2_surf=pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk_list=[player_walk1_surf,player_walk2_surf]
player_index=0
player_surf=player_walk_list[player_index]
rect_player=player_surf.get_rect(bottomleft=(50,300))
surf_sky= pygame.image.load("graphics\Sky.png").convert_alpha()
surf_ground= pygame.image.load("graphics/ground.png").convert_alpha()
surf_snail=pygame.image.load("graphics/snail/snail1.png").convert_alpha()
surf_fly= pygame.image.load("graphics/Fly/fly1.png").convert_alpha()

#snail_rectangle
player_gravity=0
game_active=True
#custom event
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,2000 )
obstacle_rect_list=[]
#While true(game-screen-updates-here)
while True:


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit()

        if game_active:
            mouse= event.type == pygame.MOUSEMOTION
            if mouse:
                if rect_player.collidepoint(event.pos):
                    print("collide")
            if rect_player.bottom == 300:
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_UP:
                        player_gravity=-18
            if event.type==pygame.MOUSEBUTTONDOWN:
                if rect_player.collidepoint(event.pos):
                    player_gravity=-15
        else:
            if game_active==False:
                start_time = pygame.time.get_ticks()
                if event.type==pygame.KEYDOWN:
                    game_active=True
                    start_time=pygame.time.get_ticks()
        if event.type==obstacle_timer:
            if randint(0,2):
                obstacle_rect_list.append(surf_snail.get_rect(bottomright=(randint(900,1300), 300)))
            else:
                obstacle_rect_list.append(surf_fly.get_rect(bottomright=(randint(900, 1300), 150)))


    if game_active:
        collisions(rect_player,obstacle_rect_list)

    #Screen Blit
        screen.blit(surf_sky,(0,0))
        screen.blit(surf_ground,(0,300))
        scoreboard()
        player_gravity+=1
        rect_player.top=rect_player.top+player_gravity
        if rect_player.bottom>=300:
            rect_player.bottom=300

        player_movement()
        screen.blit(player_surf,rect_player)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)



        if not collisions(rect_player,obstacle_rect_list):
            obstacle_rect_list.clear()
            rect_player.bottomleft=(50,300)
            game_active=False
            screen.fill("light blue")
            print("Game Over\nContinue?")
            screen.blit(surf_intro,rect_intro)
            screen.blit(surf_intro_text,rect_intro_text)
            screen.blit(surf_intro_text2, rect_intro_text2)

    pygame.display.update()
    clock.tick(60)