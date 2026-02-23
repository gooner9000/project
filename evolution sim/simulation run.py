

#imports
import random
import Oslime
import pygame
import math

import berry
import ui
import plotting

pygame.init()
pygame.font.init()


#set screen size
screen_width = 1800
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
    lower_bound = round(-1 * mutation_value * combined_val/2)
    upper_bound = round(mutation_value * combined_val / 2)
    sigma = round(mutation_value * combined_val / 2)

    mutation_delta = random.gauss(0, sigma)

    if mutation_delta < lower_bound:
        mutation_delta = lower_bound
    if mutation_delta > upper_bound:
        mutation_delta = upper_bound

    return mutation_delta

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

    size = round(round((slime1.size + slime2.size) / 2) + calculate_mutation(slime1, slime2, 'size'))
    speed = (slime1.speed + slime2.speed)/2 + calculate_mutation(slime1,slime2,'speed')
    sight = (slime1.sight + slime2.sight) / 2 + calculate_mutation(slime1, slime2, 'sight')
    max_hunger = round((slime1.max_hunger + slime2.max_hunger)/2) + calculate_mutation(slime1,slime2,'max_hunger')
    metabolism = (slime1.metabolism + slime2.metabolism)/2 + calculate_mutation(slime1,slime2,'metabolism')
    current_hunger = max_hunger*0.6
    colour = calculate_colour(slime1,slime2)
    aggression = (slime1.aggression + slime2.aggression)/2 + calculate_mutation(slime1,slime2,'aggression')
    lifespan = (slime1.lifespan + slime2.lifespan)/2 + calculate_mutation(slime1,slime2,'lifespan')
    cx = (slime1.cx + slime2.cx)/2
    cy = (slime1.cy + slime2.cy)/2
    dead = False
    berries = berry_list

    return speed,max_hunger,metabolism,current_hunger,colour,size,aggression,sight,cx,cy,dead,berries,lifespan

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
start_btn = ui.Button(centre_x - 400, 150, 800, 200, "start", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)
settings_btn = ui.Button(centre_x - 400, 400, 800, 200, "settings", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)
exit_btn = ui.Button(centre_x - 400, 650, 800, 200, "exit", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)

#game
speed_slider = ui.Slider(20, 800, 200, 20, 10, 200, 60, "speed", pygame.Color("#F0F2D5"))
simulation_box = ui.Box(0,0,1360,980,pygame.Color("#EF233C"))
#settings
size_slider = ui.Slider(centre_x - 100, 150, 200, 20, 1, 20, 5, "size", pygame.Color("#F0F2D5"))
nslimes_slider = ui.Slider(centre_x - 100, 200, 200, 20, 1, 50, 5, "num of slimes", pygame.Color("#F0F2D5"))
nberries_slider = ui.Slider(centre_x - 100, 250, 200, 20, 10, 200, 80, "num of berries", pygame.Color("#F0F2D5"))
mutation_slider = ui.Slider(centre_x - 100, 300, 200, 20, 0.1, 0.9, 0.2, "variation of mutations", pygame.Color("#F0F2D5"))
stspeed_slider = ui.Slider(centre_x - 100, 350, 200, 20, 0.1, 0.9, 0.2, "movement speed", pygame.Color("#F0F2D5"))
back_button = ui.Button(centre_x - 850, 900, 100, 50, "back", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)

def start_simulation(berry_num,slime_num,slime_size,start_speed):
    slimes_list.clear()
    berry_list.clear()

    for i in range(berry_num):
        Aberry = [berry.Berry(regen_time=random.randint(400,800),
                              available=True,
                              size=3,
                              cx=random.randint(start_size,berry.screen_widthB-start_size),
                              cy=random.randint(start_size,berry.screen_heightB-start_size)), 0]
        berry_list.append(Aberry)
    #create slimes at start


    for i in range(slime_num):
        my_slime = [Oslime.Slime(speed=start_speed,
                                 max_hunger=10,
                                 current_hunger=10,
                                 colour=(0,150,50),
                                 size=slime_size,
                                 sight=50,
                                 metabolism=200,
                                 aggression=1,
                                 cx=random.randint(start_size,Oslime.screen_widthS-start_size),
                                 cy=random.randint(start_size,Oslime.screen_heightS-start_size),
                                 dead=False,
                                 berries=berry_list,
                                 lifespan = random.randint(9000,10500))
                    , 0]
        slimes_list.append(my_slime)

    #find starting averages
    start_avgs = ui.get_averages(slimes_list,screen,stat_font)
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

        #mutation value settings
        mutation_slider.handle_event(event)
        mutation_slider.draw(screen,stat_font)
        mutation_value = float(mutation_slider.val)

        #starting speed settings
        stspeed_slider.handle_event(event)
        stspeed_slider.draw(screen,stat_font)
        start_speed = float(stspeed_slider.val)
        #back button
        back_button.draw(screen)

        #set starting parameters
        starting_parameters = start_simulation(berries_num,slime_num,start_size,start_speed)
        start_avgs = starting_parameters[0]
        slimes_list = starting_parameters[1]
        berry_list = starting_parameters[2]
        total_deaths_from_age = 0
        total_starvations = 0

        #reset graphs
        timer = 0
        sec_timer = 0
        time_plot = []
        population_plot = []
        metabolism_plot = []

    # 2. Update game state
    elif game_state == "GAME":
        slimes_to_remove = []  # Create an empty list to hold dead slimes

        for slime in slimes_list:

            speed_slider.handle_event(event)
            # Update the slime's state
            partner = slime[0].move(slimes_list)
            slime[0].eat()
            slime[0].move(slimes_list)
            slime[1] = slime[0].lose_hunger(slime[1])  # remove hunger
            #check cause of death

            if slime[0].diehunger():
                total_starvations += 1

            if slime[0].reducelifespan():
                total_deaths_from_age += 1



            if partner is not None:
                if slime[0].Can_copy and partner.Can_copy:
                    slime[0].Can_copy = False
                    partner.Can_copy = False
                    for i in range(1,random.randint(1,4)):
                        new_slime_attributes = Create_new_slime(slime[0],partner,berry_list)

                        new_slime = [Oslime.Slime(speed=new_slime_attributes[0],
                                              max_hunger=new_slime_attributes[1],
                                              metabolism=new_slime_attributes[2],
                                              current_hunger=new_slime_attributes[3],
                                              colour=new_slime_attributes[4],
                                              size=new_slime_attributes[5],
                                              sight=new_slime_attributes[7],
                                              aggression=new_slime_attributes[6],
                                              cx=new_slime_attributes[8],
                                              cy=new_slime_attributes[9],
                                              dead=new_slime_attributes[10],
                                              berries=new_slime_attributes[11],
                                              lifespan = new_slime_attributes[12])
                        , 0]
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

        screen.fill((10, 10, 10))

        for berry_data in berry_list:
            berry_data[0].create()

        for slime_data in slimes_list:
            slime_data[0].create()

        speed_slider.draw(screen,stat_font)
        back_button.draw(screen)
        simulation_box.draw(screen)
        if slimes_list != []:
            ui.draw_stats(screen, stat_font, slimes_list, start_avgs, total_deaths_from_age, total_starvations)




        #print graphs
        """
        if timer%60 == 0:#makes it so only creates a graph every 60 frames
            sec_timer += 1
            plotting.plot(time_plot, population_plot, "time/s", "population")
            plotting.plot(time_plot, metabolism_plot, "time/s", "metabolism")
            # load the image
            pop_graph_image = pygame.image.load('populationplot.png')
            pop_graph_image = pygame.transform.scale(pop_graph_image, (400, 300))

            met_graph_image = pygame.image.load('metabolismplot.png')
            met_graph_image = pygame.transform.scale(met_graph_image, (400, 300))


        population_plot.append(len(slimes_list))
        if slimes_list != []:
            metabolism_plot.append(ui.get_averages(slimes_list,screen,stat_font)[4])
        time_plot.append(sec_timer)
        timer += 1
        #display the graph
        screen.blit(pop_graph_image, (1380, 0))
        screen.blit(met_graph_image, (1380, 300))
        """
    # 5. Update the display
    pygame.display.flip()

    clock.tick(int(speed_slider.val))

# Quit Pygame when the loop ends
pygame.quit()


