import pygame

def move_player(play_x, play_y, direction, turns_allowed, player_speed, RIGHT, LEFT, UP, DOWN):
    if direction == RIGHT and turns_allowed[0]:
        play_x += player_speed
    elif direction == LEFT and turns_allowed[1]:
        play_x -= player_speed
    if direction == UP and turns_allowed[2]:
        play_y -= player_speed
    elif direction == DOWN and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y



def change_direction(direction, screen, player_images, player_x, player_y, RIGTH, LEFT, UP, DOWN):

    if direction == RIGTH:
        screen.blit(player_images, (player_x, player_y))
    elif direction == LEFT:
        screen.blit(pygame.transform.flip(player_images, True, False), (player_x, player_y))
    elif direction == UP:
        screen.blit(pygame.transform.rotate(player_images, 90), (player_x, player_y))
    elif direction == DOWN:
        screen.blit(pygame.transform.rotate(player_images, 270), (player_x, player_y))



def check_collisions(scor, power, power_count, eaten_ghosts,num1, num2, center_x, center_y, player_x, level ):

    pygame.mixer.init()
    
    points_sound = pygame.mixer.Sound("sounds/points.mp3")
    power_up_sound = pygame.mixer.Sound("sounds/powerup.mp3")
    

    if 0 < player_x < 570:
        #  zwykłe punkty
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
            points_sound.play() 
        
        #  powerup
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
            power_up_sound.play()
    return scor, power, power_count, eaten_ghosts



def check_position(centerx, centery, cell_height, cell_width, direction, level):
    turns = [False] * 4
    korekta = 11
    grid_x, grid_y = centerx // cell_width, centery // cell_height

    if centerx // 30 >= 29:
        return [True, True, False, False]  

    # Sprawdzanie kolizji dla podstawowych kierunków
    offsets = [(-korekta, 0, 1), (korekta, 0, 0), (0, korekta, 3), (0, -korekta, 2)]
    for dx, dy, idx in offsets:
        if direction == idx and level[(centery + dy) // cell_height][(centerx + dx) // cell_width] < 3:
            turns[idx] = True

    

    if direction in {2, 3}:  # Ruch góra/dół
        if 8 <= centerx % cell_width <= 12:
            turns[3] |= level[(centery + korekta) // cell_height][grid_x] < 3
            turns[2] |= level[(centery - korekta) // cell_height][grid_x] < 3
        if 8 <= centery % cell_height <= 12:
            turns[1] |= level[grid_y][(centerx - cell_width) // cell_width] < 3
            turns[0] |= level[grid_y][(centerx + cell_width) // cell_width] < 3


    if direction in {0, 1}:  # Ruch lewo/prawo
        if 8 <= centerx % cell_width <= 12:
            turns[3] |= level[(centery + cell_height) // cell_height][grid_x] < 3
            turns[2] |= level[(centery - cell_height) // cell_height][grid_x] < 3
        if 8 <= centery % cell_height <= 12:
            turns[1] |= level[grid_y][(centerx - korekta) // cell_width] < 3
            turns[0] |= level[grid_y][(centerx + korekta) // cell_width] < 3

    return turns
