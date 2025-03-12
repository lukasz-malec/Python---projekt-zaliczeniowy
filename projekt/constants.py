# Te wartości są stałe i nie powinny być zmieniane, ponieważ zostały specjalnie obliczone dla poprawnego działania programu.

WIDTH = 600
HEIGHT = 650
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

cell_height = (HEIGHT - 50) // 32
cell_width = WIDTH // 30


direction = 0
player_x = 340
player_y = 427

red_x = 37
red_y = 500
red_direction = 0

blue_x = 37
blue_y = 100
blue_direction = 0

pink_x = 500
pink_y = 100
pink_direction = 0



# współrzędne środkowej bramy z której duszki wychodzą:
# 235 - 340 na x
# 245 - 290 na y

# teleportacja ze wspolrzednych x z 10 na 575 oraz odwrotnie