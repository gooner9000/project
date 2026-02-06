import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, start_val, name, colour):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = start_val
        self.dragging = False
        self.name = name
        self.colour = colour
    def handle_event(self, event):
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
        # Constrain mouse within the slider width
        if mouse_x < self.rect.x:
            mouse_x = self.rect.x
        elif mouse_x > self.rect.x + self.rect.w:
            mouse_x = self.rect.x + self.rect.w

        # Calculate value based on position
        ratio = (mouse_x - self.rect.x) / self.rect.w
        self.val = self.min_val + (self.max_val - self.min_val) * ratio

    def draw(self, screen, font):
        # Draw the track (dark gray)
        pygame.draw.rect(screen, (100,100,100), self.rect)

        # Calculate handle position
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + (self.rect.w * ratio)

        # Draw the handle (white rectangle)
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.h + 10)
        pygame.draw.rect(screen, (self.colour), handle_rect)

        # Draw the text label
        if self.name == "variation of mutations":
            label = font.render(f"{self.name}: {float(self.val):.2f}", True, (self.colour))
        else:
            label = font.render(f"{self.name}: {int(self.val)}", True, (self.colour))
        screen.blit(label, (self.rect.x, self.rect.y - 25))

class Button:
    def __init__(self, x, y, width, height, name, colour, hover_colour, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.hover_colour = hover_colour
        self.name = name
        self.colour = colour
        self.font = font

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_colour = self.hover_colour
        else:
            current_colour = self.colour
        pygame.draw.rect(screen, current_colour, self.rect, border_radius=15)

        text_surf = self.font.render(self.name, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    def isclicked(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            return True
        return False



def get_averages(slimes,surface,font):
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
    avg_speed = total_speed / count
    avg_size = round(total_size / count, 2)
    avg_sight = round(total_sight / count, 2)
    avg_meta = round(total_metabolism / count, 2)

    return count, avg_speed, avg_size, avg_sight, avg_meta



def draw_stats(surface, font, slimes, start_stats):
    s_count, s_speed, s_size, s_sight, s_metabolism = start_stats
    count, avg_speed, avg_size, avg_sight, avg_meta = get_averages(slimes,surface,font)
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

