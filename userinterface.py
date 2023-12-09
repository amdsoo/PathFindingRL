import declaration as d
from declaration import *


button_width  = button_size*0.8
button_height = button_size*0.8


class MouseHandler:
    def __init__(self):
        self.right_click = False
        self.start_pos = None
        self.end_pos = None

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.right_click = False
                self.end_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.right_click = True
                self.start_pos = event.pos

    def reset(self):
        self.right_click = False
        self.start_pos = None
        self.end_pos = None


class Button:
    def __init__(self, button_class, x, y):
        self.button_class = button_class
        self.color = LIGHTSHADE
        self.x = x
        self.y = y
        self.width = button_width
        self.height = button_height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.state = "depressed"
        self.parent = "parent"

        # default image

        if self.button_class == "End":
            self.image = pygame.transform.scale(end_img , (self.width, self.height))
            self.image_ns = pygame.transform.scale(end_ns_img , (self.width, self.height))

        if self.button_class == "Start":
            self.image = pygame.transform.scale(start_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(start_ns_img, (self.width, self.height))

        if self.button_class == "Block":
            self.image = pygame.transform.scale(block_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(block_ns_img, (self.width, self.height))

        if self.button_class == "Preferred":
            self.image = pygame.transform.scale(preferred_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(preferred_ns_img, (self.width, self.height))

        if self.button_class == "Crossable":
            self.image = pygame.transform.scale(crossable_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(crossable_ns_img, (self.width, self.height))

        if self.button_class == "Delete":
            self.image = pygame.transform.scale(delete_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(delete_ns_img, (self.width, self.height))

        if self.button_class == "Simulation":
            self.image = pygame.transform.scale(simu_on_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(simu_off_img, (self.width, self.height))

        if self.button_class == "open":
            self.image = pygame.transform.scale(open_img, (self.width, self.height))
            self.image_ns = pygame.transform.scale(open_ns_img, (self.width, self.height))


    def draw(self, screen):
        # Call this method to draw the button on the screen if visible.
        if self.state == "depressed":
            self.color = LIGHTSHADE
            screen.blit(self.image_ns, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x , self.y))


    def click (self):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y) :
            print ("button clicked -> ", "Status before change", self.state)
            # special treatment for Simulation
            if self.button_class == "Simulation":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    if d.cell_start != None:
                        self.state = "pressed"
            elif self.button_class == "Delete":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    self.state = "pressed"
            else:
                # if this is the creation button
                if self.state == "pressed":  # the button was pressed, so now we must be depressed it and hide all
                    print("this button becomes inactive")
                    self.state = "depressed"
                    '''for button in button_list:
                        button.state = "depressed"'''
                else:
                    print("this button becomes active")
                    self.state = "pressed"


def menu_reset (button_list):
    for button in button_list:
        button.state = "depressed"


def menu_selection_frombutton (button_list):
    object_class_pressed = ""
    for button in button_list:
        if button.state == "pressed":
            object_class_pressed = button.button_class
    return object_class_pressed


def menu_state_from_event (button_list):

    placement_type = ""
    for button in button_list:
        button.click()
        if button.state == "pressed":
            placement_type = button.button_class
    return placement_type


def menu_create (button_list):
    # create the buttons of the Interface
    button_position_x = 10 * button_size + button_size / 10
    button_position_y = button_size / 10

    button_position_x = button_position_x + button_size
    button_start = Button("Start", button_position_x, button_position_y)
    button_list.append(button_start)

    button_position_x = button_position_x + button_size
    button_end = Button("End", button_position_x, button_position_y)
    button_list.append(button_end)

    button_position_x = button_position_x + button_size
    button_block = Button("Block", button_position_x, button_position_y)
    button_list.append(button_block)

    button_position_x = button_position_x + button_size
    button_preferred = Button("Preferred", button_position_x, button_position_y)
    button_list.append(button_preferred )

    button_position_x = button_position_x + button_size
    button_crossable = Button("Crossable", button_position_x, button_position_y)
    button_list.append(button_crossable )

    button_position_x = button_position_x + button_size
    button_delete = Button("Delete", button_position_x, button_position_y)
    button_list.append(button_delete)


    return button_list
