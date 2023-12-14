# Ariel Morandy -  Nov 2023
# I took some inspiration from
# https://www.viralml.com/video-content.html?v=nSxaG_Kjw_w
import declaration as d
from declaration import *
import pygame
import classes as c
import userinterface as ui
import simulation as simu
import random
import method as m
import matplotlib.pyplot as plt
import helper as h


from line_profiler_pycharm import profile

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Finding Path via RL')


# show a long message
display_long_message = False
long_message = ""

# list to manage button activity
button_list = []

# create the main Objects
world  = c.World()
grid   = c.Grid()

# main creation of creation buttons
ui.menu_create(button_list)

# simulation and open are independant
x = button_size
y = screen_height +1  - button_zone_low_height
button_simulation = ui.Button("simulation", 15 * x,y )
button_open       = ui.Button("open", 16 * x, y)
button_filter = ui.Button("filter",10 * button_size , 0 )

# create at least one Start and one End
col , row = 0 , 0
x , y = col * tile_size + grid_margin_x, row * tile_size + button_zone_high_height
d.cell_start = c.Start(x,y)
d.all_sprites_list.add(d.cell_start)
d.cell_start.col , d.cell_start.row = col , row

col , row = 15 , 15
x , y = col * tile_size + grid_margin_x, row * tile_size + button_zone_high_height
d.cell_end  = c.End(x,y)
d.all_sprites_list.add(d.cell_end)
d.cell_end.col , d.cell_end.row = col , row


# we clean the cell list and recompute the active cells
m.clear_env(button_filter.state)
world.state = 0

# game loop
inwork_mode = False
tmp_object = None
placement_type = ""


run = True
while run:
	clock.tick(60)

	for event in pygame.event.get():

		Mouse_x, Mouse_y = pygame.mouse.get_pos()


		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:

			placement_type = ""
			button_simulation.click()
			button_open.click()
			button_filter.click()

			# check all the buttons from button list, if something is clicked, deactivate all
			placement_type = ui.menu_state_from_event(button_list)

			#if a Q training exists, we display the adjacent Q values if a valid cell is selected
			if d.training_ready:
				col, row  =m.get_colrow_from_coordinates(Mouse_x, Mouse_y)
				'''print("Col / Row  = ", col, row)'''
				cell_selected = None
				cell_selected = m.find_cell(col, row)

				if cell_selected is not None:
					print("Cell # Selected  = ", cell_selected.rank)
					# we save this info for the display in Grid Class
					d.cell_under_mouse = cell_selected

		if button_open.state == "pressed":
			world.open ()
			button_open.state = "depressed"

		if placement_type != "":

			# a temporary object is created on left click if its button is active.
			if not inwork_mode:

				# creation of object based on category selected from the active button
				object_class = ui.class_selection_from_button(button_list)

				if object_class != "":
					tmp_object = eval("c." + object_class)(Mouse_x, Mouse_y)

				print("Object of Graphic Class " + object_class + " is created in tmp", tmp_object)
				'''all_sprites_tmp.add(tmp_object)'''
				d.all_sprites_list.add(tmp_object)
				inwork_mode = True
				event.button = None

			# the temporary object moves with the mouse
			if inwork_mode:

				# snap to the grid
				col, row = m.get_colrow_from_coordinates(Mouse_x, Mouse_y)
				tmp_object.rect.x = col * tile_size + grid_margin_x
				tmp_object.rect.y = row * tile_size + button_zone_high_height


				if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT                 and \
				    button_zone_high_height < Mouse_y < (screen_height - button_zone_low_height) and \
					      grid_margin_x     < Mouse_x < (grid_width+grid_margin_x):

					print ("we enter the creation of " , tmp_object)

					# in Screen coordinates
					tmp_object.rect.x = col * tile_size + grid_margin_x
					tmp_object.rect.y = row * tile_size + button_zone_high_height
					tmp_object.x = Mouse_x
					tmp_object.y = Mouse_y
					tmp_object.col = col
					tmp_object.row = row

					pygame.sprite.Sprite.kill(tmp_object)

					if isinstance(tmp_object,c.Block):
						d.block_list.append(tmp_object)
						d.all_sprites_list.add(tmp_object)

						# we clean the cell list and recompute the active cells
						m.clear_env(button_filter.state)
						world.state = 0

					elif isinstance(tmp_object,c.Preferred):
						d.preferred_list.append(tmp_object)
						d.all_sprites_list.add(tmp_object)
						# we clean everything
						m.clear_env(button_filter.state)
						world.state = 0

					elif isinstance(tmp_object,c.Crossable):
						d.crossable_list.append(tmp_object)
						d.all_sprites_list.add(tmp_object)
						# we clean everything
						m.clear_env(button_filter.state)
						world.state = 0

					elif isinstance(tmp_object,c.Start):

						d.all_sprites_list.remove(d.cell_start)
						d.all_sprites_list.add(tmp_object)
						# we register the new Start Graphic
						d.cell_start = tmp_object
						# we clean the path if it was displayed
						d.steps.clear()

						if 	d.training_ready :
							# we can compute a new path, if training exists
							simu.compute_path(world)

					elif isinstance(tmp_object,c.End):
						d.all_sprites_list.remove(d.cell_end)
						d.all_sprites_list.add(tmp_object)
						# we register the new End Graphic
						d.cell_end = tmp_object
						# we clean everything
						m.clear_env(button_filter.state)
						world.state = 0

					elif isinstance(tmp_object,c.Delete):
						something_was_deleted = False
						# check if there is a "block" or a "preferred" and delete it, else do nothing
						col, row = m.get_colrow_from_coordinates(Mouse_x , Mouse_y )
						# is it a block?
						objecttodelete = m.find_block(col, row)
						if objecttodelete is not None:
							d.block_list.remove(objecttodelete)
							pygame.sprite.Sprite.kill(objecttodelete)
							something_was_deleted = True

						# is it a preferred spot?
						objecttodelete = m.find_preferred(col, row)
						if objecttodelete is not None:
							d.preferred_list.remove(objecttodelete)
							pygame.sprite.Sprite.kill(objecttodelete)
							something_was_deleted = True

						# is it a crossable spot?
						objecttodelete = m.find_crossable(col, row)
						if objecttodelete is not None:
							d.crossable_list.remove(objecttodelete)
							pygame.sprite.Sprite.kill(objecttodelete)
							something_was_deleted = True

						if something_was_deleted :
							# we clean everything
							world.state = 0
							m.clear_env(button_filter.state)
							world.state = 0

					# we remove the sprite from the tmp group

					inwork_mode = False


		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			print("Escape button used")
			# delete the temporary object, remove the sprite
			if tmp_object is not None:
				pygame.sprite.Sprite.kill(tmp_object)
				tmp_object = None
			inwork_mode = False
			ui.menu_reset(button_list)
			placement_type      = ""
			d.cell_under_mouse = None
			button_open.state = "depressed"


	# We erase the 2D and redraw the world the grid, and the UI
	screen.fill(GREY)
	world.draw(screen)
	grid.draw(screen)
	grid.draw_graph(screen)
	for button in button_list:
		button.draw(screen)
	button_simulation.draw(screen)
	button_open.draw(screen)
	button_filter.draw(screen)

	# We draw the sprite graphic group
	d.all_sprites_list.draw(screen)

	if button_simulation.state == "pressed" and d.cell_start !=None:
		# we reset the cells and paths
		d.edge_list.clear()

		# we recompute cells and paths
		nb_possible_paths = simu.compute_possible_paths()
		world.nb_possible_paths = nb_possible_paths

		# we initialize the matrix of network from the perspective of reaching the cell_goal

		simu.compute_matrix2 (world, screen)

		# we compute a first path, using the Start stored
		simu.compute_path(world)

		button_simulation.state = "depressed"


	pygame.display.update()


pygame.quit()
