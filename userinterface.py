import declaration as d
from declaration import *
import method as m


button_width  = button_size
button_height = button_size


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
        self.object_class = "XX"


        #  image settings via naming
        #  "button_class_img" is the name of the icon when "pressed"
        #  "button_class_ns_img" is the name of the icon when "depressed"
        path = eval(str(button_class)+"_img")
        path_ns = eval(str(button_class) + "_ns_img")
        self.image = pygame.transform.scale(path, (self.width, self.height))
        self.image_ns = pygame.transform.scale(path_ns, (self.width, self.height))



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
            if self.button_class == "simulation":
                if self.state == "pressed":
                    self.state = "depressed"
                else:
                    # you can launch the simulation only if there is a Start
                    if d.cell_start != None:
                        self.state = "pressed"

            elif self.button_class == "filter":
                if self.state == "pressed":
                    self.state = "depressed"
                    m.clear_env(self.state)
                else:
                    # you can activate the Filter only if there is a Start
                    # if d.cell_start != None:
                        self.state = "pressed"
                        m.clear_env(self.state)

            elif self.button_class == "delete":
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

def class_selection_from_button (button_list):
    object_class_pressed = ""
    for button in button_list:
        if button.state == "pressed":
            object_class_pressed = button.object_class
    return object_class_pressed


def menu_state_from_event (button_list):

    placement_type = ""
    for button in button_list:
        button.click()
        if button.state == "pressed":
            placement_type = button.button_class
    return placement_type


def menu_create(button_list):
    # create the buttons of the Interface
    button_position_x = 11 * button_size
    button_position_y = 0

    button_name = ["start","end", "block", "preferred", "crossable", "delete"]

    for name in button_name:
        new_button = Button(name, button_position_x, button_position_y)

        # this trick should not be here, it is to indicate which class of object correspond each button
        new_button.object_class = name.capitalize()

        button_list.append(new_button)
        button_position_x = button_position_x + button_size

    return button_list
