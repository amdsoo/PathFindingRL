# Ariel Morandy - Nov 2023
import declaration as d
from declaration import *
import classes as c
import random
import method as m
import pygame
import networkx as nx
import numpy as np
import time


'''from line_profiler_pycharm import profile'''


def available_actions( R , state):
	#we only pick the possible action if the reward is superior to the reward init.
	current_state_row = R[state,]
	'''av_act = np.where(current_state_row >= 0)[1]'''
	av_act = np.where(current_state_row > reward_init)[1]
	return av_act

def sample_next_action(available_actions_range):
    next_action = int(np.random.choice(available_actions_range,1))
    return next_action

'''@profile'''
def update2(Q, R, current_state, action, gamma):

	# method to update the Q Table : the brain of how well the AI is doing exploring all the possibilities
	# we look for the cells around the given cell which have the highest value
	'''max_index = np.where(Q[action,] == np.max(Q[action,]))[1]'''
	# what is the cell corresponding to the action.

	# from the index, we now must retrieve the Cell based on the position
	'''cell_object = m.find_cell_from_rank(current_state)'''
	cell_object = d.cell_list [current_state]
	next_cell_object = m.cell_from_position(cell_object, action)

	#we extract the 4 values around that cell
	max_index = np.where(d.Q[next_cell_object.rank,] == np.max(d.Q[next_cell_object.rank,]))[1]

	if max_index.shape[0] > 1:
		max_index = int(np.random.choice(max_index, size=1))
	else:
		max_index = int(max_index)
	max_value = d.Q[next_cell_object.rank, max_index]

	# BellMan Equation , with discount gamma, alpha =1 in this exemple
	d.Q[current_state, action] = R[current_state, action] + gamma * max_value
	'''print('max_value', R[current_state, action] + gamma * max_value)'''

	if (np.max(d.Q) > 0):
		return (np.sum(d.Q / np.max(d.Q) * 100))
	else:
		return (0)

def compute_possible_paths():
	# we loop over the cells to establish all the possible paths, cell to cell, this is done without any goal (end) or start in mind
	nb_possible_paths = 0
	for cell in d.cell_list:
		col , row = cell.col , cell.row
		if col <col_max:
			# we check if there is free cell on the right of the current cell
			cellfound = None
			cellfound = m.find_cell (col+1, row)
			if cellfound != None:
				d.edge_list.append((cell,cellfound))
				nb_possible_paths = nb_possible_paths +1
		if row <row_max:
			# we check if there is free cell on the bottom of the current cell
			cellfound = None
			cellfound = m.find_cell (col, row+1)
			if cellfound != None:
				d.edge_list.append((cell,cellfound))
				nb_possible_paths = nb_possible_paths +1

	print("nb of possible paths", nb_possible_paths)
	return nb_possible_paths

def compute_matrix2 (world, screen):
	# we measure time from here
	start_time = time.time()

	nb_cells = len(d.cell_list)
	edge_array =[]


	# retrieve start and end cells from graphics
	'''objectstart = m.find_cell(d.cell_start.col, d.cell_start.row)
	cell_start = objectstart.rank'''
	objectend   = m.find_cell(d.cell_end.col, d.cell_end.row)
	cell_goal = objectend.rank


	# we convert the model of edge and cell into an array to be able to use the algo
	for edge in d.edge_list:
		cell_a = edge [0].rank
		cell_b = edge [1].rank
		edge_array.append((cell_a,cell_b))



	# ------------------------------------------------------------------------------------------------------
	# Training

	# how many points in graph? x points
	MATRIX_SIZE = nb_cells

	# create matrix x*y
	# for each cell , we have 4 possible states ( Top (0), Left (1), Bottom (2), right (3)), counted counter clock wise
	R = np.matrix(np.ones(shape=(nb_cells, 4)))

	# we value by default all the states at the reward_init value
	R *= reward_init

	# assign zeros to paths and 100 to goal-reaching point
	for point in edge_array:
		# because the array is built (Bottom, Right), we must do two passes
		# compute relative position a to b
		cell_a = m.find_cell_from_rank(point[0])
		cell_b = m.find_cell_from_rank(point[1])
		position = m.position_between_cells (cell_a, cell_b)

		if point[1] == cell_goal:
			R[point[0],position] = reward_goal
		elif  m.find_cell_from_rank(point[1]).ctype == "Preferred":
			R[point[0],position] = reward_preferred
		elif  m.find_cell_from_rank(point[1]).ctype == "Crossable":
			R[point[0],position] = reward_crossable
		else:
			R[point[0],position] = reward_nothing

		# compute relative position b to a
		cell_a = m.find_cell_from_rank(point[1])
		cell_b = m.find_cell_from_rank(point[0])
		position = m.position_between_cells(cell_a, cell_b)

		if point[0] == cell_goal:
			R[point[1],position] = reward_goal
		elif  m.find_cell_from_rank(point[0]).ctype == "Preferred":
			R[point[1],position] = reward_preferred
		elif  m.find_cell_from_rank(point[0]).ctype == "Crossable":
			R[point[1],position] = reward_crossable
		else:
			R[point[1],position] = reward_nothing

	# add specal goals around the End point (trick to stop the process)
	object_cell_goal = m.find_cell_from_rank(cell_goal)
	objectfound = None
	objectfound = m.cell_from_position(object_cell_goal, 0)
	if objectfound is not None:
		R[cell_goal, 0] = reward_goal
	objectfound = None
	objectfound = m.cell_from_position(object_cell_goal, 1)
	if objectfound is not None:
		R[cell_goal, 1] = reward_goal
	objectfound = None
	objectfound = m.cell_from_position(object_cell_goal, 2)
	if objectfound is not None:
		R[cell_goal, 2] = reward_goal
	objectfound = None
	objectfound = m.cell_from_position(object_cell_goal, 3)
	if objectfound is not None:
		R[cell_goal, 3] = reward_goal


	print(R)

	# the Matrix in mode 2 is
	# Row = [State]  for nb_cells
	# Column = [top, left, bottom, right ]

	d.Q = np.matrix(np.zeros([nb_cells, 4]))

	'''# we check the available actions from our starting postion
	available_act = available_actions(R ,cell_start)

	# we pick one randomly
	action = sample_next_action(available_act)

	# we update our Q table based on the reward on the first position
	update2(d.Q, R, cell_start, action, gamma)'''

	# Now we can do the Training
	d.scores = []
	best_score = 0
	cycle_best_score = 0
	display = 0

	print("Entering Q matrix training :")
	for i in range(epoch_max):
		# we take random positions between all the cells
		current_state = np.random.randint(0, int(d.Q.shape[0]))

		'''if i > 25000 and current_state == 43:
			pass'''

		available_act = available_actions(R, current_state)
		action = sample_next_action(available_act)
		score = update2(d.Q, R, current_state, action, gamma)
		d.scores.append(score)

		display = display + 1
		# store the new best score
		if score > best_score:
			best_score = score
			cycle_best_score = i
			world.score = round(best_score)

		# display every 100 iterations (change to display more often)
		if display == 1000:
			world.cycle = i+1
			world.draw(screen)
			pygame.display.update()
			display = 0

	world.cycle = cycle_best_score

	print("Trained Q matrix:")
	'''print(d.Q/np.max(d.Q)*100)'''
	k = 0
	while k<nb_cells:
		print ("state #", k, d.Q[k], ",")
		k +=1

	d.training_ready = True

	end_time = time.time()
	world.computation_time = round(end_time - start_time,2)
	'''print("Compute time #", world.computation_time)'''

	return

def compute_path (world):
	# ------------------------------------------------------------------------------------------------------
	# Finding path of higher values
	nb_cells = len(d.cell_list)
	# retrieve start and end cells from graphics
	objectstart = m.find_cell(d.cell_start.col, d.cell_start.row)

	if objectstart is None:
		d.steps = []
		world.nb_random_choice = 0
		world.state = 1
		print("No solution found")
		return
	cell_start = objectstart.rank


	objectend   = m.find_cell(d.cell_end.col, d.cell_end.row)
	cell_goal = objectend.rank

	d.steps = []
	current_state = cell_start
	d.steps = [current_state]
	world.nb_random_choice = 0

	# a counter to exit if the system cannot find a way to reach the goal
	count = 0
	exit_with_error = False


	while current_state != cell_goal:
		val1 = d.Q[current_state,]
		val2 = np.max(d.Q[current_state,])
		next_step_index = np.where(d.Q[current_state,] == np.max(d.Q[current_state,]))[1]
		'''print ("next_step_index", next_step_index)'''
		if next_step_index.shape[0] > 1:
			next_step_index = int(np.random.choice(next_step_index, size=1))
			# We also capture the number of random choices
			world.nb_random_choice +=1
		else:
			next_step_index = int(next_step_index)

		# from the index, we now must retrieve the Cell based on the position
		cell_object = m.find_cell_from_rank(current_state)
		next_cell_object = m.cell_from_position(cell_object, next_step_index)

		if next_cell_object is None:
			#this case happens when the Q table is too empty, for instance if this is an impossible choice (moving to a cell that doesnt exist)
			exit_with_error = True

		count +=1
		if count > nb_cells*2:
			exit_with_error = True

		if exit_with_error:
			d.steps = []
			world.nb_random_choice = 0
			world.state =1
			print("No solution found")
			return

		# we store the new cell and move to the next one
		d.steps.append(next_cell_object.rank)
		current_state = next_cell_object.rank

	print("Most efficient path:" , d.steps)
	world.state = 2

	return