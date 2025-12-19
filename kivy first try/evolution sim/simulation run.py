#https://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points

#imports
import random
import pygame
import math
import Oslime
import berry



pygame.init()
pygame.font.init()

stat_font = pygame.font.SysFont('Arial', 16, bold = True)
#set screen size
screen_width = 1360
screen_height = 980
screen = pygame.display.set_mode((screen_width, screen_height))
mutation_value = 0.2

def get_averages(slimes):
    count = len(slimes)

    if count == 0:
        # If no slimes, just show count 0 to avoid divide by zero errors
        text = font.render("Population: 0", True, (255, 255, 255))
        surface.blit(text, (10, 10))
        return

    # Initialize sums
    total_speed = 0
    total_size = 0
    total_sight = 0
    total_metabolism = 0

    # Sum up attributes
    for slime_data in slimes:
        # Remember slime_data is [slime_object, timer], so we access slime_data[0]
        s = slime_data[0]
        total_speed += s.speed
        total_size += s.size
        total_sight += s.sight
        total_metabolism += s.metabolism

    # Calculate averages
    avg_speed = round(total_speed / count, 2)
    avg_size = round(total_size / count, 2)
    avg_sight = round(total_sight / count, 2)
    avg_meta = round(total_metabolism / count, 2)

    return count, avg_speed, avg_size, avg_sight, avg_meta
def draw_stats(surface, font, slimes, start_stats):
    s_count, s_speed, s_size, s_sight, s_metabolism = start_stats
    count, avg_speed, avg_size, avg_sight, avg_meta = get_averages(slimes)
    # Create text surfaces
    # render(Text, Antialias, Color)
    pop_text = font.render(f"Population: {count}, Start: {s_count}", True, (255, 255, 255))
    speed_text = font.render(f"Avg Speed: {avg_speed}, Start: {s_speed}", True, (255, 255, 255))
    size_text = font.render(f"Avg Size: {avg_size}, Start: {s_size}", True, (255, 255, 255))
    sight_text = font.render(f"Avg Sight: {avg_sight}, Start: {s_sight}", True, (255, 255, 255))
    meta_text = font.render(f"Avg Metabolism: {avg_meta}, Start: {s_metabolism}", True, (255, 255, 255))

    # Blit (draw) them to the screen
    x_pos = 10
    y_pos = 10
    line_height = 20

    surface.blit(pop_text, (x_pos, y_pos))
    surface.blit(speed_text, (x_pos, y_pos + line_height))
    surface.blit(size_text, (x_pos, y_pos + line_height * 2))
    surface.blit(sight_text, (x_pos, y_pos + line_height * 3))
    surface.blit(meta_text, (x_pos, y_pos + line_height * 4))
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

for i in range(50):
    Aberry = [berry.Berry(regen_time=500,
                   available=True,
                   size=2,
                   cx=random.randint(start_size,screen.get_width()-start_size),
                   cy=random.randint(start_size,screen.get_height()-start_size)),0]
    berry_list.append(Aberry)
#create slimes at start
for i in range(10):
    my_slime = [Oslime.Slime(speed=1,
                 max_hunger=10,
                 metabolism=100,
                 current_hunger=10,
                 colour=(150,20,20),
                 size=start_size,
                 sight=50,
                 agression=1,
                 cx=random.randint(start_size,screen.get_width()-start_size),
                 cy=random.randint(start_size,screen.get_height()-start_size),
                 dead=False,
                 berries=berry_list)
             ,0]
    slimes_list.append(my_slime)
for i in range(10):
    my_slime2 = [Oslime.Slime(speed=0.5,
                     max_hunger=10,
                     metabolism=150,
                    current_hunger=10,
                     colour=(0,150,50),
                    size=start_size,
                     sight=50,
                     agression=1,
                     cx=random.randint(start_size,screen.get_width()-start_size),
                     cy=random.randint(start_size,screen.get_height()-start_size),
                    dead=False,
                     berries=berry_list)
                ,0]
    slimes_list.append(my_slime2)

#find starting averages
start_avgs = get_averages(slimes_list)
#while the program is playing

while running:
    # 1. Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Update game state
    slimes_to_remove = []  # Create an empty list to hold dead slimes

    for slime in slimes_list:


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
    draw_stats(screen,stat_font,slimes_list,start_avgs)
    # 5. Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame when the loop ends
pygame.quit()


