import pygame

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id, powerup, eaten_ghost,level, screen, spooked_img, dead_img,cell_height, cell_width):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 13
        self.center_y = self.y_pos + 13
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions(level, cell_height, cell_width)
        self.rect = self.draw(powerup, eaten_ghost, screen,spooked_img, dead_img )

    def draw(self,powerup, eaten_ghost,screen, spooked_img, dead_img ):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))

        ghost_hitbox = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_hitbox


    def check_collisions(self, level, cell_height, cell_width):
        # Definiuje korektę pozycji, aby uniknąć błędów zaokrągleń
        korekta = 10
        
        # Resetuje możliwe kierunki ruchu (0 - prawo, 1 - lewo, 2 - góra, 3 - dół)
        self.turns = [False, False, False, False]
        
        # Sprawdza, czy obiekt znajduje się w granicach poziomu (nie na krawędzi)
        if 0 < self.center_x // 30 < 29:
            # Sprawdza, czy nad obiektem znajduje się pole typu 9 (np. brama, tunel)
            if level[(self.center_y - korekta) // cell_height][self.center_x // cell_width] == 9:
                self.turns[2] = True
            
            # Sprawdza możliwość ruchu w lewo
            if level[self.center_y // cell_height][(self.center_x - korekta) // cell_width] < 3 \
                    or (level[self.center_y // cell_height][(self.center_x - korekta) // cell_width] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            
            # Sprawdza możliwość ruchu w prawo
            if level[self.center_y // cell_height][(self.center_x + korekta) // cell_width] < 3 \
                    or (level[self.center_y // cell_height][(self.center_x + korekta) // cell_width] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            
            # Sprawdza możliwość ruchu w dół
            if level[(self.center_y + korekta) // cell_height][self.center_x // cell_width] < 3 \
                    or (level[(self.center_y + korekta) // cell_height][self.center_x // cell_width] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            
            # Sprawdza możliwość ruchu w górę
            if level[(self.center_y - korekta) // cell_height][self.center_x // cell_width] < 3 \
                    or (level[(self.center_y - korekta) // cell_height][self.center_x // cell_width] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True
            
            # Dodatkowe sprawdzenie dla ruchu w osi pionowej (kiedy porusza się w górę/dół)
            if self.direction == 2 or self.direction == 3:
                if 8 <= self.center_x % cell_width <= 12:
                    if level[(self.center_y + korekta) // cell_height][self.center_x // cell_width] < 3 \
                            or (level[(self.center_y + korekta) // cell_height][self.center_x // cell_width] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - korekta) // cell_height][self.center_x // cell_width] < 3 \
                            or (level[(self.center_y - korekta) // cell_height][self.center_x // cell_width] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 8 <= self.center_y % cell_height <= 12:
                    if level[self.center_y // cell_height][(self.center_x - cell_width) // cell_width] < 3 \
                            or (level[self.center_y // cell_height][(self.center_x - cell_width) // cell_width] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // cell_height][(self.center_x + cell_width) // cell_width] < 3 \
                            or (level[self.center_y // cell_height][(self.center_x + cell_width) // cell_width] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
            
            # Dodatkowe sprawdzenie dla ruchu w osi poziomej (kiedy porusza się w lewo/prawo)
            if self.direction == 0 or self.direction == 1:
                if 8 <= self.center_x % cell_width <= 12:
                    if level[(self.center_y + korekta) // cell_height][self.center_x // cell_width] < 3 \
                            or (level[(self.center_y + korekta) // cell_height][self.center_x // cell_width] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - korekta) // cell_height][self.center_x // cell_width] < 3 \
                            or (level[(self.center_y - korekta) // cell_height][self.center_x // cell_width] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 8 <= self.center_y % cell_height <= 12:
                    if level[self.center_y // cell_height][(self.center_x - korekta) // cell_width] < 3 \
                            or (level[self.center_y // cell_height][(self.center_x - korekta) // cell_width] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // cell_height][(self.center_x + korekta) // cell_width] < 3 \
                            or (level[self.center_y // cell_height][(self.center_x + korekta) // cell_width] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            # Jeżeli postać jest poza zakresem, umożliwia ruch w lewo i prawo
            self.turns[0] = True
            self.turns[1] = True
        
        # Sprawdza, czy postać znajduje się w wyznaczonym obszarze (np. skrzynce respawnu)
        if 235 < self.x_pos < 340 and 245 < self.y_pos < 290:
            self.in_box = True
        else:
            self.in_box = False
        
        return self.turns, self.in_box



    def move_ghost(self):
        # Sprawdzenie kierunku ducha i jego ruchu
        
        if self.direction == 0:  # Kierunek: w prawo
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed  # Poruszanie się w prawo
            elif not self.turns[0]:  # Jeśli nie można iść w prawo
                # Sprawdzenie innych możliwych kierunków
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3  # Kierunek: w dół
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2  # Kierunek: w górę
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1  # Kierunek: w lewo
                    self.x_pos -= self.speed
                # Jeżeli żaden z priorytetowych kierunków nie jest dostępny
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        
        elif self.direction == 1:  # Kierunek: w lewo
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3  # Ruch w dół
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed  # Kontynuowanie ruchu w lewo
            elif not self.turns[1]:
                # Sprawdzenie alternatywnych kierunków
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        
        elif self.direction == 2:  # Kierunek: w górę
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1  # Ruch w lewo
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2  # Kontynuowanie ruchu w górę
                self.y_pos -= self.speed
            elif not self.turns[2]:
                # Sprawdzenie innych możliwych kierunków
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        
        elif self.direction == 3:  # Kierunek: w dół
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed  # Kontynuowanie ruchu w dół
            elif not self.turns[3]:
                # Sprawdzenie innych opcji ruchu
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        
        # Obsługa teleportacji na przeciwne krańce planszy
        if self.x_pos < 30:
            self.x_pos = 575
        elif self.x_pos > 575:
            self.x_pos = 30
        
        return self.x_pos, self.y_pos, self.direction
