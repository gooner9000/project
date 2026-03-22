

#imports
import random
from bdb import effective

from pygame import K_SPACE

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
    """calculates the distance between two points"""
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


def calculate_mutation(slime1, slime2, attribute_name):
    """ calculates the mutation delta for a certain attribute in a slime that is to be created
        uses a normal distribution to calculate it.
    """
    #for the colour attribute it is worked out differently than for other attributes
    #colour is split into 3 values and a seperate mutation delta is worked out for each one
    if attribute_name == 'colour0':
        #gets the value of the first colour value from both parents
        val1 = getattr(slime1, 'colour')[0]
        val2 = getattr(slime2, 'colour')[0]

    elif attribute_name == 'colour1':
        val1 = getattr(slime1, 'colour')[1]
        val2 = getattr(slime2, 'colour')[1]

    elif attribute_name == 'colour2':
        val1 = getattr(slime1, 'colour')[2]
        val2 = getattr(slime2, 'colour')[2]

    else:
        #if the attribute is not colour it just gets the value of that attribute from both parents
        val1 = getattr(slime1, attribute_name)
        val2 = getattr(slime2, attribute_name)

    # Calculate the mutation range based on those values
    combined_val = val1 + val2
    # standard deviation calculated for the normal distribution
    sigma = (mutation_value * combined_val / 2)
    # lower bound and upper bound calculated at 2 standard deviations away from the mean
    lower_bound = sigma * -2
    upper_bound = sigma * 2
    # gets a random value from the distribution
    mutation_delta = random.gauss(0, sigma)
    # keeps the mutation delta within the bounds
    if mutation_delta < lower_bound:
        mutation_delta = lower_bound
    if mutation_delta > upper_bound:
        mutation_delta = upper_bound

    return mutation_delta

def calculate_colour(slime1,slime2):
    """determines the colour of an offspring based on the two parents"""
    #calculate value of first colour value
    colour0 = (slime1.colour[0] + slime2.colour[0])/2 + calculate_mutation(slime1,slime2,'colour0')
    #ensures the colour stays within the limits of the RGB spectrum
    if colour0 < 0:
        colour0 = 0
    if colour0 > 255:
        colour0 = 255
    #calculate second colour value
    colour1 = (slime1.colour[1] + slime2.colour[1])/2 + calculate_mutation(slime1,slime2,'colour1')
    if colour1 < 0:
        colour1 = 0
    if colour1 > 255:
        colour1 = 255
    #calculate third colour value
    colour2 = (slime1.colour[2] + slime2.colour[2])/2 + calculate_mutation(slime1,slime2,'colour2')
    if colour2 < 0:
        colour2 = 0
    if colour2 > 255:
        colour2 = 255

    return colour0, colour1, colour2

def Create_new_slime(slime1,slime2,berry_list):
    """generates a full set of attributes for a new slime based on its parents
        returns a list of the values of all the attributes"""
    size = (slime1.size + slime2.size) / 2 + calculate_mutation(slime1, slime2, 'size')
    # stops slime from getting too big or too small to the point that the program breaks
    if size < 1:
        size = 1
    if size > Oslime.screen_heightS/2:
        size = Oslime.screen_heightS/2
    speed = (slime1.speed + slime2.speed)/2 + calculate_mutation(slime1,slime2,'speed')
    #ensures the slime cannot have negative speed or be equal to 0
    if speed <= 0:
        speed = 0.000001
    sight = (slime1.sight + slime2.sight) / 2 + calculate_mutation(slime1, slime2, 'sight')
    #ensures the slime cannot have a negative sight value
    if sight <= 0:
        sight = 0
    max_hunger = round((slime1.max_hunger + slime2.max_hunger)/2) + calculate_mutation(slime1,slime2,'max_hunger')
    energy_efficiency = (slime1.energy_efficiency + slime2.energy_efficiency) / 2 + calculate_mutation(slime1, slime2, 'energy_efficiency')
    #slime starts at 60% of its maximum energy level
    current_hunger = max_hunger*0.6
    colour = calculate_colour(slime1,slime2)
    lifespan = (slime1.lifespan + slime2.lifespan)/2 + calculate_mutation(slime1,slime2,'lifespan')
    cx = (slime1.cx + slime2.cx)/2
    cy = (slime1.cy + slime2.cy)/2
    dead = False
    berries = berry_list

    return speed,max_hunger,energy_efficiency,current_hunger,colour,size,sight,cx,cy,dead,berries,lifespan



running = True
#control framerate
clock = pygame.time.Clock()

slimes_list = []
berry_list = []
#set start attributes

start_size = 5
count = 0

#handle ui, ui made from classes in UI.py

#menu ui
game_state = "MENU"
centre_x = screen_width//2
stat_font = pygame.font.SysFont('Arial', 16, bold = True)
start_btn = ui.Button(centre_x - 400, 150, 800, 200, "start", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)
settings_btn = ui.Button(centre_x - 400, 400, 800, 200, "settings", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)
exit_btn = ui.Button(centre_x - 400, 650, 800, 200, "exit", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)

#game ui
speed_slider = ui.Slider(1390, 700, 200, 20, 10, 200, 60, "speed", pygame.Color("#F0F2D5"))
simulation_box = ui.Box(0,0,1360,980,pygame.Color("#EF233C"))
back_button_game = ui.Button(centre_x + 600, 800, 200, 80, "back", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)
view_graph_button = ui.Button(centre_x + 600, 400, 200, 80, "view graphs", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)

#settings ui
size_slider = ui.Slider(centre_x - 100, 150, 200, 20, 1, 20, 5, "size", pygame.Color("#F0F2D5"))
nslimes_slider = ui.Slider(centre_x - 100, 200, 200, 20, 1, 50, 5, "num of slimes", pygame.Color("#F0F2D5"))
nberries_slider = ui.Slider(centre_x - 100, 250, 200, 20, 10, 200, 80, "num of berries", pygame.Color("#F0F2D5"))
mutation_slider = ui.Slider(centre_x - 100, 300, 200, 20, 0.1, 0.9, 0.2, "variation of mutations", pygame.Color("#F0F2D5"))
stspeed_slider = ui.Slider(centre_x - 100, 350, 200, 20, 0.1, 0.9, 0.2, "movement speed", pygame.Color("#F0F2D5"))
back_button_settings = ui.Button(centre_x - 100, 500, 200, 80, "back", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)

#graphs ui
back_button_graph = ui.Button(centre_x + 600, 800, 200, 80, "back", pygame.Color("#97051D"), pygame.Color("#EF233C"), stat_font)
#initialize graphs
#resets all the graph lists and images
pop_graph_image = None
eff_graph_image = None
sight_graph_image = None
speed_graph_image = None
lifespan_graph_image = None
size_graph_image = None
population_plot = []
energy_efficiency_plot = []
sight_plot = []
speed_plot = []
lifespan_plot = []
size_plot = []
timer = 0
time_plot = []




def start_simulation(berry_num,slime_num,slime_size,start_speed):
    """ makes the initial slime and berry objects at the start of the simulation as well as putting them in lists,
        all parameters are determined by the user in the settings before the simulations starts,
        also gets the average attributes of the starting slimes"""

    slimes_list.clear()
    berry_list.clear()
    #creates the list of berries
    for i in range(berry_num):
        # every item in the berry list is a list of length 2 with the first item being the object and the second being a counter
        Aberry = [berry.Berry(regen_time=random.randint(400,800),
                              available=True,
                              size=3,
                              cx=random.randint(start_size,berry.screen_widthB-start_size),
                              cy=random.randint(start_size,berry.screen_heightB-start_size)), 0]
        berry_list.append(Aberry)

    #create slimes at start
    for i in range(slime_num):
        # every item in the slime list is a list of length 2 with the first item being the object and the second being a counter
        start_slime = [Oslime.Slime(speed=start_speed,
                                 max_hunger=10,
                                 current_hunger=10,
                                 colour=(50,150,50),
                                 size=slime_size,
                                 sight=80,
                                 energy_efficiency=40,
                                 cx=random.randint(start_size,Oslime.screen_widthS-start_size),
                                 cy=random.randint(start_size,Oslime.screen_heightS-start_size),
                                 dead=False,
                                 berries=berry_list,
                                 lifespan = random.randint(9000,10500))
                    , 0]
        slimes_list.append(start_slime)

    #find starting averages
    start_avgs = ui.get_averages(slimes_list,screen,stat_font)
    return start_avgs,slimes_list,berry_list

#while the program is playing
while running:

    # determine when to change game states
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #starts in MENU game state
        if game_state == "MENU":
            if start_btn.isclicked(event):
                game_state = "GAME"
            elif settings_btn.isclicked(event):
                game_state = "SETTINGS"
            elif exit_btn.isclicked(event):
                running = False
        if game_state == "SETTINGS" or game_state == "GAME":
            if back_button_settings.isclicked(event) or back_button_game.isclicked(event):
                game_state = "MENU"
        if game_state == "GAME":
            if view_graph_button.isclicked(event):
                game_state = "GRAPHS"
        if game_state == "GRAPHS":
            if back_button_graph.isclicked(event):
                game_state = "GAME"
    screen.fill((10, 10, 10))

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
        back_button_settings.draw(screen)

        #set starting parameters
        starting_parameters = start_simulation(berries_num,slime_num,start_size,start_speed)
        start_avgs = starting_parameters[0]
        slimes_list = starting_parameters[1]
        berry_list = starting_parameters[2]
        total_deaths_from_age = 0
        total_starvations = 0

        #reset graphs everytime the settings are visited, to start a new simulation
        timer = 0
        time_plot = []
        population_plot = []
        energy_efficiency_plot = []
        speed_plot = []
        sight_plot = []
        lifespan_plot = []
        size_plot = []
        pop_graph_image = None
        eff_graph_image = None
        speed_graph_image = None
        sight_graph_image = None
        lifespan_graph_image = None
        size_graph_image = None

    # 2. Update game state
    elif game_state == "GAME":
        slimes_to_remove = []

        #check user input
        keys = pygame.key.get_pressed()
        #check if simulation speed slider has been changed
        speed_slider.handle_event(event)

        #update the slime objects
        for slime in slimes_list:
            #slime.move can return a partner slime, if not partner = NONE
            partner = slime[0].move(slimes_list)
            slime[0].eat()
            #moves slimes twice per frame so that slimes have a better chance of surviving
            slime[0].move(slimes_list)
            slime[1] = slime[0].lose_hunger(slime[1])

            #check cause of death
            if slime[0].diehunger():
                total_starvations += 1

            if slime[0].Increase_age():
                total_deaths_from_age += 1


            # creating new slimes
            if partner is not None:
                if slime[0].Can_copy and partner.Can_copy:
                    slime[0].Can_copy = False
                    partner.Can_copy = False
                    #determine how many babies are created
                    #calculate standard deviation
                    energy = (slime[0].current_hunger + partner.current_hunger)/11
                    lower_bound = 1
                    sigma = energy
                    #select random number from distribution
                    num_of_babies = round(random.gauss(1, sigma))
                    #ensure num doesnt go below lower bound
                    if num_of_babies < lower_bound:
                        num_of_babies = lower_bound
                    #create the slimes
                    for i in range(num_of_babies):
                        new_slime_attributes = Create_new_slime(slime[0],partner,berry_list)

                        new_slime = [Oslime.Slime(speed=new_slime_attributes[0],
                                                  max_hunger=new_slime_attributes[1],
                                                  energy_efficiency=new_slime_attributes[2],
                                                  current_hunger=new_slime_attributes[3],
                                                  colour=new_slime_attributes[4],
                                                  size=new_slime_attributes[5],
                                                  sight=new_slime_attributes[6],
                                                  cx=new_slime_attributes[7],
                                                  cy=new_slime_attributes[8],
                                                  dead=new_slime_attributes[9],
                                                  berries=new_slime_attributes[10],
                                                  lifespan = new_slime_attributes[11])
                        , 0]
                        slimes_list.append(new_slime)
                    #parents lose energy to below the reproduction threshold after they reproduce
                    slime[0].current_hunger = slime[0].current_hunger * 0.6
                    partner.current_hunger = partner.current_hunger * 0.6
                    partner = None

            if slime[0].dead:
                slimes_to_remove.append(slime)


        #remove the slimes that died this frame
        for dead_slime in slimes_to_remove:
            slimes_list.remove(dead_slime)

        #handle the berry object
        for berry_data in berry_list:
            #either increments the counter or resets it depending on the output of reset()
            berry_data[1] = berry_data[0].reset(berry_data[1])

        screen.fill((10, 10, 10))
        #draw slimes and berries to the screen
        for berry_data in berry_list:
            berry_data[0].create()

        for slime_data in slimes_list:
            slime_data[0].create()

        #Ui for the GAME state
        speed_slider.draw(screen,stat_font)
        back_button_game.draw(screen)
        simulation_box.draw(screen)
        view_graph_button.draw(screen)
        #only draws if there are slimes in the simulation
        if slimes_list != []:
            ui.draw_stats(screen, stat_font, slimes_list, start_avgs, total_deaths_from_age, total_starvations)

        #update graphs
        #gets the new point of each graph
        if slimes_list != []:
            avgs = ui.get_averages(slimes_list, screen, stat_font)
            energy_efficiency_plot.append(avgs[4])
            speed_plot.append(avgs[1])
            sight_plot.append(avgs[3])
            lifespan_plot.append(avgs[6])
            size_plot.append(avgs[2])
            population_plot.append(len(slimes_list))
        #if no slimes alive all stats are zero
        else:
            energy_efficiency_plot.append(0)
            speed_plot.append(0)
            sight_plot.append(0)
            lifespan_plot.append(0)
            size_plot.append(0)
            population_plot.append(0)
        #updates the simulation timer
        time_plot.append(timer)
        timer += 1


    #graph state
    if game_state == "GRAPHS":


        plotting.plot(time_plot, population_plot, "frames", "population")
        plotting.plot(time_plot, energy_efficiency_plot, "frames", "energy efficiency")
        plotting.plot(time_plot, speed_plot, "frames", "movement speed")
        plotting.plot(time_plot, sight_plot, "frames", "sight")
        plotting.plot(time_plot, lifespan_plot, "frames", "lifespan")
        plotting.plot(time_plot, size_plot, "frames", "size")

        # load the image from the file and transforms them to the correct size
        pop_graph_image = pygame.image.load('populationplot.png').convert_alpha()
        pop_graph_image = pygame.transform.smoothscale(pop_graph_image, (400, 300))
        eff_graph_image = pygame.image.load('energy efficiencyplot.png').convert_alpha()
        eff_graph_image = pygame.transform.smoothscale(eff_graph_image, (400, 300))
        speed_graph_image = pygame.image.load('movement speedplot.png').convert_alpha()
        speed_graph_image = pygame.transform.smoothscale(speed_graph_image, (400, 300))
        sight_graph_image = pygame.image.load('sightplot.png').convert_alpha()
        sight_graph_image = pygame.transform.smoothscale(sight_graph_image, (400, 300))
        lifespan_graph_image = pygame.image.load('lifespanplot.png').convert_alpha()
        lifespan_graph_image = pygame.transform.smoothscale(lifespan_graph_image, (400, 300))
        size_graph_image = pygame.image.load('sizeplot.png').convert_alpha()
        size_graph_image = pygame.transform.smoothscale(size_graph_image, (400, 300))


        #display the graph onto the screen
        if 'pop_graph_image' in locals() and pop_graph_image != None:
            screen.blit(pop_graph_image, (0, 0))
            screen.blit(eff_graph_image, (400, 0))
            screen.blit(speed_graph_image, (800, 0))
            screen.blit(sight_graph_image, (1200, 0))
            screen.blit(lifespan_graph_image, (400, 300))
            screen.blit(size_graph_image, (0, 300))

        back_button_graph.draw(screen)

    # update the display
    pygame.display.flip()

    clock.tick(int(speed_slider.val))


pygame.quit()


