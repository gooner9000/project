#https://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points

#imports
import random
import pygame
import math
import Oslime
import berry
import ui


pygame.init()
pygame.font.init()


#set screen size
screen_width = 1360
screen_height = 980
screen = pygame.display.set_mode((screen_width, screen_height))
mutation_value = 0.2



def calculate_distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


def calculate_mutation(slime1, slime2, attribute_name):
    # Get the actual values dynamically using getattr()
    if attribute_name == 'colour0':
        val1 = getattr(slime1, 'colour')[0]
        val2 = getattr(slime2, 'colour')[0]

    elif attribute_name == 'colour1':
        val1 = getattr(slime1, 'colour')[1]
        val2 = getattr(slime2, 'colour')[1]

    elif attribute_name == 'colour2':
        val1 = getattr(slime1, 'colour')[2]
        val2 = getattr(slime2, 'colour')[2]

    else:
        val1 = getattr(slime1, attribute_name)
        val2 = getattr(slime2, attribute_name)

    # Calculate the mutation range based on those values
    combined_val = val1 + val2
    lower_bound = round(-1 * mutation_value * combined_val)
    upper_bound = round(mutation_value * combined_val)

    return random.randint(lower_bound, upper_bound)
def calculate_colour(slime1,slime2):
    colour0 = (slime1.colour[0] + slime2.colour[0])/2 + calculate_mutation(slime1,slime2,'colour0')
    if colour0 < 0:
        colour0 = 0
    if colour0 > 255:
        colour0 = 255
    colour1 = (slime1.colour[1] + slime2.colour[1])/2 + calculate_mutation(slime1,slime2,'colour1')
    if colour1 < 0:
        colour1 = 0
    if colour1 > 255:
        colour1 = 255
    colour2 = (slime1.colour[2] + slime2.colour[2])/2 + calculate_mutation(slime1,slime2,'colour2')
    if colour2 < 0:
        colour2 = 0
    if colour2 > 255:
        colour2 = 255
    return colour0, colour1, colour2
def Create_new_slime(slime1,slime2,berry_list):



    speed = (slime1.speed + slime2.speed)/2 + calculate_mutation(slime1,slime2,'speed')
    max_hunger = (slime1.max_hunger + slime2.max_hunger)/2 + calculate_mutation(slime1,slime2,'max_hunger')
    metabolism = (slime1.metabolism + slime2.metabolism)/2 + calculate_mutation(slime1,slime2,'metabolism')
    current_hunger = max_hunger*0.6
    colour = calculate_colour(slime1,slime2)
    size = round((slime1.size + slime2.size)/2) + calculate_mutation(slime1,slime2,'size')
    agression = (slime1.agression + slime2.agression)/2 + calculate_mutation(slime1,slime2,'agression')
    sight = (slime1.sight + slime2.sight)/2 + calculate_mutation(slime1,slime2,'sight')
    cx = (slime1.cx + slime2.cx)/2
    cy = (slime1.cy + slime2.cy)/2
    dead = False
    berries = berry_list
    return speed,max_hunger,metabolism,current_hunger,colour,size,agression,sight,cx,cy,dead,berries

#set screen size

running = True
#control framerate
clock = pygame.time.Clock()

slimes_list = []
berry_list = []
#set start attributes

start_size = 5
count = 0

#handle ui
#menu
game_state = "MENU"
centre_x = screen_width//2
stat_font = pygame.font.SysFont('Arial', 16, bold = True)
start_btn = ui.Button(centre_x - 400, 150, 800, 200, "start", (0,200,0), (0,150,0), stat_font)
settings_btn = ui.Button(centre_x -400, 400, 800, 200, "settings", (0,200,0), (0,150,0), stat_font)
exit_btn = ui.Button(centre_x -400, 650, 800, 200, "exit", (0,200,0), (0,150,0), stat_font)
#game
speed_slider = ui.Slider(20,150,200,20,10,1000,60,"speed","blue")
#settings
size_slider = ui.Slider(centre_x-100,150,200,20,1,20,5,"size","blue")
nslimes_slider = ui.Slider(centre_x-100,200,200,20,1,50,5,"num of slimes","blue")
nberries_slider = ui.Slider(centre_x-100,250,200,20,10,200,80,"num of berries","blue")
back_button = ui.Button(centre_x - 200, 700, 400, 100, "back", (0,200,0), (0,150,0), stat_font)

def start_simulation(berry_num,slime_num,slime_size):
    slimes_list.clear()
    berry_list.clear()

    for i in range(berry_num):
        Aberry = [berry.Berry(regen_time=500,
                       available=True,
                       size=3,
                       cx=random.randint(start_size,screen.get_width()-start_size),
                       cy=random.randint(start_size,screen.get_height()-start_size)),0]
        berry_list.append(Aberry)
    #create slimes at start


    for i in range(slime_num):
        my_slime = [Oslime.Slime(speed=0.5,
                         max_hunger=10,
                         metabolism=150,
                        current_hunger=10,
                         colour=(0,150,50),
                        size=slime_size,
                         sight=50,
                         agression=1,
                         cx=random.randint(start_size,screen.get_width()-start_size),
                         cy=random.randint(start_size,screen.get_height()-start_size),
                        dead=False,
                         berries=berry_list)
                    ,0]
        slimes_list.append(my_slime)

    #find starting averages
    start_avgs = ui.get_averages(slimes_list)
    return start_avgs,slimes_list,berry_list
#while the program is playing

while running:
    # 1. Event handling


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == "MENU":
            if start_btn.isclicked(event):
                game_state = "GAME"
            elif settings_btn.isclicked(event):
                game_state = "SETTINGS"
            elif exit_btn.isclicked(event):
                running = False
        if game_state == "SETTINGS" or game_state == "GAME":
            if back_button.isclicked(event):
                game_state = "MENU"
    screen.fill((0, 0, 0))

    if game_state == "MENU":
        start_btn.draw(screen)
        settings_btn.draw(screen)
        exit_btn.draw(screen)
    if game_state == "SETTINGS":
        #size settings
        size_slider.handle_event(event)
        size_slider.draw(screen,stat_font)
        start_size = int(size_slider.val)
        #Nslimes settings
        nslimes_slider.handle_event(event)
        nslimes_slider.draw(screen,stat_font)
        slime_num = int(nslimes_slider.val)
        #Nberries settings
        nberries_slider.handle_event(event)
        nberries_slider.draw(screen, stat_font)
        berries_num = int(nberries_slider.val)
        #back button
        back_button.draw(screen)
        #set starting parameters
        starting_parameters = start_simulation(berries_num,slime_num,start_size)
        start_avgs = starting_parameters[0]
        slimes_list = starting_parameters[1]
        berry_list = starting_parameters[2]
    # 2. Update game state
    elif game_state == "GAME":
        slimes_to_remove = []  # Create an empty list to hold dead slimes

        for slime in slimes_list:

            speed_slider.handle_event(event)
            # Update the slime's state
            partner = slime[0].move(slimes_list)
            slime[0].eat()
            slime[0].move(slimes_list)
            slime[1] = slime[0].lose_hunger(slime[1])
            if partner is not None:
                if slime[0].Can_copy and partner.Can_copy:
                    slime[0].Can_copy = False
                    partner.Can_copy = False
                    new_slime_attributes = Create_new_slime(slime[0],partner,berry_list)
                    new_slime = [Oslime.Slime(speed=new_slime_attributes[0],
                         max_hunger=new_slime_attributes[1],
                         metabolism=new_slime_attributes[2],
                        current_hunger=new_slime_attributes[3],
                         colour=new_slime_attributes[4],
                        size=new_slime_attributes[5],
                         sight=new_slime_attributes[7],
                         agression=new_slime_attributes[6],
                         cx=new_slime_attributes[8],
                         cy=new_slime_attributes[9],
                        dead=new_slime_attributes[10],
                         berries=new_slime_attributes[11])
                    ,0]
                    slimes_list.append(new_slime)
                    slime[0].current_hunger = slime[0].current_hunger * 0.6
                    partner.current_hunger = partner.current_hunger * 0.6
                    partner = None
            # If the slime is dead, add it to our removal list
            if slime[0].dead:
                slimes_to_remove.append(slime)

        # 3. Now, safely remove the dead slimes AFTER the main loop is done
        for dead_slime in slimes_to_remove:
            slimes_list.remove(dead_slime)
        for berry_data in berry_list:
            berry_data[1] = berry_data[0].reset(berry_data[1])

        screen.fill((0, 0, 0))

        for berry_data in berry_list:
            berry_data[0].create()

        for slime_data in slimes_list:
            slime_data[0].create()

        speed_slider.draw(screen,stat_font)
        back_button.draw(screen)
        ui.draw_stats(screen,stat_font,slimes_list,start_avgs)
    # 5. Update the display
    pygame.display.flip()

    clock.tick(int(speed_slider.val))

# Quit Pygame when the loop ends
pygame.quit()


