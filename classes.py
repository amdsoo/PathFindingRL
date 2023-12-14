import math

from declaration import *
import declaration as d
import method as m
import pickle as pick


pygame.font.init()


# Regular font for titles and Score
# fixed fonts for score and texts
my_font = pygame.font.SysFont('Comic Sans MS', 14)
# Medium font for Cell number/depending of font_ratio
my_font_M = pygame.font.SysFont('Comic Sans MS', int(14*font_ratio))
# tiny font for cell info/depending of font_ratio
my_font_SM = pygame.font.SysFont('Comic Sans MS', int(12*font_ratio))


class World:
	def __init__(self):
		self.tile_list = []
		# load images
		grey_img = pygame.image.load('img/grey.png')
		colmax = screen_width // tile_size
		rowmax = screen_height// tile_size
		col_count = 0

		self.score = 0
		self.cycle = 0
		self.computation_time = 0
		self.nb_possible_paths = 0

		self.nb_random_choice  = 0
		self.path_value =0

		# the state of the world
		# 0 - no training yet
		# 1 - training failed, no solution
		# 2 - training ok, path displayed
		# 3 - Case could not be loaded
		self.state = 0


		'''while col_count < colmax:
			# top level
			img = pygame.transform.scale(grey_img, (button_size, button_size))
			img_rect = img.get_rect()
			img_rect.x = col_count * button_size
			img_rect.y = 0
			tile = (img, img_rect)
			self.tile_list.append(tile)

			# lowlevel
			img = pygame.transform.scale(grey_img, (button_size, button_size))
			img = pygame.transform.rotate(img, 180)
			img_rect = img.get_rect()
			img_rect.x = col_count * button_size
			img_rect.y = rowmax* button_size - button_size
			tile = (img, img_rect)
			self.tile_list.append(tile)

			col_count +=1'''

	def draw(self, screen):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])

		#Text parameters
		text_margin =50
		text_column = 150
		text_row = 20

		# create rectangle
		input_rect = pygame.Rect(0, 0, 20 * button_size, button_size)
		pygame.draw.rect(screen, GREY, input_rect)
		current_cycle = self.cycle
		if self.cycle == 0:
			current_cycle = epoch_max
		text_surface = my_font.render ("Cycle / " + str(current_cycle) , False, BLACK)
		screen.blit(text_surface, (input_rect.x + text_margin, 0))

		text_surface = my_font.render ("MaxScore / "+str(self.score), False, BLACK)
		screen.blit(text_surface, (input_rect.x + text_margin, text_row))

		# the state of the world
		# 0 - no training yet
		# 1 - training failed, no solution
		# 2 - training ok, path displayed
		# 3 - Case could not be loaded
		msg =""
		if self.state == 0:
			msg = "No training info"
		elif self.state == 1:
			msg = "Training failed"
		elif self.state == 3:
			msg = "Case could not be loaded"
		if msg !="":
			text_surface = my_font.render ( msg, False, BLACK)
			screen.blit(text_surface, (input_rect.x + text_margin + text_column, 0))

		# 2 we display path info if available
		if len (d.steps) > 0:
			text_surface = my_font.render ("Path Length/ " + str(len (d.steps)) , False, BLACK)
			screen.blit(text_surface, (input_rect.x + text_margin +text_column, 0))

			# we compute the percentage of randomness
			value = self.nb_random_choice / len (d.steps)
			text_surface = my_font.render ("Randomness / "+str(round(value *100,1)) + "%", False, BLACK)
			screen.blit(text_surface, (input_rect.x + text_margin + text_column, text_row))

			# we compute the value of the path
			total_value = 0
			i = 0
			while i < len(d.steps) - 1:
				rank_cell_1 = d.steps[i]
				rank_cell_2 = d.steps[i + 1]
				cell_1 = m.find_cell_from_rank(rank_cell_1)
				cell_2 = m.find_cell_from_rank(rank_cell_2)

				#where is cell_2 compared to cell_1 ?
				position = m.position_between_cells (cell_1, cell_2)

				#we extract the relative value from Q table
				val1 = d.Q[rank_cell_1,]
				value = round(val1[0, position])

				total_value = total_value +value
				i +=1

			text_surface = my_font.render ("Path value / "+str(round(total_value)), False, BLACK)
			screen.blit(text_surface, (input_rect.x + text_margin + text_column*2, text_row))

		text_surface = my_font.render ("Compute Time / "+str(self.computation_time) +" s", False, BLACK)
		screen.blit(text_surface, (input_rect.x + text_margin + text_column*2,0 ))

	def open(self):
		# this is the Open of an existing csv containing a predefined UC
		print ("Open the game")
		# resetting world
		# This is the list of every sprite. For Blocks, Preferred, Start and End
		d.all_sprites_list.empty()

		# This is a group to handle tmp object
		'''d.all_sprites_tmp.empty()'''

		# 3  lists to manage all objects /graphics
		d.block_list.clear()
		d.preferred_list.clear()
		d.crossable_list.clear()
		d.start_list.clear()
		d.end_list.clear()

		# start and end position on the grid, those are graphics objects, no information on grid rank
		d.cell_start = None
		d.cell_end = None

		# edges and cell List
		d.edge_list.clear()
		d.cell_list.clear()
		d.steps.clear()
		d.visits.clear()

		with open("setup/setup.txt") as file:
			lines = []
			for line in file:
				lines.append(line)
		# reading header
		j =0
		chunk = lines [j].split(",")
		# reading Grid size
		j += 1
		chunk = lines [j].split(",")
		grid_size = int(chunk[0])

		if grid_size != col_max+1:
			# we abort
			m.clear_env("depressed")
			file.close()
			self.state = 3
			return

		# reading start and end
		j += 1
		chunk = lines [j].split(",")
		# create Start
		col , row = int(chunk[0]) , int(chunk[1])
		x, y = grid_margin_x + col * tile_size, row * tile_size + button_zone_high_height
		d.cell_start = Start(x, y)
		d.all_sprites_list.add(d.cell_start)
		d.cell_start.col, d.cell_start.row = col, row

		j += 1
		chunk = lines [j].split(",")
		# create End
		col , row = int(chunk[0]) , int(chunk[1])
		x, y = grid_margin_x + col * tile_size, row * tile_size + button_zone_high_height
		d.cell_end = End(x, y)
		d.all_sprites_list.add(d.cell_end)
		d.cell_end.col, d.cell_end.row = col, row

		# Reading blocks, preferred and crossable spots
		j = 0
		i = 0
		while j <= row_max:
			# read the line (by row)
			chunk = lines[j+4].split(",")
			i = 0
			#traverse the row (by column)
			while i <= col_max:
				element = None
				x, y = i * tile_size + grid_margin_x, j * tile_size + button_zone_high_height
				if chunk [i] == "X":
					# this is a block
					element = Block(x, y)
					d.block_list.append(element)

				elif chunk [i] == "P":
					# this is a preferred spot
					element = Preferred(x, y)
					d.preferred_list.append(element)

				elif chunk [i] == "C":
					# this is a Crossable spot
					element = Crossable(x, y)
					d.crossable_list.append(element)

				if element is not None:
					d.all_sprites_list.add(element)
					element.col, element.row = i, j

				i +=1
			j +=1

		# closing
		# we clean the cell list and recompute the active cells
		m.clear_env("depressed")
		file.close()


class Grid:
	def __init__(self):
		pass

	def draw (self, screen):
		horiz  =  grid_height // tile_size +1
		vertic =  grid_width  // tile_size +1

		h, v = 0, 0

		i = 0
		for line in range(0, horiz):
			pygame.draw.line(screen, WHITE, (grid_margin_x , line * tile_size + button_zone_high_height), (grid_margin_x + grid_width, line * tile_size + button_zone_high_height))

		i = 0
		for line in range(0, vertic):
			pygame.draw.line(screen, WHITE, (grid_margin_x + line * tile_size , button_zone_high_height), (grid_margin_x + line * tile_size, grid_height + button_zone_high_height))

		# we display the cell number
		# we display cell number on the grid
		for cell in d.cell_list:
			text = str(cell.rank)
			text_surface = my_font_M.render(text, True, WHITE)
			screen.blit(text_surface, (grid_margin_x + tile_size * cell.col, tile_size * cell.row + button_zone_high_height))


		# we display a path if it exists
		i =0
		while i< len (d.steps) -1:
			rank_cell_1 = d.steps [i]
			rank_cell_2 = d.steps [i+1]
			cell_1 = m.find_cell_from_rank(rank_cell_1)
			cell_2 = m.find_cell_from_rank(rank_cell_2)
			pygame.draw.line(screen, BLACK,
			                 (grid_margin_x + cell_1.col * tile_size + tile_size / 2, cell_1.row * tile_size + tile_size / 2 + button_zone_high_height),
			                 (grid_margin_x + cell_2.col * tile_size + tile_size / 2, cell_2.row * tile_size + tile_size / 2 + button_zone_high_height), width=2)

			i = i+1

		# we display Q values for the adjacent cells
		# The Q matrix is now [State, top, left, bottom, right]
		if d.cell_under_mouse is not None :
			val1 = d.Q[d.cell_under_mouse.rank,]
			i=0
			while i<= 3:
				value =  round(val1[0 ,i])
				if value >0:
					'''print ("Value at cell #", i, " = ", value)'''
					text = str(value)
					# we retreive the cell that correspond to this rank, this time we must use the position API
					cell_tmp  = m.cell_from_position(d.cell_under_mouse, i)
					text_surface = my_font_SM.render(text, True, BLACK)
					screen.blit(text_surface, (grid_margin_x + tile_size * cell_tmp.col + tile_size // 4, tile_size * cell_tmp.row + tile_size // 4 + button_zone_high_height))
				i=i+1


	def draw_graph(self, screen):
		# we display the scores in the right side of the screen on a 400x400 graph
		# this method is not in the regular draw to be able to trigger it manually if necessary
		size = 400
		origin = (grid_margin_x *2+grid_width,screen_height//2)

		# Axis X
		point = (origin[0]+size,origin[1])
		pygame.draw.line(screen, BLACK, origin, point)
		text = "Epoch Max"
		# we retreive the cell that correspond to this rank, this time we must use the position API
		text_surface = my_font_SM.render(text, True, BLACK)
		screen.blit(text_surface, (point))

		# Axis Y
		point = (origin[0] , origin[1]-size)
		pygame.draw.line(screen, BLACK, origin, point)
		text = "Score Max"
		# we retreive the cell that correspond to this rank, this time we must use the position API
		text_surface = my_font_SM.render(text, True, BLACK)
		screen.blit(text_surface, (point))

		# vertical graduation on Axis X
		number = 10
		lenght = 10
		dx = size//number
		i = 1
		while i<=number:
			point_a = (origin[0] +dx*i, origin[1]-lenght//2)
			point_b = (origin[0] +dx*i, origin[1]+lenght//2)
			pygame.draw.line(screen, BLACK, point_a, point_b)
			i +=1

		# draw the curve
		if (len(d.scores) !=0):

			epoch_frequency = 100
			dx = size/epoch_max
			dy = size/max(d.scores)
			point_a = origin
			i = 0
			x = 0
			for score in d.scores:
				if i==epoch_frequency:
					point_b = (origin [0]+x*dx,origin [1]-score*dy)
					pygame.draw.line(screen, BLUE, point_a, point_b)
					point_a = point_b
					i = 0
				i+=1
				x+=1


# The graphic objects manipulated by the UI, not used by the simulation
class Start (pygame.sprite.Sprite):
	def __init__(self,  x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.col = 0
		self.row = 0

		img = pygame.transform.scale(start_obj_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(img, 0)
		self.rect = self.image.get_rect()
		# we intialize the sprite base
		self.rect.x = self.x
		self.rect.y = self.y

class End (pygame.sprite.Sprite):
	def __init__(self,  x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.col = 0
		self.row = 0

		img = pygame.transform.scale(end_obj_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(img, 0)
		self.rect = self.image.get_rect()
		# we intialize the sprite base
		self.rect.x = self.x
		self.rect.y = self.y

class Block (pygame.sprite.Sprite):
	def __init__(self,  x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.col = 0
		self.row = 0

		img = pygame.transform.scale(block_obj_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(img, 0)
		self.rect = self.image.get_rect()
		# we intialize the sprite base
		self.rect.x = self.x
		self.rect.y = self.y

class Preferred(pygame.sprite.Sprite):
	def __init__(self,  x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.col = 0
		self.row = 0

		img = pygame.transform.scale(preferred_obj_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(img, 0)
		self.rect = self.image.get_rect()
		# we intialize the sprite base
		self.rect.x = self.x
		self.rect.y = self.y

class Crossable (pygame.sprite.Sprite):
	def __init__(self,  x, y):
		super().__init__()
		self.x = x
		self.y = y
		self.col = 0
		self.row = 0

		img = pygame.transform.scale(crossable_obj_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(img, 0)
		self.rect = self.image.get_rect()
		# we intialize the sprite base
		self.rect.x = self.x
		self.rect.y = self.y

# This class is used only for displaying a cursor during the delete sequence
class Delete (pygame.sprite.Sprite):
	def __init__(self,  x, y):
		super().__init__()
		self.x = x
		self.y = y

		img = pygame.transform.scale(delete_obj_img, (tile_size, tile_size))
		self.image = pygame.transform.rotate(img, 0)
		self.rect = self.image.get_rect()
		# we intialize the sprite base
		self.rect.x = self.x
		self.rect.y = self.y


# The cells are used by the simulation engine.
class Cell ():
	def __init__(self,  col, row, ctype, rank):
		super().__init__()
		self.col = col
		self.row = row
		# cell type : "Free",  "Preferred", or "Crossable"
		# NB: blocks are not added as cells, they are ignored completely.
		self.ctype = ctype
		self.rank = rank
		#  frequency at which the training visits this cell
		self.visit = 0




