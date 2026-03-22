import pygame

class Slider:
    """

    description: A UI component that allows users to adjust a value by dragging a handle
                along a horizontal track


    attributes: rect: the size and shape of the slider track
                min_val: The minimum value the slider can represent
                max_val: The maximum value the slider can represent
                val: The current value selected by the slider position
                dragging: True or false depending on if the user is sliding it
                name: The display name of the slider
                colour: The color of the slider handle
    """
    def __init__(self, x, y, width, height, min_val, max_val, start_val, name, colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.dragging = False
        self.name = name
        self.colour = colour

    def handle_event(self, event):
        """
        Detects mouse clicks and movement to update the slider's dragging state
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.update_val(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_val(event.pos[0])

    def update_val(self, mouse_x):
        """
        Calculates the new value of the slider based on the relative X position
        of the mouse within the track
        """
        if mouse_x < self.rect.x:
            mouse_x = self.rect.x
        elif mouse_x > self.rect.x + self.rect.w:
            mouse_x = self.rect.x + self.rect.w

        ratio = (mouse_x - self.rect.x) / self.rect.w
        self.val = self.min_val + (self.max_val - self.min_val) * ratio

    def draw(self, screen, font):
        """
        draws the slider bar and labels it
        """
        pygame.draw.rect(screen, (100,100,100), self.rect)
        #determines the handle size and draws the handle
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + (self.rect.w * ratio)
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.h + 10)
        pygame.draw.rect(screen, (self.colour), handle_rect)
        #allows the variation of mutations and movement speed sliders to select a float
        if self.name == "variation of mutations" or self.name == "movement speed":
            label = font.render(f"{self.name}: {float(self.val):.2f}", True, (self.colour))
        else:
            label = font.render(f"{self.name}: {int(self.val)}", True, (self.colour))
        screen.blit(label, (self.rect.x, self.rect.y - 25))

class Button:
    """
        description: A clickable UI button that changes color when hovered and triggers events
        attributes: rect: The buttons shape adn size
                    hover_colour: the colour the button goes when the mouse hovers over it
                    name: text on the button
                    colour: colour of the button
                    font: font of the text on the button

    """
    def __init__(self, x, y, width, height, name, colour, hover_colour, font):

        self.rect = pygame.Rect(x, y, width, height)
        self.hover_colour = hover_colour
        self.name = name
        self.colour = colour
        self.font = font

    def draw(self, screen):
        """draws the button to the screen and checks if the mouse is hovering over it"""
        mouse_pos = pygame.mouse.get_pos()
        current_colour = self.hover_colour if self.rect.collidepoint(mouse_pos) else self.colour
        pygame.draw.rect(screen, current_colour, self.rect, border_radius=15)

        text_surf = self.font.render(self.name, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def isclicked(self, event):
        """Checks if the button has been clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            return True
        return False

class Box:
    """description: a box used to contain the simulation"""
    def __init__(self, x, y, width, height, colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = colour

    def draw(self, screen):
        """Draws the box outline to the screen"""
        pygame.draw.rect(screen, self.colour, self.rect, width=10)


def get_averages(slimes, surface, font):
    """
    Iterates through the slime list to calculate average of the attribute values
    """
    count = len(slimes)
    # if there are no slimes
    if count == 0:
        text = font.render("Population: 0", True, (255, 255, 255))
        surface.blit(text, (10, 10))
        return
    #sets totals to 0 before calculating them
    total_speed = total_size = total_sight = total_energy_efficiency = total_age = total_lifespan = 0

    for slime_data in slimes:
        s = slime_data[0]
        total_speed += s.speed
        total_size += s.size
        total_sight += s.sight
        total_energy_efficiency += s.actual_energy_efficiency
        total_age += s.age
        total_lifespan += s.lifespan
    #returns the averages and the population to a certain number of decimal places
    return (count,
            round(total_speed / count, 4),
            round(total_size / count, 2),
            round(total_sight / count, 2),
            round(total_energy_efficiency / count, 2),
            round(total_age / count, 2),
            round(total_lifespan / count, 2))

def draw_stats(surface, font, slimes, start_stats, total_death_from_age, total_starvations):
    """
    Calculates current averages displays and them to the screen,
    this allows for a real time comparison between the starting and current averages,
    also displays population, how many slimes died from starvation and how many slimes died from old age.
    """
    s_count, s_speed, s_size, s_sight, s_efficiency, s_age, s_lifespan = start_stats
    current_stats = get_averages(slimes, surface, font)
    count, avg_speed, avg_size, avg_sight, avg_eff, avg_age, avg_lifespan = current_stats

    # List of formatted strings to display
    stat_lines = [
        f"Population: {count}, Start: {s_count}",
        f"Avg Speed: {avg_speed}, Start: {s_speed}",
        f"Avg Size: {avg_size}, Start: {s_size}",
        f"Avg Sight: {avg_sight}, Start: {s_sight}",
        f"Avg energy efficiency: {avg_eff}, Start: {s_efficiency}",
        f"Avg age: {avg_age}, Start: {s_age}",
        f"Avg lifespan: {avg_lifespan}, Start:{s_lifespan}",
        f"Slimes dead from age: {total_death_from_age} slimes",
        f"Slimes dead from starvation: {total_starvations} slimes"
    ]
    #posistion of text
    x_pos = 1380
    y_pos = 10
    line_height = 20

    for i, line in enumerate(stat_lines):
        text_surf = font.render(line, True, (255, 255, 255))
        surface.blit(text_surf, (x_pos, y_pos + (line_height * i)))