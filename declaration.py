
import pygame
import random
import numpy as np

# simulation specification
epoch_max = 70000
gamma = 0.95


# simulation reward
reward_goal = 100
reward_preferred = 50
reward_crossable = -20
reward_nothing = 0
reward_init = -30

# the cell to display Q values
cell_under_mouse = None

# This is a list of every sprite. For Blocks, Preferred, Start and End
all_sprites_list  = pygame.sprite.Group()

# 3  lists to manage all objects /graphics
block_list       = []
preferred_list   = []
crossable_list   = []
start_list       = []
end_list         = []

# start and end position on the grid, those are graphics objects, no information on grid rank
cell_start = None
cell_end = None

#how many col and row beyond Start and End in case filter in ON
filter_margin = 2

training_ready = False

# edges and cell List
edge_list = []
cell_list = []
steps = []
visits = []
scores = []

#initialize a Q matrix
Q = np.matrix(np.zeros([1, 1]))

# define screen size and UI size
screen_width = 1400
screen_height = 900

# the grid origin in [grid_zone_width,button_zone_high_height]
grid_margin_x = 50
button_zone_high_height = 50
button_zone_low_height = 50
button_size =50


# grid defintion / keep the grid square!
tile_size = 50 # use a number that makes sense (50,25,10..)
grid_width = 800 #do not change this or check for impact
grid_height = grid_width
col_max = grid_width  // tile_size -1
row_max = grid_height // tile_size -1


font_ratio = tile_size / 50
BLACK = (0  ,  0,  0)
WHITE = (255,255,255)

RED   = (255,  0,  0)
GREEN = (0  ,255,  0)
BLUE  = (0  ,0 , 255)

YELLOW  = (255,255,  0)
CYAN    = (0  ,255,255)
MAGENTA = (255,  0,255)

LIGHTSHADE = (170, 170, 170)
DARKSHADE = (100, 100, 100)

RUSTY = (99, 11, 27)
GREY = (126,132,140)

# mouse click index
LEFT = 1
RIGHT = 3

# initialisation of images

block_img = pygame.image.load('img/block.png')
block_obj_img = pygame.image.load('img/block_obj.png')
block_ns_img = pygame.image.load('img/block_ns.png')

start_img = pygame.image.load('img/start.png')
start_obj_img= pygame.image.load('img/start_obj.png')
start_ns_img= pygame.image.load('img/start_ns.png')

end_img = pygame.image.load('img/end.png')
end_obj_img= pygame.image.load('img/end_obj.png')
end_ns_img= pygame.image.load('img/end_ns.png')

simulation_img = pygame.image.load('img/simulation.png')
simulation_ns_img = pygame.image.load('img/simulation_ns.png')

delete_img = pygame.image.load('img/delete.png')
delete_obj_img = pygame.image.load('img/delete_obj.png')
delete_ns_img = pygame.image.load('img/delete_ns.png')

preferred_img = pygame.image.load('img/preferred.png')
preferred_obj_img = pygame.image.load('img/preferred_obj.png')
preferred_ns_img = pygame.image.load('img/preferred_ns.png')

crossable_img = pygame.image.load('img/crossable.png')
crossable_obj_img = pygame.image.load('img/crossable_obj.png')
crossable_ns_img = pygame.image.load('img/crossable_ns.png')

open_img = pygame.image.load('img/open.png')
open_ns_img = pygame.image.load('img/open_ns.png')

filter_img = pygame.image.load('img/filter.png')
filter_ns_img = pygame.image.load('img/filter_ns.png')


