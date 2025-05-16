import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Circle Moving to Random Locations")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Circle properties
circle_radius = 20
circle_color = RED
# Initial position (center of the screen)
circle_x = SCREEN_WIDTH // 2
circle_y = SCREEN_HEIGHT // 2
circle_speed = 3 # Pixels per frame

# Target position
target_x = random.randint(circle_radius, SCREEN_WIDTH - circle_radius)
target_y = random.randint(circle_radius, SCREEN_HEIGHT - circle_radius)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Game logic should go here ---

    # Calculate the distance to the target
    dx = target_x - circle_x
    dy = target_y - circle_y
    distance = math.sqrt(dx**2 + dy**2)

    # If the circle is close enough to the target, pick a new target
    if distance < circle_speed: # If closer than one step, snap to target and pick new
        circle_x = target_x
        circle_y = target_y
        target_x = random.randint(circle_radius, SCREEN_WIDTH - circle_radius)
        target_y = random.randint(circle_radius, SCREEN_HEIGHT - circle_radius)
        # print(f"New target: ({target_x}, {target_y})") # For debugging
    else:
        # Move towards the target
        # Normalize the direction vector (dx, dy)
        if distance != 0: # Avoid division by zero if already at target (though covered by above)
            move_x = (dx / distance) * circle_speed
            move_y = (dy / distance) * circle_speed

            circle_x += move_x
            circle_y += move_y

    # --- Drawing code should go here ---
    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the target (optional, for visualization)
    pygame.draw.circle(screen, GREEN, (int(target_x), int(target_y)), 5)

    # Draw the circle
    pygame.draw.circle(screen, circle_color, (int(circle_x), int(circle_y)), circle_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60) # 60 frames per second

# Quit Pygame
pygame.quit()