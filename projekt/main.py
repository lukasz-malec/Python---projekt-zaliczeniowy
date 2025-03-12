import pygame
import copy
from board import boards
import time
import drawings
import player
from ghost import Ghost
from constants import *

pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60

font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(boards)
color = 'blue'


pygame.mixer.init()
dead_ghost_sound = pygame.mixer.Sound("sounds/dead_ghost.mp3")

player_speed = 2
score = 0
max_score = 2620
lives = 1


player_images = pygame.transform.scale(pygame.image.load(f'images/pacman.png'), (25, 25))
red_img = pygame.transform.scale(pygame.image.load(f'images/red.png'), (25, 25))
pink_img = pygame.transform.scale(pygame.image.load(f'images/pink.png'), (25, 25))
blue_img = pygame.transform.scale(pygame.image.load(f'images/blue.png'), (25, 25))
spooked_img = pygame.transform.scale(pygame.image.load(f'images/powerup.png'), (25, 25))
dead_img = pygame.transform.scale(pygame.image.load(f'images/dead.png'), (25, 25))


direction_command = 0
turns_allowed = [False,False, False, False]
powerup = False
power_counter = 0
eaten_ghost = [False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y)]

red_dead = False
blue_dead = False
pink_dead = False
red_box = False
blue_box = False
pink_box = False

ghost_speeds = [2, 2, 2]
eaten_ghost_counter = 0



#  cele śledzenie duszków
def get_targets(red_x, red_y, blue_x, blue_y, pink_x, pink_y):
    runaway_x = 580 if player_x < 450 else 0
    runaway_y = 580 if player_y < 450 else 0
    return_target = (260, 270)
    scatter_targets = [(runaway_x, runaway_y), (300, 300), (10, 10)]
    ghosts = [(red, red_x, red_y, 0), (blue, blue_x, blue_y, 1), (pink, pink_x, pink_y, 2)]
    home_area = (235, 340, 245, 290)
    chase_target = (360, 310)
    
    targets = []
    for ghost, x, y, idx in ghosts:
        if powerup:
            target = scatter_targets[idx] if not ghost.dead else return_target if eaten_ghost[idx] else (player_x, player_y)
        else:
            in_home = home_area[0] < x < home_area[1] and home_area[2] < y < home_area[3]
            target = return_target if ghost.dead else chase_target if in_home else (player_x, player_y)
        targets.append(target)
    
    return targets




run = True
while run:
    timer.tick(fps)
    screen.fill('black')

    center_x = player_x + 13
    center_y = player_y + 13
    player_hitbox = pygame.draw.circle(screen, "orange", (center_x, center_y), 17, 3)

    drawings.draw_board(level, screen, color, cell_height, cell_width)
    drawings.text(font, score, screen, eaten_ghost_counter)
    player.change_direction(direction, screen, player_images, player_x, player_y, RIGHT, LEFT, UP, DOWN)

     
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False]


    red = Ghost(red_x, red_y, targets[0], ghost_speeds[0], red_img, red_direction, red_dead, red_box, 0, powerup, eaten_ghost, level, screen, spooked_img, dead_img, cell_height, cell_width) 

    blue = Ghost(blue_x, blue_y, targets[1], ghost_speeds[1], blue_img, blue_direction, blue_dead, blue_box, 1,powerup, eaten_ghost, level, screen, spooked_img, dead_img, cell_height, cell_width)
    
    pink = Ghost(pink_x, pink_y, targets[2], ghost_speeds[2], pink_img, pink_direction, pink_dead,
                   pink_box, 2, powerup, eaten_ghost, level, screen, spooked_img, dead_img, cell_height, cell_width)
    

    turns_allowed = player.check_position(center_x, center_y, cell_height, cell_width, direction, level)
    targets = get_targets(red_x, red_y, blue_x, blue_y, pink_x, pink_y)


    player_x, player_y = player.move_player(player_x, player_y, direction, turns_allowed, player_speed, RIGHT, LEFT, UP, DOWN)
    red_x, red_y, red_direction = red.move_ghost()
    blue_x, blue_y, blue_direction = blue.move_ghost()
    pink_x, pink_y, pink_direction = pink.move_ghost()



    
    score, powerup, power_counter, eaten_ghost = player.check_collisions(score, powerup, power_counter, eaten_ghost,cell_height, cell_width, center_x, center_y, player_x, level)

    ghosts = [(red, 0), (blue, 1), (pink, 2)]


    #  pacman uderzył w duszka, koniec gry 
    #  else pacman połyka duszka   
    if not powerup:
        if any(player_hitbox.colliderect(ghost.rect) and not ghost.dead for ghost, _ in ghosts):
            lives = 0       
    else:
        for ghost, index in ghosts:                   
            if player_hitbox.colliderect(ghost.rect) and not ghost.dead and not eaten_ghost[index]:
                eaten_ghost[index] = True
                eaten_ghost_counter += 1
                dead_ghost_sound.play()

                if index == 0:
                    red_dead = True
                elif index == 1:
                    blue_dead = True
                elif index == 2:
                    pink_dead = True


    #  obsługa klawiszy
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = RIGHT
            if event.key == pygame.K_LEFT:
                direction_command = LEFT
            if event.key == pygame.K_UP:
                direction_command = UP
            if event.key == pygame.K_DOWN:
                direction_command = DOWN

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == RIGHT:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == LEFT:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == UP:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == DOWN:
                direction_command = direction

    if direction_command == RIGHT and turns_allowed[0]:
        direction = RIGHT
    if direction_command == LEFT and turns_allowed[1]:
        direction = LEFT
    if direction_command == UP and turns_allowed[2]:
        direction = UP
    if direction_command == DOWN and turns_allowed[3]:
        direction = DOWN



    #  teleportacja gracza
    if player_x > 575:
        player_x = 30
    elif player_x < 30:
        player_x = 570

    if red.in_box and red_dead:
        red_dead = False
    if blue.in_box and blue_dead:
        blue_dead = False
    if pink.in_box and pink_dead:
        pink_dead = False


    #  wygrana w przypadku połknięcia wszystkich małych i dużych kropek, poczekaj 2 sekudny przed zakmnięciem programu
    if score == max_score:
        screen.fill('black')
        game_over_text = font.render(f"Wygrałes :)", True, "white")
        screen.blit(game_over_text, (100, 300))
        pygame.display.flip()
        time.sleep(2)
        run = False


    #  porażka w przypadku kolizji z duszkiem,poczekaj 2 sekudny przed zakmnięciem programu
    elif lives == 0:
        screen.fill('black')
        game_over_text = font.render(f"Porazka", True, "white")
        screen.blit(game_over_text, (100, 300))
        pygame.display.flip()
        time.sleep(2)
        run = False


    pygame.display.flip()

  

pygame.quit()
