import math
import declaration as d
import classes as c
from declaration import *

from line_profiler_pycharm import profile

def find_block(col, row):
	# the method finds block at the coordinates' col, row, and return  the object if found
	objectfound = None

	for block in d.block_list:
		if block.col == col and block.row == row:
			objectfound = block
			return objectfound

def find_preferred(col, row):
	# the method finds preferred at the coordinates' col, row, and return  the object if found
	objectfound = None

	for preferred in d.preferred_list:
		if preferred.col == col and preferred.row == row:
			objectfound = preferred
			return objectfound

def find_crossable(col, row):
	# the method finds preferred at the coordinates' col, row, and return  the object if found
	objectfound = None

	for crossable in d.crossable_list:
		if crossable.col == col and crossable.row == row:
			objectfound = crossable
			return objectfound

'''@profile'''
def find_cell(col, row):
	# the method finds cell at the coordinates' col, row, and return  the cell  if found
	objectfound = None

	for cell in d.cell_list:
		if cell.col == col and cell.row == row : return cell
	return objectfound

	'''# new method
	objectfound = None
	coord = (col, row)
	for cell in d.cell_list:
		match coord:
			case (cell.col, cell.row): return cell
	return objectfound'''

def get_colrow_from_coordinates(x, y):
	# works in W coordinates
	col = (x - grid_margin_x) // tile_size
	row = (y -button_zone_high_height)// tile_size
	return col, row

def find_cell_from_rank(rank):
	# the method finds cell using the rank and return the object cell
	objectfound = None

	for cell in d.cell_list:
		if cell.rank == rank:
			objectfound = cell
			return objectfound
	return objectfound

def find_cell_from_type (c_type):
	# the method finds cell using the ctype and return the object cell
	# works for "Free", "Start" ,  "End" and "Preferred"
	objectfound = None

	for cell in d.cell_list:
		if cell.ctype== c_type:
			objectfound = cell
			return objectfound

def clear_env (filter_state):
	# we clean the cell list and recompute the active cells
	d.steps.clear()
	compute_cells(filter_state)
	d.training_ready = False
	d.cell_under_mouse = None

	return

def compute_cells(filter_state):
	# we loop over the grid to create all the cells which are going to participate in the simulation
	# we must restrict the cells to the rectangle formed by Start and End if filter_state = "pressed"

	if filter_state == "pressed":
		min_row = min(d.cell_start.row,d.cell_end.row) -filter_margin
		min_col = min(d.cell_start.col,d.cell_end.col) -filter_margin
		if min_row < 0: min_row =0
		if min_col < 0: min_col =0

		max_row = max(d.cell_start.row,d.cell_end.row) + filter_margin
		max_col = max(d.cell_start.col,d.cell_end.col) + filter_margin
		if max_row > row_max : max_row =row_max
		if max_col > col_max : max_col =col_max
	else:
		min_row = 0
		min_col = 0
		max_row = row_max
		max_col = col_max



	d.cell_list.clear()

	nb_cells = 0
	i ,j = min_col ,min_row
	while j <=max_row:
		i = min_col
		while i <= max_col:
			objectfound = None
			objectfound = find_block(i, j)
			ctype = "Free"
			if objectfound == None:
				objectfound2 = None
				objectfound2 = find_preferred(i, j)
				if objectfound2 != None:
					ctype = "Preferred"
				objectfound3 = None
				objectfound3 = find_crossable(i, j)
				if objectfound3 != None:
					ctype = "Crossable"

				# we create the cell to hold the information
				cell = c.Cell (i, j, ctype ,nb_cells)
				d.cell_list.append(cell)
				'''d.cell_list.add(cell)'''
				nb_cells = nb_cells +1

			i = i+1
		j = j + 1

	print ("nb of cells" , nb_cells)
	return nb_cells

def position_between_cells (cell_a, cell_b):
	# for each cell , we have 4 possible states ( Top (0), Left (1), Bottom (2), right (3)), counted counter clock wise
	# this method returns 0,1,2,3 or -1
	# -1 means the two cells are not adjacent
	position =-1
	# top
	if cell_a.row -1 == cell_b.row  and cell_a.col == cell_b.col:
		position = 0

	# left
	if cell_a.row == cell_b.row  and cell_a.col -1 == cell_b.col:
		position = 1

	# Bottom
	if cell_a.row == cell_b.row -1 and cell_a.col == cell_b.col:
		position = 2

	# right
	if cell_a.row == cell_b.row  and cell_a.col  == cell_b.col -1:
		position = 3

	return position

def cell_from_position (cell, position):
	# for each cell , we have 4 possible states ( Top (0), Left (1), Bottom (2), right (3)), counted counter clock wise
	# this method returns a cell object from a given cell and a relative position
	# None means there is no adjacent cell at this position
	objectfound = None
	# top
	if position ==0:
		col = cell.col
		row = cell.row -1
		objectfound = find_cell(col, row)

	# left
	if position ==1:
		col = cell.col -1
		row = cell.row
		objectfound = find_cell(col, row)

	# Bottom
	if position ==2:
		col = cell.col
		row = cell.row +1
		objectfound = find_cell(col, row)

	# right
	if position ==3:
		col = cell.col +1
		row = cell.row
		objectfound = find_cell(col, row)

	return objectfound




