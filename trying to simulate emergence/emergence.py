import pygame
import numpy as np

# --- CONFIGURATION ---
WIDTH, HEIGHT = 1100, 800
N_PARTICLES = 600
N_TYPES = 4
R_MAX = 80
FRICTION = 0.85
DT = 0.5
FORCE_FACTOR = 0.3

# UI Layout Constants
UI_START_X = 20
UI_START_Y = 50
CELL_WIDTH = 60
CELL_HEIGHT = 30

COLOR_DEFS = [
    {"name": "RED", "rgb": (255, 50, 50)},
    {"name": "GREEN", "rgb": (50, 255, 50)},
    {"name": "BLUE", "rgb": (50, 50, 255)},
    {"name": "YELLO", "rgb": (255, 255, 50)},
    {"name": "CYAN", "rgb": (50, 255, 255)},
    {"name": "MAGEN", "rgb": (255, 50, 255)},
]
N_TYPES = min(N_TYPES, len(COLOR_DEFS))


def create_world():
    positions = np.random.rand(N_PARTICLES, 2) * [WIDTH, HEIGHT]
    velocities = np.zeros((N_PARTICLES, 2))
    types = np.random.randint(0, N_TYPES, N_PARTICLES)
    rules = np.random.uniform(-0.5, 0.5, (N_TYPES, N_TYPES))  # Start with mild rules
    return positions, velocities, types, rules


def update_physics(positions, velocities, types, rules):
    # Standard Particle Life Physics
    x = positions[:, 0:1]
    y = positions[:, 1:2]
    dx = x.T - x
    dy = y.T - y

    # Wrap borders
    dx = np.where(dx > WIDTH / 2, dx - WIDTH, dx)
    dx = np.where(dx < -WIDTH / 2, dx + WIDTH, dx)
    dy = np.where(dy > HEIGHT / 2, dy - HEIGHT, dy)
    dy = np.where(dy < -HEIGHT / 2, dy + HEIGHT, dy)

    r2 = dx ** 2 + dy ** 2
    r2 = np.maximum(r2, 0.01)
    r = np.sqrt(r2)

    mask = (r > 0) & (r < R_MAX)
    f_magnitude = np.zeros((N_PARTICLES, N_PARTICLES))
    f_magnitude[mask] = (1 - r[mask] / R_MAX)

    type_matrix_i = np.tile(types, (N_PARTICLES, 1)).T
    type_matrix_j = np.tile(types, (N_PARTICLES, 1))
    interactions = rules[type_matrix_i, type_matrix_j]
    f_magnitude *= interactions * FORCE_FACTOR

    vx_change = np.sum((dx / r) * f_magnitude, axis=1)
    vy_change = np.sum((dy / r) * f_magnitude, axis=1)

    velocities[:, 0] += vx_change * DT
    velocities[:, 1] += vy_change * DT
    velocities *= FRICTION
    positions += velocities * DT
    positions[:, 0] %= WIDTH
    positions[:, 1] %= HEIGHT

    return positions, velocities


def draw_ui(screen, rules, font):
    # Draw Background Panel
    panel_h = UI_START_Y + (N_TYPES * CELL_HEIGHT) + 40
    panel_w = UI_START_X + 80 + (N_TYPES * CELL_WIDTH) + 20

    s = pygame.Surface((panel_w, panel_h))
    s.set_alpha(220)
    s.fill((30, 30, 30))
    screen.blit(s, (0, 0))

    # Instructions
    header = font.render("L-CLICK: Attract (+)", True, (200, 200, 200))
    header2 = font.render("R-CLICK: Repel (-)", True, (200, 200, 200))
    screen.blit(header, (20, 10))
    screen.blit(header2, (220, 10))

    # Draw Column Headers (The "Target")
    for j in range(N_TYPES):
        col_x = UI_START_X + 80 + j * CELL_WIDTH
        name = font.render(COLOR_DEFS[j]["name"][:3], True, COLOR_DEFS[j]["rgb"])
        screen.blit(name, (col_x + 10, UI_START_Y - 20))

    # Draw Rows
    for i in range(N_TYPES):
        row_y = UI_START_Y + i * CELL_HEIGHT

        # Row Header (The "Actor")
        name = font.render(COLOR_DEFS[i]["name"], True, COLOR_DEFS[i]["rgb"])
        screen.blit(name, (UI_START_X, row_y + 5))

        # Draw Grid Cells
        for j in range(N_TYPES):
            col_x = UI_START_X + 80 + j * CELL_WIDTH
            val = rules[i][j]

            # Determine color intensity
            c_val = int(abs(val) * 255)
            if val > 0:
                bg_col = (0, c_val // 2 + 20, 0)
                txt_col = (150, 255, 150)
            else:
                bg_col = (c_val // 2 + 20, 0, 0)
                txt_col = (255, 150, 150)

            # Draw Cell Rect
            pygame.draw.rect(screen, bg_col, (col_x, row_y, CELL_WIDTH - 2, CELL_HEIGHT - 2))

            # Draw Number
            val_str = f"{val:+.1f}"
            txt = font.render(val_str, True, txt_col)
            screen.blit(txt, (col_x + 10, row_y + 5))


def handle_mouse_click(pos, rules, button):
    """Detects if a click hit a cell and updates the rule."""
    mx, my = pos

    # Check if within grid bounds
    grid_x = UI_START_X + 80
    grid_y = UI_START_Y

    if mx < grid_x or my < grid_y:
        return rules

    col = (mx - grid_x) // CELL_WIDTH
    row = (my - grid_y) // CELL_HEIGHT

    # Validate indices
    if 0 <= row < N_TYPES and 0 <= col < N_TYPES:
        # Left Click (1) = Increase, Right Click (3) = Decrease
        change = 0.1 if button == 1 else -0.1

        rules[row][col] += change

        # Clamp between -1.0 and 1.0
        rules[row][col] = np.clip(rules[row][col], -1.0, 1.0)

    return rules


def main():
    pygame.init()
    font = pygame.font.SysFont("consolas", 14, bold=True)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Particle Life - CLICK TABLE TO EDIT PHYSICS")
    clock = pygame.time.Clock()

    positions, velocities, types, rules = create_world()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    positions, velocities, types, rules = create_world()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle Click
                rules = handle_mouse_click(event.pos, rules, event.button)

        positions, velocities = update_physics(positions, velocities, types, rules)

        screen.fill((20, 20, 20))

        for i in range(N_PARTICLES):
            x, y = int(positions[i, 0]), int(positions[i, 1])
            color = COLOR_DEFS[types[i]]["rgb"]
            pygame.draw.circle(screen, color, (x, y), 3)

        draw_ui(screen, rules, font)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()